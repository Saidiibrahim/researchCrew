# 🐨 Research Crew

Welcome to the Research Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a GUI for a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. The framework used for the GUI is [Streamlit](https://streamlit.io/).

Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

## Cloning the Repository

To get started with the Research Crew project, you first need to clone the repository from GitHub.
Open your terminal and run the following command:

```bash
git clone https://github.com/Saidiibrahim/researchCrew.git
```

This will create a local copy of the repository on your machine.

## Setting Up

After cloning the repository, navigate into the project directory and install the dependencies using Poetry:

```bash
cd research-crew
poetry install
```

This will set up a virtual environment and install all required dependencies.

## Usage

To run the application, run the following command from the project directory:

```bash
streamlit run src/frontend/app.py
```

This start the streamlit app and you can interact with the application.

## Project Structure

```text
research-crew/
├── .venv/
├── cookbook/
├── docs/
├── src/
│   ├── frontend/
│   ├── research_crew/
│   │   ├── config/
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── crew.py
│   │   │   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── poetry.lock
├── pyproject.toml
└── README.md
```

- `src/research_crew/`: Contains the core logic and configuration for the research crew.
- `src/frontend/`: Contains the Streamlit app and UI components.
- `src/research_crew/config/`: Configuration files for the research crew.
- `src/research_crew/crew.py`: The main file that initializes the crew and assigns tasks to agents.
- `src/research_crew/main.py`: The main file that runs the crew and handles the execution of tasks.

## Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/research_crew/config/agents.yaml` to define your agents
- Modify `src/research_crew/config/tasks.yaml` to define your tasks
- Modify `src/research_crew/crew.py` to add your own logic, tools and specific args
- Modify `src/research_crew/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run research_crew
```

This command initializes the research_crew Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The research_crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Contributing

Everyone is welcome to contribute to the Research Crew project! Please open an issue or submit a pull request with your changes.

Let's create wonders together with the power and simplicity of crewAI.
