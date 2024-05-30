import requests
import json
import os
from crewai_tools import tool
from crewai_tools import BaseTool

class SearchTool(BaseTool):
    name : str = "search_google"
    description : str = "Use this tool to search the internet for information."

    def _run(self, query: str, limit: int = 5) -> str:
        url = "https://google.serper.dev/search"
        payload = json.dumps({
        "q": query,
        "num": limit
        })
        headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()['organic']
        string = []
        for result in results:
            string.append(f"{result['title']}\n{result['snippet']}\n{result['link']}\n\n")
        return f"Search results for {query}:\n\n" + "\n".join(string)

