import pytest
from research_crew.tools.search import SearchTool

def test_search_tool():
    tool = SearchTool()
    result = tool._run("test query", limit=1)
    assert "Search results for test query:" in result
    # assert "https://www.example.com" in result  # Assuming this URL is part of the mocked response