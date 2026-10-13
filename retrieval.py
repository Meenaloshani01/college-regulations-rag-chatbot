
import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Step 1: Load policy chunks
BASE_DIR = Path(__file__).resolve().parent
CHUNKS_PATH = BASE_DIR / "data" / "processed" / "chunks.json"

with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
    chunks = json.load(file)

if not chunks:
    raise ValueError(f"No policy chunks found at {CHUNKS_PATH}")


# Step 2: Prepare policy text
policy_texts = [chunk["text"] for chunk in chunks]


# Step 3: Build the local TF-IDF search index
vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    stop_words="english"
)

policy_vectors = vectorizer.fit_transform(policy_texts)


# Step 4: Search for a relevant policy
def search_policy(question):
    question = question.strip()

    if not question:
        return None, 0.0

    question_vector = vectorizer.transform([question])

    if question_vector.nnz == 0:
        print("No policy vocabulary matched.")
        return None, 0.0

    scores = cosine_similarity(
        question_vector,
        policy_vectors
    )[0]

    best_index = int(scores.argmax())
    best_score = float(scores[best_index])

    ranked_indices = scores.argsort()[::-1]

    second_score = (
        float(scores[ranked_indices[1]])
        if len(ranked_indices) > 1
        else 0.0
    )

    print("\nQuestion:", question)
    print("Policy scores:", scores.round(3))
    print("Best score:", round(best_score, 3))
    print("Second-best score:", round(second_score, 3))

    # Conservative fallback for unrelated questions
    if best_score < 0.15:
        return None, best_score

    # Reject ambiguous matches between different policies
    if len(chunks) > 1 and best_score - second_score < 0.02:
        return None, best_score

    return chunks[best_index], best_score


# Step 5: Terminal chatbot
def run_chatbot():
    while True:
        question = input(
            "\nAsk a college policy question (or type 'exit'): "
        ).strip()

        if question.lower() == "exit":
            print("Thank you for using CampusPolicy AI!")
            break

        if not question:
            print("Please enter a question.")
            continue

        result, score = search_policy(question)

        if result is None:
            print("\nSorry, I couldn't find a sufficiently relevant policy.")
            print("Try asking about attendance, exams, or leave.")
        else:
            print("\nRelevant Policy:", result["source"])
            print("Policy ID:", result["chunk_id"])
            print("Similarity Score:", round(score, 3))
            print("Retrieved Text:", result["text"])


# Step 6: Run terminal chatbot only when executed directly
if __name__ == "__main__":
    run_chatbot()
