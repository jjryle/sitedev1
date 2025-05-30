# config_settings.py
env_path = "C:\\Users\\johnj\\secure_configs\\AgenticResearch\\.env"


initial_query = """What big AI news stories have happened in the last 24 hours?
This is a request for a summary of the latest AI news, focusing on significant developments, breakthroughs, or events in the field of artificial intelligence that have occurred within the last day. The summary should highlight key points and provide insights into the implications of these stories for the AI community and the general public.
The summary should be concise, informative, and engaging, suitable for readers who want to stay updated on the latest trends and advancements in AI.    
Talk about leading companies such as OpenAI, Nvidia, Google, Microsoft, Anthropic and Meta, and their latest AI developments. 
"""


min_length = 300
max_length = 400

blog_prompt_long = f"""You are a news editor. Review the initial query: "{initial_query}"
    Read each row's Title and body into one article. Synergize into a summary, 
    capturing the most interesting points relevant to the initial_query.
    Present the summary as a short news article with 3-4 bullet points followed 
    by a "{min_length}" - "{max_length}" word summary.
    This should written in English (American). 
    The summary should be concise and engaging, suitable for a news article.
    
    
"""

print(blog_prompt_long)

