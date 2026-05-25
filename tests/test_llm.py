import json
from app.services.llm_service import generate_cv_feedback

DUMMY_CV_TEXT = """
Guei - Full Stack Developer (Freelance External) / Lead Tech
Ingénierie Frontend : Remplacement d'une gestion d'état classique par une architecture Event Sourcing (Next.js / Zustand).
Backend & Cloud : Modélisation de base de données via Prisma ORM, Node.js, PostgreSQL, AWS.
Qualité : Pilotage d'une stratégie de tests automatisés (Jest, Cypress) visant 80% de couverture.
"""

DUMMY_JOB_OFFER = """
Recherche Développeur Full Stack Confirmé pour une FinTech.
Compétences requises : React, Node.js, TypeScript.
Un profil orienté produit avec une expérience en SaaS B2B est un gros plus.
Maîtrise exigée de Docker, Kubernetes, et des pipelines CI/CD (GitLab CI).
Une expérience préalable avec des APIs financières (GraphQL) est attendue.
"""

def run_llm_test():
    print("🚀 Contacting Groq API (Llama 3)...")
    
    try:
        # We simulate the exact scenario we hit earlier: a low math score (12)
        # due to vocabulary mismatch, despite high technical skills.
        mock_nlp_score = 12
        
        
        # The NLP score is no longer passed in
        result = generate_cv_feedback(DUMMY_CV_TEXT, DUMMY_JOB_OFFER, mock_nlp_score)
        
        print("\n✅ Success! The LLM autonomously generated the score and passed the Pydantic shield:")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")

if __name__ == "__main__":
    run_llm_test()