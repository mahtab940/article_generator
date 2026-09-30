import requests
from bs4 import BeautifulSoup


def verify_reference(reference):
    url = reference.url

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code != 200:
            return {
                "valid": False,
                "reason": f"Website returned status code {response.status_code}",
                "url": url
            }

        soup = BeautifulSoup(response.text, "html.parser")

        page_text = soup.get_text(" ", strip=True).lower()

        title_found = reference.title.lower() in page_text

        year_found = str(reference.year) in page_text

        # Check whether part of the author information appears
        author_parts = reference.authors.lower().split()

        author_found = any(
            len(part) > 2 and part in page_text
            for part in author_parts
        )

        return {
            "valid": title_found and year_found and author_found,
            "author_found": author_found,
            "title_found": title_found,
            "year_found": year_found,
            "url_accessible": True,
            "url": url
        }

    except Exception as e:
        return {
            "valid": False,
            "reason": str(e),
            "url": url
        }


def verify_references(references):
    results = []

    for reference in references:
        result = verify_reference(reference)

        results.append({
            "reference": reference,
            "verification": result
        })

    return results