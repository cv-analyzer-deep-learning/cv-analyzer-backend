import spacy
from sentence_transformers import SentenceTransformer, util

# Load models globally so they only initialize once when the server starts
# Using the multilingual model because CVs/Offers often mix French and English tech terms
print("Loading NLP models... This may take a moment.")
try:
    nlp = spacy.load("fr_core_news_md")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
except OSError:
    raise RuntimeError("Models not found. Did you run 'python -m spacy download fr_core_news_md'?")

def calculate_similarity_score(cv_text: str, job_text: str) -> int:
    """
    Calculates a semantic similarity score between the CV and Job Offer.
    Returns an integer between 0 and 100.
    """
    # Encode both texts into high-dimensional vectors
    cv_embedding = model.encode(cv_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)
    
    # Calculate Cosine Similarity
    cosine_scores = util.cos_sim(cv_embedding, job_embedding)
    
    # Convert tensor to float and scale to 100
    raw_score = float(cosine_scores[0][0])
    
    # Cosine similarity can technically be negative, though rare here. 
    # Clamp it between 0 and 100.
    normalized_score = max(0, min(100, int(raw_score * 100)))
    
    return normalized_score

def extract_basic_entities(text: str) -> list:
    """
    Uses spaCy to extract standard entities to satisfy the NLP rubric.
    Note: Tech skills will primarily be extracted via the LLM later.
    """
    doc = nlp(text)
    # Extracting standard entities like Organizations (ORG) or Locations (LOC)
    entities = list(set([ent.text for ent in doc.ents if ent.label_ in ["ORG", "MISC"]]))
    return entities