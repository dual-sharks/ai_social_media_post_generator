import os
from datetime import datetime
import requests
from typing import Optional
from pydantic import Field, PrivateAttr
from openai import OpenAI
from crewai.tools import BaseTool

class ImageGenerationTool(BaseTool):
    name: str = Field(default="Image Generator")
    description: str = Field(default="Generates and saves professional background images for social media content")
    output_dir: str = Field(default="img")
    
    _client: OpenAI = PrivateAttr()

    def __init__(self, output_dir: str = "img", **data):
        super().__init__(**data)
        self._client = OpenAI()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _run(self, prompt: str, filename: Optional[str] = None) -> str:
        """
        Generate and save an image based on the prompt
        Args:
            prompt (str): Description of the image to generate
            filename (str, optional): Custom filename for the image
        Returns:
            str: Path to the saved image
        """
        try:
            response = self._client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"carousel_{timestamp}.png"
            
            response = requests.get(image_url)
            if response.status_code == 200:
                filepath = os.path.join(self.output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                return filepath
            return "Failed to download image"
        except Exception as e:
            return f"Error generating image: {str(e)}"