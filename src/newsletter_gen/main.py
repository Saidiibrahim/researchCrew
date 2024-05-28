#!/usr/bin/env python
from newsletter_gen.crew import NewsletterGenCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    NewsletterGenCrew().crew().kickoff(inputs=inputs)