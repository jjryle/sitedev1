# publish_news_response.py
"""
A script to publish the generated news_response.html to the blog using bloggerUtils.create_blogger_post.
"""
import dotenv 
import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_settings

#import config_settings from one folder up
from config_settings import blog_prompt_long
from config_settings import env_path
dotenv.load_dotenv(env_path)


dotenv.load_dotenv(env_path)
blog_id = os.getenv('KICKSERVE_BLOG_ID')

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
        print(f"[DEBUG] blog_id: {self.blog_id}")
        print(f"[DEBUG] title: {self.title}")
        print(f"[DEBUG] html_content (first 200 chars): {self.html_content[:200]}")
        blogger_utils = BloggerUtils()
        blogger_utils.create_blogger_post(self.blog_id, self.title, self.html_content)
        print(f"Published blog post: {self.title}")

    @staticmethod
    def post_to_bluesky(post_text, handle, app_password):
        """
        Post the given text to BlueSky.
        Requires the requests library and BlueSky app password authentication.
        """
        import requests
        session = requests.Session()
        try:
            resp = session.post(
                "https://bsky.social/xrpc/com.atproto.server.createSession",
                json={"identifier": handle, "password": app_password},
                timeout=10
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"BlueSky login failed: {e}")
            return False, f"BlueSky login failed: {e}"

        session_data = resp.json()
        access_jwt = session_data.get("accessJwt")

        post_record = {
            "$type": "app.bsky.feed.post",
            "text": post_text,
            "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        headers = {"Authorization": f"Bearer {access_jwt}"}
        try:
            post_resp = session.post(
                "https://bsky.social/xrpc/com.atproto.repo.createRecord",
                headers=headers,
                json={
                    "repo": session_data.get("handle"),
                    "collection": "app.bsky.feed.post",
                    "record": post_record,
                },
                timeout=10
            )
            post_resp.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to post to BlueSky: {e}")
            return False, f"Failed to post to BlueSky: {e}"

        print("Posted to BlueSky!")
        return True, "Posted to BlueSky!"

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
    import argparse
    print("This script is intended to be used as a module.")
    print("To publish content, run GenerateContent.py, which will then use this Publisher class.")
    parser = argparse.ArgumentParser(description="Publish a Blogger HTML file.")
    parser.add_argument('--file', type=str, default=r"C:\AppAdmin\kickserve\news_response.html", help='Path to the HTML file to publish')
    args = parser.parse_args()
    NEWS_HTML_PATH = args.file
    # # To test Publisher directly, you'd need to provide sample blogger_content:
    # # sample_content = "<style>.my{color:red;}</style><div class='my'><h1>Test</h1><p>Content</p></div>"
    publish_blog_id = os.getenv('KICKSERVE_BLOG_ID')
    if not publish_blog_id:
        raise ValueError("KICKSERVE_BLOG_ID environment variable is not set.")  
    publisher = Publisher(NEWS_HTML_PATH, blog_id)
    publisher.publish()
