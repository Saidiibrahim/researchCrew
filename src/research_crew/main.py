#!/usr/bin/env python
from research_crew.crew import ResearchCrew

def load_html_template():
    with open('src/research_crew/config/research_template.html', 'r') as file:
        html_template = file.read()
    return html_template


def main():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': input("Enter the topic for your research: "),
        'personal_message': input("Enter your personal message: "),
        'html_template': load_html_template(),
    }
    ResearchCrew().crew().kickoff(inputs=inputs)


if __name__ == '__main__':
    main()

