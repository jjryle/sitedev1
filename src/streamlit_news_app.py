import streamlit as st
import os
import datetime
from GenerateContent import NewsContentGenerator  # Fixed import
import config_settings
from google.genai import errors
from src.publish_news_response import Publisher

class StreamlitNewsApp:
    def __init__(self):
        self.output_dir = r'C:\AppAdmin\kickserve'
        os.makedirs(self.output_dir, exist_ok=True)
        self.env_path = config_settings.env_path
        self.blog_id = os.getenv('KICKSERVE_BLOG_ID')
        self.html_file = 'news_response.html'
        self.generator = NewsContentGenerator(self.env_path, self.blog_id, html_file=self.html_file)

    def run(self):
        st.markdown(
            """
            <style>
            .block-container {
                padding-top: 1rem;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.title('Kickserve News Generator')
        tabs = st.tabs(["News Generator", "Social Media Summary"])
        with tabs[0]:
            st.write('Enter your initial query and generate a news article.')
            initial_query = st.text_area('Initial Query', value=config_settings.initial_query, height=200)
            generate = st.button('Generate Content')
            md_file_path = os.path.join(self.output_dir, 'news_response.md')
            md_content = ''
            if generate:
                blog_prompt_long = f"""You are a news editor. Review the initial query: "{initial_query}"
    Read each row's Title and body into one article. Synergize into a summary, 
    capturing the most interesting points relevant to the initial_query.
    Begin the article with a compelling lead that hooks the reader in ten words or less.
    Present the summary as a short news article with 3-4 bullet points followed 
    by a "300" - "400" word summary.
    This should written in English (American). 
    The summary should be concise and engaging, suitable for a sports news article.
    """
                news_prompt = self.generator.build_news_prompt(blog_prompt_long)
                try:
                    response = self.generator.generate_content(news_prompt)
                    st.success('Content generated!')
                except errors.ServerError as e:
                    st.error(f"The content generation service returned an error. This is usually temporary. Please try again in a few moments.\n\nDetails: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
            # Load the markdown file if it exists
            if os.path.exists(md_file_path):
                with open(md_file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
            st.subheader('Edit Markdown Content')
            edited_md = st.text_area('Markdown Content', value=md_content, height=400)
            save_as_new = st.button('Save as New Markdown File')
            if save_as_new:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                new_md_file = os.path.join(self.output_dir, f'news_response_{timestamp}.md')
                with open(new_md_file, 'w', encoding='utf-8') as f:
                    f.write(edited_md)
                file_uri = f'file:///{new_md_file.replace(os.path.sep, "/")}'
                st.markdown(f'Saved as [{new_md_file}]({file_uri})')
            # Add publish button
            publish_html_file = os.path.join(self.output_dir, self.html_file)
            publish = st.button('Publish to Blogger')
            if publish:
                # Save the current markdown to file before publishing
                with open(md_file_path, 'w', encoding='utf-8') as f:
                    f.write(edited_md)
                # Re-render HTML from markdown
                self.generator.render_html_response()
                # Call publish_news_response.py as a subprocess
                import subprocess
                import sys
                result = subprocess.run([
                    sys.executable,
                    os.path.join('src', 'publish_news_response.py'),
                    '--file', publish_html_file
                ], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success('Published to Blogger!')
                else:
                    st.error(f'Publish failed: {result.stderr}')
        with tabs[1]:
            st.write('Generate a short summary for social media (BlueSky, etc).')
            # Load the markdown file if it exists
            md_file_path = os.path.join(self.output_dir, 'news_response.md')
            md_content = ''
            if os.path.exists(md_file_path):
                with open(md_file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
            st.text_area('Current Markdown Content', value=md_content, height=200, disabled=True)
            st.subheader('Short Social Media Summary')
            # Option to generate a short summary
            if st.button('Generate Social Media Summary'):
                # For now, just take the first 200 characters as a placeholder
                short_summary = md_content[:200] + ('...' if len(md_content) > 200 else '')
                st.session_state['short_summary'] = short_summary
            short_summary = st.session_state.get('short_summary', '')
            edited_short_summary = st.text_area('Summary to Post', value=short_summary, height=100)
            if st.button('Post to BlueSky'):
                handle = os.getenv("BLUESKY_HANDLE")
                password = os.getenv("BLUESKY_PASSWORD")
                if not handle or not password:
                    st.error("BlueSky handle or password not found in environment variables.")
                else:
                    success, message = Publisher.post_to_bluesky(edited_short_summary, handle, password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            st.write('You can copy this summary to post on BlueSky or other social media.')

def main():
    app = StreamlitNewsApp()
    app.run()

if __name__ == '__main__':
    main()
