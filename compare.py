import os
from dotenv import load_dotenv
from openai import OpenAI

from models import Report
from verify import verify_references


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_without_search(topic):
    prompt = f"""
Write a short scientific or technical article about:

{topic}

Do NOT use web search.

Generate the article using your own existing knowledge.

The article must contain:
1. A title
2. An abstract
3. An introduction
4. Logical main sections
5. A conclusion
6. A reference list

Provide references based on your existing knowledge.
Do not claim that you searched the web.
"""

    response = client.responses.parse(
        model="gpt-4o-2024-08-06",
        input=prompt,
        text_format=Report
    )

    report = response.output_parsed

    if report is None:
        raise ValueError("The LLM did not return a valid Report.")

    return report


def compare_references(report):
    print("\nChecking references from the non-grounded article...\n")

    results = verify_references(report.references)

    valid_count = 0
    invalid_count = 0

    for i, result in enumerate(results, start=1):

        reference = result["reference"]
        verification = result["verification"]

        print("=" * 70)
        print(f"REFERENCE {i}")
        print("=" * 70)

        print("Author:", reference.authors)
        print("Title:", reference.title)
        print("Year:", reference.year)
        print("URL:", reference.url)

        print("\nVerification:")

        if verification.get("valid"):
            print("VALID")
            valid_count += 1
        else:
            print("NOT VERIFIED")
            invalid_count += 1

        print(verification)

    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)

    print(f"Total references: {len(results)}")
    print(f"Verified references: {valid_count}")
    print(f"Unverified references: {invalid_count}")


if __name__ == "__main__":
    topic = input("Enter a topic: ")

    print("\nGenerating article WITHOUT web search...\n")

    report = generate_without_search(topic)

    print("Article generated successfully.")

    compare_references(report)