# config_settings.py
env_path = "C:\\Users\\johnj\\secure_configs\\AgenticResearch\\.env"


initial_query = """Preview tomorrow's french open women's final tennis match between Coco Gauff and Aryna Sabalenka.
Provide a detailed analysis of their recent performances, head-to-head statistics, and any relevant news leading up to the match.
Analyze their playing styles, strengths, and weaknesses, and predict the potential outcome of the match.
What are the betting odds for this match, and how do they reflect the players' current form?
Talk about potential impact of the match in the race for WTA #1 ranking.
"""


initial_query_prior = """Preview today's semifinal tennis match between Novak Djokovic and Jannik Sinner.
Provide a detailed analysis of their recent performances, head-to-head statistics, and any relevant news leading up to the match.
Analyze their playing styles, strengths, and weaknesses, and predict the potential outcome of the match.
What are the betting odds for this match, and how do they reflect the players' current form?
Talk about potential matchups with either Carlos Alcaraz and Lorenzo Musetti in the final.
"""



min_length = 300
max_length = 400

blog_prompt_long = f"""You are a news editor. Review the initial query: "{initial_query}"
    Read each row's Title and body into one article. Synergize into a summary, 
    capturing the most interesting points relevant to the initial_query.
    Begin the article with a compelling lead that hooks the reader in ten words or less.
    Present the summary as a short news article with 3-4 bullet points followed 
    by a "{min_length}" - "{max_length}" word summary.
    This should written in English (American). 
    The summary should be concise and engaging, suitable for a sports news article.
    
    
"""

print(blog_prompt_long)

