import json
import os
from dotenv import load_dotenv  # Add this import
from groq import Groq
from app.models.schemas import AnalysisResponse

# Force Python to read the .env file in the root directory
load_dotenv()

# Initialize the Groq client.
try:
    client = Groq()
except Exception:
    raise RuntimeError("Groq client failed to initialize. Check GROQ_API_KEY in the .env file.")

def generate_cv_feedback(cv_text: str, job_description: str, nlp_score: int) -> dict:
    """
    Calls Llama 3 via Groq to analyze the CV against the job description.
    Forces strict JSON output and validates it against our Pydantic API contract.
    """
    
    # The System Prompt acts as the engine and the governor. 
    # We define the strict CTO persona and the exact JSON shape.
    system_prompt = f"""You are a strict, highly technical CTO evaluating a candidate's CV against a Job Description.
    Do not be overly generous. Evaluate their actual architectural and tooling depth.
    
    You MUST respond ONLY with a valid JSON object. 
    
    The JSON must perfectly match this structure:
    {{
      "compatibility_score": {nlp_score}, 
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
        "<Specific, actionable advice 1>",
        "<Specific, actionable advice 2>",
        "<Specific, actionable advice 3>"
      ]
    }}
    
    Rules for the data:
    1. "compatibility_score" MUST be exactly {nlp_score}. Do not calculate it yourself.
    2. Radar chart values MUST be integers between 1 and 5. (1 = missing/novice, 3 = adequate, 5 = expert/lead level).
    3. Extract precise technical entities (e.g., frameworks, databases, CI/CD tools, architectural patterns).
    4. "actionable_feedback" must be exactly 3 bullet points of constructive, highly specific advice. Tell the candidate exactly what technical gaps they need to close or how to rephrase their experience to match the offer.
    """

    user_prompt = f"CV TEXT:\n{cv_text}\n\nJOB DESCRIPTION:\n{job_description}"

    try:
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"), 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1, # Keep it near zero for deterministic, stable JSON formatting
            response_format={"type": "json_object"} 
        )
        
        raw_json = response.choices[0].message.content
        parsed_data = json.loads(raw_json)
        
        # The Shield: Pass the raw dictionary into our Pydantic model.
        # If the LLM hallucinates a key or uses the wrong type, this raises a ValidationError.
        validated_data = AnalysisResponse(**parsed_data)
        
        return validated_data.model_dump()
        
    except json.JSONDecodeError:
        raise ValueError("The LLM failed to return a readable JSON string.")
    except Exception as e:
        raise ValueError(f"LLM Generation failed: {str(e)}")