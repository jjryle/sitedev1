import os
import glob
import datetime
from GenerateContent import NewsContentGenerator

# Set up paths and environment
output_dir = r'C:\AppAdmin\kickserve'
env_path = "C:\\Users\\johnj\\secure_configs\\AgenticResearch\\.env"
blog_id = os.getenv('KICKSERVE_BLOG_ID')
html_file = 'news_response.html'

# Find the most recently modified .md file
md_files = glob.glob(os.path.join(output_dir, '*.md'))
if not md_files:
    raise FileNotFoundError("No markdown files found in output directory.")
latest_md = max(md_files, key=os.path.getmtime)

# Read the markdown content
with open(latest_md, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Overwrite the main .md file (so the HTML generator uses it)
main_md_path = os.path.join(output_dir, 'news_response.md')
with open(main_md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

# Generate HTML from the markdown
generator = NewsContentGenerator(env_path, blog_id, html_file=html_file)
generator.render_html_response()

# Publish using the existing publish_news_response.py script
import subprocess
html_path = os.path.join(output_dir, html_file)
result = subprocess.run([
    'python',
    os.path.join('src', 'publish_news_response.py'),
    '--file', html_path
], capture_output=True, text=True)

if result.returncode == 0:
    print('Published to Blogger!')
else:
    print(f'Publish failed: {result.stderr}')