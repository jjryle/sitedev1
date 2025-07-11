# %%

import pandas as pd
import json
import os
import dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from google import genai
from google.genai import types
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from dotenv import load_dotenv

class NewsContentGenerator:
    def __init__(self, env_path, blog_id, html_file="news_response.html"):
        from dotenv import load_dotenv
        load_dotenv(env_path, override=True)
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.blog_id = blog_id
        self.html_file = html_file
        self.client = self._init_genai_client()
        self.blogger_ready_content = None # To store content formatted for Blogger
        self.google_search_tool = self._init_google_search_tool()

    def _init_genai_client(self):
        from google import genai
        from google.genai import types
        return genai.Client(
            api_key=self.GOOGLE_API_KEY,
            http_options=types.HttpOptions(api_version='v1alpha')
        )

    def _init_google_search_tool(self):
        from google.genai.types import Tool, GoogleSearch
        return Tool(google_search=GoogleSearch())

    #def build_news_prompt(self, initial_query):
    #    return f"""You are a news editor. Review the initial query: \"{initial_query}\"\n    Read each row's Title and body into one article. Synergize into a summary, \n    capturing the most interesting points relevant to the initial_query.\n    Present the summary as a short news article with 3-4 bullet points followed\n    by a \"300\" - \"400\" word summary.\n    Include a link to the source article and a list of follow-up questions that could be asked based on the summary.\n    The summary should be concise and engaging, suitable for a news article."""
    def build_news_prompt(self, blog_prompt_long):
        return f"""{blog_prompt_long} """


    def generate_content(self, news_prompt):
        from google.genai import types
        import datetime
        output_dir = r'C:\AppAdmin\kickserve'
        os.makedirs(output_dir, exist_ok=True)
        response = self.client.models.generate_content(
            model='gemini-2.5-pro-preview-05-06',
            contents=news_prompt,
            config=GenerateContentConfig(
                tools=[self.google_search_tool],
                response_modalities=["TEXT"],
            )
        )
        # Extract a headline (first 10 words) from the response text
        response_text = response.text.strip()
        headline = ' '.join(response_text.split()[:10])
        # Remove headline from body if it repeats at the start
        body = response_text
        if body.lower().startswith(headline.lower()):
            body = body[len(headline):].lstrip(' ,\n')
        md_file_path = os.path.join(output_dir, 'news_response.md')
        with open(md_file_path, 'w', encoding='utf-8') as md_file:
            md_file.write(f"# {headline}\n\n{body}\n")
        # Also create a timestamped copy
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext('news_response.md')
        md_file_copy = os.path.join(output_dir, f"news_response_{timestamp}{ext}")
        with open(md_file_copy, 'w', encoding='utf-8') as md_file:
            md_file.write(f"# {headline}\n\n{body}\n")
        return response

    def print_response(self, response):
        print(response.text)
        # Print each part if available
        if hasattr(response.candidates[0].content, 'parts'):
            for each in response.candidates[0].content.parts:
                print(getattr(each, 'text', each))
        # Safely print grounding_metadata if available
        grounding_metadata = getattr(response.candidates[0], 'grounding_metadata', None)
        if grounding_metadata and hasattr(grounding_metadata, 'search_entry_point'):
            search_entry_point = getattr(grounding_metadata, 'search_entry_point', None)
            if search_entry_point and hasattr(search_entry_point, 'rendered_content'):
                print(search_entry_point.rendered_content)

    def render_html_response(self):
        import markdown2
        import datetime
        import re
        output_dir = r'C:\AppAdmin\kickserve'
        os.makedirs(output_dir, exist_ok=True)
        md_file_path = os.path.join(output_dir, 'news_response.md')
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            response_text_for_processing = md_file.read()

        # Extract the headline from the first markdown H1 (first line starting with # )
        headline = None
        h1_match = re.search(r"^# (.+)$", response_text_for_processing, re.MULTILINE)
        if h1_match:
            headline = h1_match.group(1).strip()
            # Remove this H1 from the content to avoid duplication in HTML
            response_text_for_processing = re.sub(r"^# .+$\n?", "", response_text_for_processing, count=1, flags=re.MULTILINE)
        else:
            # fallback: use first 8 words
            headline = ' '.join(response_text_for_processing.strip().split()[:8]) + '...'

        # Convert markdown to HTML (after headline removal)
        try:
            html_body = markdown2.markdown(response_text_for_processing)
        except Exception:
            html_body = response_text_for_processing

        # Define CSS specifically for the content block to be published
        content_specific_css = '''
        <style>
        .gemini-generated-news-content {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #23272a; /* Dark background for the content block */
            color: #e0e0e0;       /* Light text for the content block */
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.5);
            padding: 20px;
            margin: 20px 0;     /* Vertical margin, horizontal will be handled by Blogger theme */
            max-width: 100%;    /* Ensure it fits within Blogger's post container */
            box-sizing: border-box; /* Ensures padding doesn't add to width */
            line-height: 1.6;   /* Improve readability */
        }
        .gemini-generated-news-content h1,
        .gemini-generated-news-content h2,
        .gemini-generated-news-content h3,
        .gemini-generated-news-content h4 {
            color: #8ab4f8;
        }
        .gemini-generated-news-content pre {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid #333;
        }
        .gemini-generated-news-content a {
            color: #82aaff;
        }
        .gemini-generated-news-content ul,
        .gemini-generated-news-content ol {
            margin-left: 2em;
            padding-left: 0; /* Reset padding if theme adds it */
        }
        .gemini-generated-news-content strong {
            color: #ffd700;
        }
        .gemini-generated-news-content img { /* Responsive images */
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px 0;
        }
        </style>
        '''

        # Only include the headline as <title> and a single <h1> in the content
        self.blogger_ready_content = f"""
        {content_specific_css}
        <div class=\"gemini-generated-news-content\">
        <h1>{headline}</h1>
        {html_body}
        </div>
        """

        local_preview_html = f"""
        <html>
        <head>
        <meta charset='utf-8'>
        <title>{headline}</title>
        <style>body {{ font-family: sans-serif; background-color: #f0f0f0; margin: 20px; }}</style>
        </head>
        <body>
            {self.blogger_ready_content}
        </body></html>
        """
        html_file_path = os.path.join(output_dir, self.html_file)
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(local_preview_html)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext(self.html_file)
        html_file_copy = os.path.join(output_dir, f"{base}_{timestamp}{ext}")
        with open(html_file_copy, "w", encoding="utf-8") as f:
            f.write(local_preview_html)

        return html_file_path

# Example usage:
if __name__ == "__main__":
    import config_settings
    # Remove Publisher import and related logic

    env_path = "C:\\Users\\johnj\\secure_configs\\AgenticResearch\\.env"
    publish_blog_id = os.getenv('KICKSERVE_BLOG_ID')
    initial_query = config_settings.initial_query

    generator = NewsContentGenerator(env_path, publish_blog_id)
    news_prompt = generator.build_news_prompt(initial_query)
    print("Generated Prompt:\n", news_prompt)

    response = generator.generate_content(news_prompt)
    # generator.print_response(response) # Optional: for debugging

    local_html_preview_file = generator.render_html_response()
    print(f"Local preview saved to: {local_html_preview_file}")
    print("\nTo publish this content, use the publish_news_response.py script and provide the generated HTML file as input.")

    # Optionally, open the preview in a browser
    import webbrowser
    webbrowser.open(f"file://{os.path.abspath(local_html_preview_file)}")