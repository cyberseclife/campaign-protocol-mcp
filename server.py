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

@mcp.tool()
def generate_strategy_reply(user_problem: str, author_name: str, technical_insight: str, proposed_solution: str, project_tag: str = None):
    """
    Generates a helpful reply. Only mentions a project if a relevant tag is provided.
    Otherwise, provides a pure 'Help-First' technical response.
    """
    persona = get_persona()
    company = persona.get("brand_name", "CyberSecLife Development")
    projects = persona.get("projects", [])

    # Try to find a project that actually matches the technical context
    selected_project = next((p for p in projects if project_tag and project_tag in p.get('tag', '')), None)

    intro = f"@{author_name} saw you were hitting a wall with {user_problem[:50]}..."

    # Logic Gate: If we have a matching project, mention it. If not, don't lie.
    if selected_project:
        body = (
            f"We ran into this exact behavior at **{company}** while building {selected_project['name']}. "
            f"It's a known pain point when {selected_project['description']}."
        )
        cta = f"We handled the implementation details here if it helps your research: {selected_project['url']}"
    else:
        # PURE HELP MODE: No advertising, just building brand authority through expertise
        body = (
            f"I've been looking into similar {technical_insight} issues recently. "
            "It usually stems from the way the host environment handles async cleanup cycles."
        )
        cta = f"Hope the solution below helps get this cleared up!"

    help_section = f"**Head-on Solution:**\n{proposed_solution}"

    return f"{intro}\n\n{body}\n\n{help_section}\n\n{cta}"

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
