from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool


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
            verbose=True
        )

    @agent
    def company_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['company_summarizer'],
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
