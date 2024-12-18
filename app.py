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
                    
                    st.success("Content generated successfully!")
                    st.text_area("Generated Content", result, height=800)
                    
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")
    
    with col2:
        st.title("Preview")
        if 'result' in locals() and platform == Platform.LINKEDIN.value:
            from utils.linkedin_preview import LinkedInPreviewGenerator
            preview = LinkedInPreviewGenerator().generate_preview(result)
            st.components.v1.html(preview, height=800, width=800)

if __name__ == "__main__":
    main() 