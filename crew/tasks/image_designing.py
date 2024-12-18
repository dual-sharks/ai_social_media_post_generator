"""
Task definition for generating background images for social media content.
"""

from crewai import Task
from crew.agents.image_designer import get_image_designer_agent

def get_image_design_task() -> Task:
    """Returns a configured image design task."""
    return Task(
        description=(
            "Create a single background image for a {social_platform} post about {topic} "
            "targeting {expertise_level} audience."
            "\n\nImage requirements:"
            "\n- Extremely subtle and minimal background designs"
            "\n- NO human figures, hands, or detailed objects"
            "\n- Focus on abstract patterns, gentle gradients, or simple geometric shapes"
            "\n- Ensure high text readability with clean, uncluttered compositions"
            "\n- Use muted colors that won't compete with text overlays"
            "\n- Color scheme based on complexity level:"
            "\n  * Beginner: Soft, warm gradients (blues, warm grays)"
            "\n  * Intermediate: Professional, neutral tones (navy, slate, subtle gold)"
            "\n  * Advanced: Rich, deep colors (dark blues, burgundy, charcoal)"
            "\n\nAdditional guidelines:"
            "\n- Maintain 30% or less visual complexity"
            "\n- Ensure patterns are subtle enough to read white or black text clearly"
            "\n- Avoid any text or symbols in the images"
        ),
        expected_output="Path to the generated background image.",
        agent=get_image_designer_agent()
    )

image_design_task = get_image_design_task()
