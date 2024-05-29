#!/usr/bin/env python
from newsletter_gen.crew import NewsletterGenCrew


def main():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    NewsletterGenCrew().crew().kickoff(inputs=inputs)


if __name__ == '__main__':
    main()

