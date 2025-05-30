# %%
3 + 2
# %%
import GenerateContent
from GenerateContent import NewsContentGenerator

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_settings
env_path = config_settings.env_path

dotenv.load_dotenv(env_path)
blog_id = os.getenv('JRYLE_BLOG_ID')


news_content_generator = NewsContentGenerator(env_path, blog_id)

get_content = news_content_generator.generate_content()



# %%
from publish_news_response import Publisher
from datetime import datetime   
import os
import dotenv

gen_content = GenerateContent()
#get_content = gen_content.get_news_response()

# %%


env_path = "C:\\Users\\johnj\\secure_configs\\AgenticResearch\\.env"
dotenv.load_dotenv(env_path)
BLOG_ID = os.getenv('JRYLE_BLOG_ID')

# %%




# %%
NEWS_HTML_PATH = "news_response.html"
publisher = Publisher(NEWS_HTML_PATH, BLOG_ID)
publisher.publish()

# %%
