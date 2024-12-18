"""
Researcher agent for gathering detailed information and insights about topics.
"""

from crewai import Agent
from crewai_tools import SerperDevTool
from constants.domains import PREFERRED_DOMAINS

def get_researcher_agent() -> Agent:
    """Returns a configured Researcher agent."""
    return Agent(
        role='Researcher',
        goal='Gather detailed and relevant information about {topic}.',
        backstory=(
            "A skilled and inquisitive researcher, adept at diving deep into topics "
            "and pulling out critical insights that are accurate and comprehensive. "
            "Prioritizes authoritative sources and cross-references information."
        ),
        verbose=True,
        memory=True,
        tools=[
            SerperDevTool(
                search_params={
                    "site": " OR ".join(PREFERRED_DOMAINS.get("trading", [])),
                    "num": 5
                }
            ),
            SerperDevTool(
                search_params={
                    "num": 5,
                    "exclude": "pinterest.com,facebook.com,instagram.com"
                }
            )
        ]
    )