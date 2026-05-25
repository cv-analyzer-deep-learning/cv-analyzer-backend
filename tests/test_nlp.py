from app.services.nlp_service import calculate_similarity_score, extract_basic_entities

# A condensed representation of a Full Stack Developer CV
MOCK_CV = """
Développeur Full Stack spécialisé dans la conception d'architectures SaaS performantes.
Forte expertise technique (Next.js, architecture Event Sourcing, AWS).
Backend & Cloud : Node.js, PostgreSQL, Prisma ORM.
Qualité logicielle : TDD, CI/CD, Jest, Cypress.
"""

# Scenario A: A highly matching job offer
PERFECT_MATCH_JOB = """
Nous recherchons un Développeur Full Stack avec une forte maîtrise de Next.js et Node.js.
Une expérience avec AWS et la mise en place de tests automatisés (Cypress, Jest) est exigée.
La connaissance des architectures SaaS et de PostgreSQL est un gros plus.
"""

# Scenario B: A completely unrelated job offer
POOR_MATCH_JOB = """
Recherche Développeur C++ embarqué pour l'industrie automobile.
Maîtrise de C, C++, et des systèmes temps réel (RTOS).
Connaissance des protocoles CAN et LIN.
"""

def run_nlp_tests():
    print("🧠 Initializing NLP Core Test...\n")
    print("=" * 60)
    
    # Test 1: The Semantic Math
    print("Testing Semantic Similarity (Cosine Distance):")
    high_score = calculate_similarity_score(MOCK_CV, PERFECT_MATCH_JOB)
    low_score = calculate_similarity_score(MOCK_CV, POOR_MATCH_JOB)
    
    print(f"  ➔ Score vs Perfect Match Job: {high_score}/100")
    print(f"  ➔ Score vs Unrelated Job:     {low_score}/100")
    print("-" * 60)
    
    # Test 2: The spaCy Fallback
    print("Testing spaCy Entity Extraction:")
    entities = extract_basic_entities(MOCK_CV)
    print(f"  ➔ Extracted Entities: {entities}")
    
    print("=" * 60)

if __name__ == "__main__":
    run_nlp_tests()