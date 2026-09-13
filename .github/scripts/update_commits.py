import urllib.request
import json
import re

repos = [
    {
        "name": "solomonrajan.github.io",
        "icon": "🌐",
        "description": "A hobby personal website *(Current working repo)*",
        "url": "https://github.com/solomonrajan/solomonrajan.github.io"
    },
    {
        "name": "solomonrajan",
        "icon": "👤",
        "description": "GitHub Profile Readme",
        "url": "https://github.com/solomonrajan/solomonrajan"
    }
]

def fetch_latest_commit(repo_name):
    url = f"https://api.github.com/repos/solomonrajan/{repo_name}/commits"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0:
                commit = data[0]
                sha = commit['sha'][:7]
                msg = commit['commit']['message'].split('\n')[0]
                # truncate long messages
                if len(msg) > 50:
                    msg = msg[:47] + '...'
                return sha, msg
    except Exception as e:
        print(f"Error fetching data for {repo_name}: {e}")
    return None, None

def generate_table():
    lines = [
        "| 📁 Repository | 📝 Description | 🚀 Latest Commit |",
        "| :--- | :--- | :--- |"
    ]
    
    for repo in repos:
        sha, msg = fetch_latest_commit(repo['name'])
        if sha and msg:
            commit_link = f"[{sha}]({repo['url']}/commit/{sha})"
            badge = f"[![Last Commit](https://img.shields.io/github/last-commit/solomonrajan/{repo['name']}?style=flat-square&color=2ea44f)]({repo['url']}/commits/main)"
            msg_clean = msg.replace('|', '-') # prevent markdown table break
            
            repo_cell = f"{repo['icon']} **[{repo['name']}]({repo['url']})**"
            desc_cell = repo['description']
            commit_cell = f"`{sha}` - {msg_clean}<br/>{badge}"
            
            lines.append(f"| {repo_cell} | {desc_cell} | {commit_cell} |")
        else:
            # Fallback
            repo_cell = f"{repo['icon']} **[{repo['name']}]({repo['url']})**"
            desc_cell = repo['description']
            badge = f"[![Last Commit](https://img.shields.io/github/last-commit/solomonrajan/{repo['name']}?style=flat-square&color=2ea44f)]({repo['url']}/commits/main)"
            lines.append(f"| {repo_cell} | {desc_cell} | {badge} |")
            
    return "\n".join(lines)

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
        
    table_content = generate_table()
    
    pattern = r'(<!-- START_COMMIT_TABLE -->\n)(.*?)(\n<!-- END_COMMIT_TABLE -->)'
    replacement = f"\\1{table_content}\\3"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    update_readme()
