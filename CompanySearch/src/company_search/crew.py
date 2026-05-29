import os

from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool

from company_search.models import CompanyReport

_llm = LLM(
    model=os.environ["MODEL"],
    api_base=os.environ["AZURE_API_BASE"],
    api_key=os.environ["AZURE_API_KEY"],
    api_version=os.environ["AZURE_API_VERSION"],
)


@CrewBase
class CompanySearch():
    """CompanySearch crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def company_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['company_researcher'],
            tools=[SerperDevTool()],
            llm=_llm,
            verbose=True
        )

    @agent
    def company_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['company_summarizer'],
            llm=_llm,
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['summary_task'],
            output_pydantic=CompanyReport,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CompanySearch crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
