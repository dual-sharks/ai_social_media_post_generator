"""
Defines content formatting requirements and specifications for different social media platforms
and audience expertise levels.
"""

from enum import Enum
from typing import Dict, Any

class Platform(Enum):
    """Supported social media platforms for content generation."""
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"

class ExpertiseLevel(Enum):
    """Target audience expertise levels for content customization."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

EXPERTISE_REQUIREMENTS: Dict[str, Dict[str, Any]] = {
    ExpertiseLevel.BEGINNER.value: {
        "description": "Explain concepts simply, use analogies, avoid jargon",
        "tone": "educational and supportive"
    },
    ExpertiseLevel.INTERMEDIATE.value: {
        "description": "Balance technical detail with practical application",
        "tone": "practical and analytical"
    },
    ExpertiseLevel.ADVANCED.value: {
        "description": "Focus on complex analysis, assume strong background knowledge",
        "tone": "technical and sophisticated"
    }
}

PLATFORM_FORMATS: Dict[str, Dict[str, Any]] = {
    Platform.LINKEDIN.value: {
        "description": (
            "Format requirements for LinkedIn:\n"
            "- NO asterisks or markdown formatting\n"
            "- For emphasis, use CAPS or simple text\n"
            "- Professional tone with clear section headers\n"
            "- Use line breaks for readability\n"
            "- Include relevant emojis sparingly\n"
            "\nExample format:\n"
            "MARKET INSIGHTS 📊\n"
            "Here's what you need to know...\n"
            "\nKey Statistics:\n"
            "• Point 1\n"
            "• Point 2\n"
            "\n#Hashtag1 #Hashtag2"
        )
    },
    Platform.TWITTER.value: {
        "description": (
            "Format requirements for Twitter:\n"
            "- Create a thread of 5-7 tweets\n"
            "- Each tweet must be under 280 characters\n"
            "- Use numbers for thread sequence\n"
            "- Include relevant emojis\n"
            "- End with call-to-action\n"
            "- Add hashtags to final tweet"
        )
    },
    Platform.INSTAGRAM.value: {
        "description": (
            "Format requirements for Instagram carousel:\n"
            "- Create 5-7 slides\n"
            "- One main point per slide\n"
            "- Start with hook slide\n"
            "- End with call-to-action\n"
            "- Use emojis for visual appeal\n"
            "- Short, punchy sentences\n"
            "- Hashtags in comment block"
        )
    }
}
