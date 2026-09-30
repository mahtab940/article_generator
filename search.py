import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(topic, max_results=5):
    response = tavily.search(
        query=topic,
        search_depth="advanced",
        max_results=max_results
    )

    sources = []

    for result in response["results"]:
        sources.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", "")
        })

    return sources


if __name__ == "__main__":
    topic = input("Enter a topic: ")

    print("\nSearching the web...\n")

    sources = search_web(topic)

    for i, source in enumerate(sources, start=1):
        print("=" * 70)
        print(f"SOURCE {i}")
        print("=" * 70)
        print("Title:", source["title"])
        print("URL:", source["url"])
        print("Content:", source["content"][:500])
        print()