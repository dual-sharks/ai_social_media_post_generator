"""
Streamlit GUI application for managing CrewAI content generation workflows.
"""

import streamlit as st
from crewai import Agent, Task, Crew, Process
from constants.content_requirements import (
    Platform,
    ExpertiseLevel,
)
from typing import Dict, Any
from streamlit.components.v1 import html
from utils.linkedin_preview import LinkedInPreviewGenerator
import os
from crew.agents.image_designer import get_image_designer_agent
from crew.tasks.image_designing import image_design_task
from crew.tasks.research import research_task
from crew.tasks.writing import create_writing_task
from crew.agents.researcher import get_researcher_agent
from crew.agents.writer import get_writer_agent

def initialize_crew(topic: str, platform: Platform, expertise_level: ExpertiseLevel) -> Dict[str, Any]:
    """Initialize and run the CrewAI workflow with given parameters."""
    research_agent = get_researcher_agent()
    writer_agent = get_writer_agent()
    
    writing_task = create_writing_task(
        platform=platform,
        expertise_level=expertise_level,
        writer_agent=writer_agent
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
                        agents=[get_image_designer_agent()],
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