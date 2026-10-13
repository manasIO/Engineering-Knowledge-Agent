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

# Individual metrics for each question
evaluation_results = []
for item in questions:
    question = item["question"]
    excepted = item["relevant_sections"]

    start_time = time.perf_counter()

    results = retrieve(question, top_k=3)

    latency_ms = (time.perf_counter() - start_time) * 1000

    metadatas = results["metadatas"][0]

    metrics = evaluate_ranking(metadatas, excepted)

    evaluation_results.append({
        "id": item["id"],
        "question": question,
        "expected": excepted,
        "retrieved": metadatas,
        "latency_ms": latency_ms,
        **metrics
    })

# Calculating aggregate metrics
total = len(evaluation_results)

if total == 0:
    raise ValueError("No evaluation questions found.")

hit_at_1 = sum(r["hit_at_1"] for r in evaluation_results) / total
hit_at_3 = sum(r["hit_at_3"] for r in evaluation_results) / total
mrr = sum(r["reciprocal_rank"] for r in evaluation_results) / total

avg_latency = sum(r["latency_ms"] for r in evaluation_results) / total

print("\n===== RETRIEVAL EVALUATION =====")
print(f"Total Questions: {total}")
print(f"Hit@1:           {hit_at_1:.3f}")
print(f"Hit@3:           {hit_at_3:.3f}")
print(f"MRR@3:           {mrr:.3f}")
print(f"Avg Latency:     {avg_latency:.2f} ms")


# Printing failure questions
print("\n===== FAILED TOP-1 QUESTIONS =====")

for result in evaluation_results:
    if result["hit_at_1"] == 0:
        print(f"\nID: {result['id']}")
        print(f"Question: {result['question']}")
        print(f"Expected: {result['expected']}")

        for rank, metadata in enumerate(result["retrieved"], start=1):
            print(
                f"  Rank {rank}: "
                f"{metadata.get('source')} / "
                f"{metadata.get('section')}"
            )


# test_results = [
#     {"source": "other.txt", "section": "Overview"},
#     {"source": "deployment_guide.txt", "section": "Monitoring"},
#     {"source": "other.txt", "section": "Configuration"}
# ]

# expected = [
#     {"source": "deployment_guide.txt", "section": "Monitoring"}
# ]
# print(evaluate_ranking(test_results, expected))


# TESTING RETRIEVAL
# question_data = questions[0]

# question = question_data["question"]
# excepted = question_data["relevant_sections"]

# results = retrieve(question, top_k=3)

# metadatas = results["metadatas"][0]

# metrics = evaluate_ranking(metadatas, excepted)

# print("\nQuestion: ", question)
# print("Expected: ", excepted)
# print("Retrieved: ", metadatas)
# print("Metrics: ", metrics)