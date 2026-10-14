# CITATION VALIDATOR

import re

def extract_citations(answer: str) -> list[int]:
    pattern = r"\[Source\s+(\d+)(?:\s+\([^\]]+\))?\]"

    matches = re.findall(pattern, answer)

    return [int(match) for match in matches]

def validate_citations(answer: str, source_count: int):
    citations = extract_citations(answer)

    valid_ids = set(range(1, source_count + 1))

    invalid = [
        citation
        for citation in citations
        if citation not in valid_ids
    ]

    return {
        "citations": citations,
        "invalid_citations": invalid,
        "all_valid": len(invalid) == 0
    }

if __name__ == "__main__":
    test_cases = [
        "Monitor latency [Source 1].",
        "Run security checks [Source 2] and [Source 3].",
        "Use PostgreSQL [Source 7].",
        "Engineers should monitor errors."
    ]

    for answer in test_cases:
        result = validate_citations(answer, source_count=3)

        print(f"\nAnswer: {answer}")
        print(f"Validation: {result}")