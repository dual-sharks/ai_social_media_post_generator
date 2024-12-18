"""
Image Designer agent for generating background images for social media content.
Specializes in creating minimal, text-friendly designs with appropriate color schemes.
"""

from crewai import Agent
from tools.image_generation.image_gen import ImageGenerationTool

def get_image_designer_agent() -> Agent:
    """Returns a configured Image Designer agent."""
    return Agent(
        role='Image Designer',
        goal='Create subtle, text-friendly background images for social media content',
        backstory=(
            "An expert in creating minimalist, professional background designs "
            "that enhance readability and maintain visual hierarchy. Specializes in "
            "subtle patterns, gradients, and abstract compositions that complement "
            "text overlays without competing for attention."
        ),
        verbose=True,
        memory=True,
        tools=[ImageGenerationTool()]
    )