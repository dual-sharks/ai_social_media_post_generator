"""
Writer agent for creating platform-specific social media content.
"""

from crewai import Agent

def get_writer_agent() -> Agent:
    """Returns a configured Writer agent."""
    return Agent(
        role='Writer',
        goal='Create content about {topic} tailored for {expertise_level} audience on {social_platform}.',
        backstory=(
            "An expert content creator who specializes in adapting complex topics for different "
            "audiences and social media platforms. Skilled at creating engaging content that "
            "matches each platform's unique style and requirements."
        ),
        verbose=True,
        memory=True
    ) 