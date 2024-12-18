from crewai import Task, Agent
from constants.content_requirements import (
    Platform,
    ExpertiseLevel,
    PLATFORM_FORMATS,
    EXPERTISE_REQUIREMENTS
)

def create_writing_task(platform: Platform, expertise_level: ExpertiseLevel, writer_agent: Agent) -> Task:
    """Creates a writing task with specific requirements based on platform and expertise level"""
    platform_format = PLATFORM_FORMATS.get(platform.value, {}).get("description", "")
    expertise_reqs = EXPERTISE_REQUIREMENTS.get(expertise_level.value, {})
    
    task_description = (
        "Using the research findings, create content about {topic} for {social_platform}. "
        f"The content should be appropriate for a {expertise_level} audience with a "
        f"{expertise_reqs.get('tone', 'neutral')} tone.\n\n"
        "IMPORTANT FORMATTING RULES:\n"
        "- DO NOT use any markdown formatting (no asterisks, underscores, or other symbols)\n"
        "- For emphasis, use CAPS or simply regular text\n"
        "- Numbers should be written plainly without any special formatting\n\n"
        f"{platform_format}\n\n"
        f"{expertise_reqs.get('description', '')}\n\n"
        "Ensure the content is engaging, accurate, and matches the platform's style."
    )
    
    return Task(
        description=task_description,
        expected_output=f"Platform-native content formatted for {platform}",
        agent=writer_agent,
        async_execution=False
    )