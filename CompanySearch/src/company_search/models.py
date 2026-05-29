from pydantic import BaseModel, Field
from typing import List


class NewsItem(BaseModel):
    date: str = Field(description="Date of the news item (e.g. 2025-01-15 or 'January 2025')")
    headline: str = Field(description="Short headline of the news")
    description: str = Field(description="1-2 sentence description of the news")
    source: str = Field(default="", description="Source name or URL")


class CompanyReport(BaseModel):
    company_name: str = Field(description="Name of the company researched")
    about: str = Field(description="2-3 sentence overview of what the company does, its business model, and key facts")
    news: List[NewsItem] = Field(description="List of 3 to 5 recent news items about the company")
