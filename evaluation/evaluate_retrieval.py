import json
from pathlib import Path

import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "app"))

from retrieve import retrieve

QUESTIONS_FILE = Path(__file__).with_name("questions.json")

with open(QUESTIONS_FILE, encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions")

def is_relevant(metadata, relevant_sections):
    for expected in relevant_sections:
        if(
            metadata.get("source") == expected["source"]
            and metadata.get("section") == expected["section"]
        ): 
            return True
    return False

def evaluate_ranking(metadatas, relevant_sections):
    first_relevant_rank = None

    for rank, metadata in enumerate(metadatas, start=1):
        if is_relevant(metadata, relevant_sections):
            first_relevant_rank = rank
            break

    return {
        "hit_at_1": int(first_relevant_rank == 1),
        "hit_at_3": int(first_relevant_rank is not None and first_relevant_rank <=3),
        "reciprocal_rank": (1/first_relevant_rank 
                            if first_relevant_rank is not None 
                            else 0)
    }

# test_results = [
#     {"source": "other.txt", "section": "Overview"},
#     {"source": "deployment_guide.txt", "section": "Monitoring"},
#     {"source": "other.txt", "section": "Configuration"}
# ]

# expected = [
#     {"source": "deployment_guide.txt", "section": "Monitoring"}
# ]
# print(evaluate_ranking(test_results, expected))

question_data = questions[0]

question = question_data["question"]
excepted = question_data["relevant_sections"]

results = retrieve(question, top_k=3)

metadatas = results["metadatas"][0]

metrics = evaluate_ranking(metadatas, excepted)

print("\nQuestion: ", question)
print("Expected: ", excepted)
print("Retrieved: ", metadatas)
print("Metrics: ", metrics)