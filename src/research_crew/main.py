#!/usr/bin/env python
from research_crew.crew import ResearchCrew


def main():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    ResearchCrew().crew().kickoff(inputs=inputs)


if __name__ == '__main__':
    main()

