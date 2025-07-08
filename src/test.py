# %%
import dotenv

import GenerateContent
from GenerateContent import NewsContentGenerator

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_settings
env_path = config_settings.env_path

dotenv.load_dotenv(env_path)
blog_id = os.getenv('KICKSERVE_BLOG_ID')
# %%

# ...existing code...
news_content_generator = NewsContentGenerator(env_path, blog_id)

# Build the news prompt using your config_settings
news_prompt = news_content_generator.build_news_prompt(config_settings.initial_query)

# Pass the prompt to generate_content
get_content = news_content_generator.generate_content(news_prompt)
# ...existing code...
#get_content = news_content_generator.generate_content(news_prompt)



# %%
from publish_news_response import Publisher
from datetime import datetime   
import os
import dotenv

news_prompt = news_content_generator.build_news_prompt(config_settings.initial_query)

gen_content = GenerateContent(news_prompt, env_path, blog_id)
#get_content = gen_content.get_news_response()

# %%


env_path = "C:\\Users\\johnj\\secure_configs\\AgenticResearch\\.env"
dotenv.load_dotenv(env_path)
BLOG_ID = os.getenv('KICKSERVE_BLOG_ID')

# %%

import ftplib
# %%
ftp = ftplib.FTP()
#ftp.connect("6.tcp.ngrok.io", 13008)
ftp.connect("kick-serve.com", 13008)
ftp.login("jryle", "alskdjf^%&$2930u42prj")



# %%
NEWS_HTML_PATH = "news_response.html"
publisher = Publisher(NEWS_HTML_PATH, BLOG_ID)
publisher.publish()

# %%
