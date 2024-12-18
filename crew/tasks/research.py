"""
Task definition for research.
"""
from crewai import Task, Agent
from crew.agents.researcher import get_researcher_agent
def get_research_task() -> Task:
    """Creates a research task for gathering information about the topic."""
    return Task(
        description=(
            "Conduct thorough research on the topic {topic}. Focus on collecting key points, "
            "relevant statistics, and critical insights to form a strong foundation for the report."
            ),
            expected_output="A comprehensive list of data points and insights about {topic}.",
            agent=get_researcher_agent()
        )

research_task = get_research_task()
