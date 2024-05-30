import pytest

def test_import_ResearchCrew():
    try:
        from research_crew.crew import ResearchCrew
        assert True, "Successfully imported ResearchCrew"
    except ImportError as e:
        assert False, f"Failed to import: {str(e)}"

