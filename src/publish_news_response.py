# publish_news_response.py
"""
A script to publish the generated news_response.html to the blog using bloggerUtils.create_blogger_post.
"""
import dotenv 

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_settings

#import config_settings from one folder up
from config_settings import blog_prompt_long
from config_settings import env_path
dotenv.load_dotenv(env_path)


dotenv.load_dotenv(env_path)
blog_id = os.getenv('JRYLE_BLOG_ID')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bloggerUtils import BloggerUtils



class Publisher:
    def __init__(self, html_file_path, blog_id):
        self.blog_id = blog_id
        self.html_content = self._read_html_file(html_file_path)
        self.title = self._extract_title_from_content()

    def _read_html_file(self, html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _extract_title_from_content(self):
        import re
        # Search for the first H1 or H2 tag within the provided HTML content
        # The content might start with <style>...</style> then <div...><h1/2>...
        title_match = re.search(r"<h[12][^>]*>(.*?)</h[12]>", self.html_content, re.IGNORECASE | re.DOTALL)
        if title_match:
            title_text = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() # Remove any inner HTML tags from title
            return title_text if title_text else "News Update"
        return "News Update" # Fallback title

    def publish(self):
        from src.bloggerUtils import BloggerUtils
        blogger_utils = BloggerUtils()
        blogger_utils.create_blogger_post(self.blog_id, self.title, self.html_content)
        print(f"Published blog post: {self.title}")

    def post_to_bluesky(self, handle, app_password):
        """
        Post the blog title and a link to the blog post to BlueSky.
        Requires the bsky-sdk or requests library and BlueSky app password authentication.
        """
        import requests
        post_text = f"{self.title} - Read more: https://kicksrv.blogspot.com/"
        session = requests.Session()
        resp = session.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": handle, "password": app_password}
        )
        if resp.status_code != 200:
            print("BlueSky login failed:", resp.text)
            return False
        access_jwt = resp.json().get("accessJwt")
        headers = {"Authorization": f"Bearer {access_jwt}"}
        post_resp = session.post(
            "https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers=headers,
            json={
                "repo": handle,
                "collection": "app.bsky.feed.post",
                "record": {
                    "$type": "app.bsky.feed.post",
                    "text": post_text
                }
            }
        )
        if post_resp.status_code == 200:
            print("Posted to BlueSky!")
            return True
        else:
            print("Failed to post to BlueSky:", post_resp.text)
            return False

    def post_to_threads(self, username, password):
        """
        Post the blog title and a link to the blog post to Threads.
        There is no official Threads API as of May 2025. This is a placeholder for future implementation.
        """
        print("Threads API is not officially available. Please use the Threads app to post manually:")
        print(f"{self.title} - Read more: https://kicksrv.blogspot.com/")
        return False

# Example usage:
if __name__ == "__main__":
    print("This script is intended to be used as a module.")
    print("To publish content, run GenerateContent.py, which will then use this Publisher class.")
    NEWS_HTML_PATH = "news_response.html" # No longer directly used by Publisher like this
    # # To test Publisher directly, you'd need to provide sample blogger_content:
    # # sample_content = "<style>.my{color:red;}</style><div class='my'><h1>Test</h1><p>Content</p></div>"
    publisher = Publisher(NEWS_HTML_PATH, blog_id)
    publisher.publish()
