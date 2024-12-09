import os
import base64
from pathlib import Path
from jinja2 import Template
from IPython.display import HTML, display
from datetime import datetime
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import time

class LinkedInPreviewGenerator:
    def __init__(self):
        self.template = Template('''
        <div style="max-width: 552px; margin: 20px auto; font-family: -apple-system,system-ui,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif; border: 1px solid #e0e0e0; border-radius: 8px; background: white; padding: 12px;">
            <!-- Profile Header -->
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <div style="width: 48px; height: 48px; border-radius: 50%; background: #0a66c2; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold;">DS</div>
                <div style="margin-left: 8px;">
                    <div style="font-weight: 600; color: rgba(0,0,0,0.9);">DualSharks</div>
                    <div style="font-size: 14px; color: rgba(0,0,0,0.6);">{{ timestamp }}</div>
                </div>
            </div>
            
            <!-- Post Content -->
            <div style="color: rgba(0,0,0,0.9); font-size: 14px; margin: 12px 0; white-space: pre-wrap;">{{ text }}</div>
            
            <!-- Images -->
            {% if images %}
            <div style="margin: 12px -12px;">
                {% if images|length == 1 %}
                <img src="{{ images[0] }}" style="width: 100%; max-height: 400px; object-fit: cover;">
                {% else %}
                <div style="display: grid; grid-template-columns: repeat({{ min(images|length, 2) }}, 1fr); gap: 2px;">
                    {% for image in images %}
                    <img src="{{ image }}" style="width: 100%; height: 250px; object-fit: cover;">
                    {% endfor %}
                </div>
                {% endif %}
            </div>
            {% endif %}
            
            <!-- Interaction Buttons -->
            <div style="display: flex; justify-content: space-around; margin-top: 12px; padding-top: 12px; border-top: 1px solid #e0e0e0;">
                <div style="color: rgba(0,0,0,0.6); font-size: 14px;">👍 Like</div>
                <div style="color: rgba(0,0,0,0.6); font-size: 14px;">💬 Comment</div>
                <div style="color: rgba(0,0,0,0.6); font-size: 14px;">↗️ Share</div>
            </div>
        </div>
        ''')

    def _get_image_base64(self, image_path: str) -> str:
        """Convert image to base64 string"""
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    def generate_preview(self, text: str, image_paths: List[str] = None) -> None:
        images = []
        if image_paths:
            for path in image_paths:
                if os.path.exists(path):
                    img_type = path.split('.')[-1].lower()
                    b64_img = self._get_image_base64(path)
                    images.append(f"data:image/{img_type};base64,{b64_img}")

        timestamp = datetime.now().strftime("%b %d, %Y")
        html = self.template.render(
            text=text,
            images=images,
            timestamp=timestamp
        )
        
        display(HTML(html))
    
    def save_preview_as_png(self, text: str, image_paths: List[str], output_path: str) -> str:
        """
        Save the LinkedIn preview as a PNG file
        Args:
            text: The post content
            image_paths: List of paths to images to include
            output_path: Where to save the PNG file
        Returns:
            str: Path to the saved PNG file
        """
        images = []
        if image_paths:
            for path in image_paths:
                if os.path.exists(path):
                    b64_img = self._get_image_base64(path)
                    img_type = path.split('.')[-1].lower()
                    images.append(f"data:image/{img_type};base64,{b64_img}")

        timestamp = datetime.now().strftime("%b %d, %Y")
        html = self.template.render(
            text=text,
            images=images,
            timestamp=timestamp
        )

        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
            f.write(f"""
                <html>
                <body style="background-color: #f3f2ef; padding: 20px;">
                    {html}
                </body>
                </html>
            """)
            temp_path = f.name

        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=800,1000")
            chrome_options.add_argument("--hide-scrollbars")

            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f"file://{temp_path}")
            time.sleep(1)
            
            preview = driver.find_element("css selector", "div[style*='max-width: 552px']")
            preview.screenshot(output_path)
            
            driver.quit()
            return output_path

        finally:
            os.unlink(temp_path)