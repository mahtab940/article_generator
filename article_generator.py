import os
from dotenv import load_dotenv
from openai import OpenAI

from models import Report
from search import search_web
from verify import verify_references
from pdf_generator import generate_pdf


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_report(topic, sources):
    source_text = ""

    for i, source in enumerate(sources, start=1):
        source_text += f"""
SOURCE {i}
Title: {source["title"]}
URL: {source["url"]}
Content:
{source["content"]}

"""

    print("Sources prepared for the LLM.")

    prompt = f"""
Write a short scientific or technical article about:

{topic}

Use ONLY the information provided in the web sources below.

IMPORTANT RULES:
- Do not invent sources.
- Do not invent authors, titles, years, or URLs.
- Use the provided sources for the reference list.
- The article must contain:
  1. Title
  2. Abstract
  3. Introduction
  4. Logical main sections
  5. Conclusion
  6. Reference list
- References must correspond to the provided web sources.
- Use APA-style in-text citations in the article.
- Every factual claim based on a source should have an APA-style
  in-text citation, for example (Smith, 2024).
- Every in-text citation must correspond to a reference in the
  reference list.
- Every reference must come from one of the provided web sources.
- Keep the article concise and factual.

WEB SOURCES:
{source_text}
"""

    response = client.responses.parse(
        model="gpt-4o-2024-08-06",
        input=prompt,
        text_format=Report
    )

    report = response.output_parsed

    if report is None:
        raise ValueError("The LLM did not return a valid Report.")

    print("Report generated and structured successfully.")

    return report


if __name__ == "__main__":
    topic = input("Enter a topic: ")

    print("\nSearching the web...\n")

    sources = search_web(topic, max_results=5)

    print(f"\nFound {len(sources)} sources.")

    # Generate structured article
    report = generate_report(topic, sources)

    print("\nReport generated successfully.")

    # Verify references
    print("\nChecking references...")

    verification_results = verify_references(report.references)

    for result in verification_results:
        print(result["verification"])

    # Generate PDF
    print("\nGenerating PDF...")

    generate_pdf(report)

    print("\nDone!")
    print("Your article is saved as:")
    print("output/article.pdf")