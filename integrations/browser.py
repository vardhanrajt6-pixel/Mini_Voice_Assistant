import webbrowser

def search(query: str):
    if not query:
        return "No search query provided."
    try:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searched for '{query}' in your browser."
    except Exception as e:
        return f"Failed to search the web: {str(e)}"
