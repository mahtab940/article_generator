from pydantic import BaseModel, Field
from typing import List


class Reference(BaseModel):
    authors: str
    title: str
    year: int
    url: str


class Section(BaseModel):
    heading: str
    content: str


class Report(BaseModel):
    title: str
    abstract: str
    introduction: str
    sections: List[Section]
    conclusion: str
    references: List[Reference]
if __name__ == "__main__":
    test = Report(
        title="Test Article",
        abstract="This is a test.",
        introduction="This is the introduction.",
        sections=[
            Section(
                heading="Background",
                content="This is the main section."
            )
        ],
        conclusion="This is the conclusion.",
        references=[
            Reference(
                authors="Test Author",
                title="Test Paper",
                year=2025,
                url="https://example.com"
            )
        ]
    )

    print(test)

