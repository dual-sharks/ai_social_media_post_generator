"""
Streamlit GUI application for managing CrewAI content generation workflows.
"""

import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from constants.content_requirements import (
    Platform,
    ExpertiseLevel,
    PLATFORM_FORMATS,
    EXPERTISE_REQUIREMENTS
)
from constants.domains import PREFERRED_DOMAINS
from typing import Dict, Any
from streamlit.components.v1 import html
from utils.linkedin_preview import LinkedInPreviewGenerator
from tools.image_generation.image_gen import ImageGenerationTool
import os

# Move these definitions to the top level, after imports
image_designer_agent = Agent(
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

image_design_task = Task(
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
    agent=image_designer_agent
)

def initialize_crew(topic: str, platform: Platform, expertise_level: ExpertiseLevel) -> Dict[str, Any]:
    """Initialize and run the CrewAI workflow with given parameters."""
    research_agent = Agent(
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
    
    writer_agent = Agent(
        role='Writer',
        goal='Create content about {topic} tailored for {expertise_level} audience on {social_platform}.',
        backstory=(
            "An expert content creator who specializes in adapting complex topics for different "
            "audiences and social media platforms. Skilled at creating engaging content that "
            "matches each platform's unique style and requirements."
        ),
        verbose=True,
            memory=True,
        )
    
    writing_task = create_writing_task(
        platform=platform,
        expertise_level=expertise_level,
        writer_agent=writer_agent
    )
    research_task = Task(
            description=(
                "Conduct thorough research on the topic {topic}. Focus on collecting key points, "
                "relevant statistics, and critical insights to form a strong foundation for the report."
            ),
            expected_output="A comprehensive list of data points and insights about {topic}.",
            agent=research_agent
        )
    
    crew = Crew(
        agents=[research_agent, writer_agent],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew.kickoff(
        inputs={
            "topic": topic,
            "expertise_level": expertise_level.value,
            "social_platform": platform.value
        }
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

def main():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title("Social Media Content Generator")
        
        # Input fields
        topic = st.text_input("Topic", "trading crude oil futures")
        
        platform = st.selectbox(
            "Platform",
            options=[p.value for p in Platform],
            format_func=lambda x: x.title()
        )
        
        expertise = st.selectbox(
            "Expertise Level",
            options=[e.value for e in ExpertiseLevel],
            format_func=lambda x: x.title()
        )
        
        if st.button("Generate Content"):
            with st.spinner("Generating content..."):
                try:
                    result = initialize_crew(
                        topic=topic,
                        platform=Platform(platform),
                        expertise_level=ExpertiseLevel(expertise)
                    )
                    
                    # Generate image
                    image_crew = Crew(
                        agents=[image_designer_agent],
                        tasks=[image_design_task],
                        process=Process.sequential
                    )
                    
                    image_result = image_crew.kickoff(inputs={
                        "topic": topic,
                        "expertise_level": expertise,
                        "social_platform": platform,
                        "content": result
                    })
                    
                    st.success("Content generated successfully!")
                    st.text_area("Generated Content", result, height=800)
                    
                    # Move preview generation inside try block
                    if platform == Platform.LINKEDIN.value:
                        # Parse single image path from TaskOutput
                        image_path = image_result.raw.strip()
                        if image_path.startswith('- '):
                            image_path = image_path[2:]
                        
                        preview = LinkedInPreviewGenerator().generate_preview(
                            content=result,
                            image_paths=[image_path] if os.path.exists(image_path) else None
                        )
                        with col2:
                            st.title("Preview")
                            st.components.v1.html(preview, height=1200, width=1000)
                            
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")

if __name__ == "__main__":
    main() 