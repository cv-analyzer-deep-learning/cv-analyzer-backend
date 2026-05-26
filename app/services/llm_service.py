import json
from groq import Groq
from app.core.config import settings
from app.models.schemas import AnalysisResponse

# Initialize the Groq client strictly using the config hub
try:
    client = Groq(api_key=settings.GROQ_API_KEY)
except Exception:
    raise RuntimeError("Groq client failed to initialize. Check GROQ_API_KEY in the .env file.")

def generate_cv_feedback(cv_text: str, job_description: str, nlp_score: int) -> dict:
    """
    Calls Llama 3 via Groq to analyze the CV against the job description.
    Uses the mathematical NLP score as a baseline, then adjusts it qualitatively.
    """
    
    system_prompt = f"""You are a strict, highly technical CTO evaluating a candidate's CV against a Job Description.
    
    You are provided with a baseline mathematical semantic similarity score: {nlp_score}/100.
    This baseline score is calculated via cosine distance. It is strictly literal and often artificially low if the CV is much longer than the job offer, or if the candidate uses different terminology for the same concepts.
    
    Your job is to synthesize this data. Review their actual architectural and tooling depth, and adjust the baseline {nlp_score} into a final, realistic compatibility score.
    
    You MUST respond ONLY with a valid JSON object matching this structure:
    {{
      "compatibility_score": <int 0-100>, 
      "radar_chart_data": {{
        "technical_skills": <int 1-5>,
        "domain_knowledge": <int 1-5>,
        "tooling_and_infrastructure": <int 1-5>,
        "soft_skills": <int 1-5>,
        "experience_level": <int 1-5>
      }},
      "matching_entities": ["<skill1>", "<skill2>"],
      "missing_entities": ["<missing_skill1>"],
      "actionable_feedback": [
        "<Specific advice 1 referencing the math/skills gap>",
        "<Specific advice 2>",
        "<Specific advice 3>"
      ]
    }}
    
    Rules for the data:
    1. "compatibility_score" MUST be an integer between 0 and 100. If the baseline is {nlp_score} but you see deep technical overlap, adjust it upward significantly. If they lack core tools, keep it closer to the baseline.
    2. Radar chart values MUST be integers between 1 and 5. (1 = missing, 3 = adequate, 5 = expert).
    3. Extract precise technical entities (e.g., frameworks, databases, CI/CD tools).
    4. "actionable_feedback" must be exactly 3 bullet points. The feedback should explain the gap that caused their final score.
    """

    user_prompt = f"CV TEXT:\n{cv_text}\n\nJOB DESCRIPTION:\n{job_description}"

    try:
        response = client.chat.completions.create(
            # Dynamically load the model from the config hub
            model=settings.GROQ_MODEL, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1, 
            response_format={"type": "json_object"} 
        )
        
        raw_json = response.choices[0].message.content
        parsed_data = json.loads(raw_json)
        
        validated_data = AnalysisResponse(**parsed_data)
        
        return validated_data.model_dump()
        
    except json.JSONDecodeError:
        raise ValueError("The LLM failed to return a readable JSON string.")
    except Exception as e:
        raise ValueError(f"LLM Generation failed: {str(e)}")