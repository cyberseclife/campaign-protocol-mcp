from fastmcp import FastMCP
import requests
import json
import os

# Initialize the Server
mcp = FastMCP("Campaign-Protocol-MCP")

# --- 1. MEMORY (Identity) ---
def get_persona():
    """Loads the brand identity from persona.json"""
    try:
        with open("persona.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "brand_name": "CyberSecLife Development",
            "product_name": "Campaign-Protocol-MCP",
            "github_repo": "https://github.com/YOUR_USERNAME/campaign-protocol-mcp"
        }

# --- 2. THE HUNTER (Search) ---
@mcp.tool()
def search_github_issues(keyword: str, limit: int = 5):
    """
    Searches GitHub for recent issues/discussions containing the keyword.
    Useful for finding people struggling with problems we can solve.
    """
    url = "https://api.github.com/search/issues"
    params = {
        "q": f"{keyword} is:issue is:open",
        "sort": "updated",
        "order": "desc",
        "per_page": limit
    }

    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("html_url"),
                "author": item.get("user", {}).get("login"),
                "body_snippet": item.get("body", "")[:200] + "..."
            })
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error searching GitHub: {str(e)}"

# --- 3. THE STRATEGIST (Writer) ---
@mcp.tool()
def generate_strategy_reply(user_problem: str, author_name: str, technical_insight: str):
    """
    Generates a TAILORED marketing reply.
    technical_insight: The specific fix or observation (e.g., 'Electron beforeQuit race condition').
    """
    persona = get_persona()
    company = persona.get("brand_name", "CyberSecLife Development")
    product = persona.get("product_name", "Campaign-Protocol-MCP")
    link = persona.get("github_repo", "https://github.com/cyberseclife/campaign-protocol-mcp")

    intro = f"@{author_name} saw you were hitting a wall with {user_problem[:50]}..."

    # We use the technical_insight parameter to make it unique and relevant
    body = (
        f"We actually investigated a similar {technical_insight} over at **{company}** "
        f"while stress-testing the {product} lifecycle. It’s a nasty bottleneck, "
        "especially when async cleanup handlers don't signal the parent process correctly."
    )

    cta = f"We documented our signal-handling patterns in the {product} repo if you want to compare notes: {link}"

    return f"{intro}\n\n{body}\n\n{cta}"

@mcp.tool()
def read_issue_details(owner: str, repo: str, issue_number: int):
    """
    Fetches the full body and all comments of a specific GitHub issue.
    Use this to understand the full context before generating a reply.
    """
    # 1. Get the main issue body
    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    # 2. Get the comments
    comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"

    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        issue_res = requests.get(issue_url, headers=headers).json()
        comments_res = requests.get(comments_url, headers=headers).json()

        full_text = f"TITLE: {issue_res.get('title')}\n"
        full_text += f"BODY: {issue_res.get('body')}\n\n"
        full_text += "--- COMMENTS ---\n"

        for c in comments_res:
            full_text += f"{c['user']['login']}: {c['body']}\n\n"

        return full_text
    except Exception as e:
        return f"Error fetching details: {str(e)}"

# --- RUN AS SSE SERVER ---
if __name__ == "__main__":
    # This forces the server to listen on port 8000 instead of stdio
    mcp.run(transport="sse")
