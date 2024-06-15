from crewai import Agent, Crew, Process, Task
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool
)
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_anthropic import ChatAnthropic
from research_crew.tools.search import SearchTool
from research_crew.tools.research import SearchAndContents, FindSimilar, GetContents
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
import streamlit as st
from typing import Union, List, Tuple, Dict
from langchain_core.agents import AgentFinish
import json
from dotenv import load_dotenv
import os
from datetime import datetime
from langsmith.run_helpers import traceable

load_dotenv()

# WORKING_DIRECTORY = "/Users/ibrahimsaidi/Desktop/Builds/crewAIBuilds/researchCrew/docs"

# Instantiate tools
docs_tool = DirectoryReadTool("./docs")
file_tool = FileReadTool("./docs")
search_tool = SearchTool()

@CrewBase
class ResearchCrew():
	"""Research crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	
	def llm(self, model_name: str, model_provider: str = "openai"):
		if model_provider == "openai":
			return ChatOpenAI(
				model=model_name, 
				api_key=os.getenv("OPENAI_API_KEY"),
			)
		elif model_provider == "anthropic":
			return ChatAnthropic(
				model_name=model_name, 
				api_key=os.getenv("ANTHROPIC_API_KEY"),
				max_tokens = 4096,
			)
		else:
			raise ValueError(f"Invalid model provider: {model_provider}")
	
	#TODO: Abstract this to a class in a utils file
	def step_callback(
        self,
        agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish],
        agent_name,
        *args,):
		with st.chat_message("AI"):
		# Try to parse the output if it is a JSON string
			if isinstance(agent_output, str):
				try:
					agent_output = json.loads(agent_output)
				except json.JSONDecodeError:
					pass

			if isinstance(agent_output, list) and all(
				isinstance(item, tuple) for item in agent_output
			):

				for action, description in agent_output:
					# Print attributes based on assumed structure
					st.write(f"Agent Name: {agent_name}")
					st.write(f"Tool used: {getattr(action, 'tool', 'Unknown')}")
					st.write(f"Tool input: {getattr(action, 'tool_input', 'Unknown')}")
					st.write(f"{getattr(action, 'log', 'Unknown')}")
					with st.expander("Show observation"):
						st.markdown(f"Observation\n\n{description}")

			# Check if the output is a dictionary as in the second case
			elif isinstance(agent_output, AgentFinish):
				st.write(f"Agent Name: {agent_name}")
				output = agent_output.return_values
				st.write(f"I finished my task:\n{output['output']}")

			# Handle unexpected formats
			else:
				st.write(type(agent_output))
				st.write(agent_output)

	
	
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[SearchAndContents(), FindSimilar(), GetContents()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=self.llm(model_provider="openai", model_name="gpt-4-turbo"),
			step_callback=lambda step: self.step_callback(step, "Research Agent")
		)
	
	
	@agent
	def editor(self) -> Agent:
		return Agent(
			config=self.agents_config['editor'],
			verbose=True,
			tools=[SearchAndContents(), FindSimilar(), GetContents()],
			llm=self.llm(model_provider="openai", model_name="gpt-4-turbo"),
			step_callback=lambda step: self.step_callback(step, "Chief Editor")
		)
	
	
	@agent
	def designer(self) -> Agent:
		return Agent(
			config=self.agents_config['designer'],
			# tools = [read_tool, write_tool],
			verbose=True,
			allow_delegation=False,
			llm=self.llm(model_provider="openai", model_name="gpt-4-turbo"),
			step_callback=lambda step: self.step_callback(step, "HTML Writer")
		)

	
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher(),
			output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_research_task.md"
		)

	@task
	def edit_task(self) -> Task:
		return Task(
			config=self.tasks_config['edit_task'],
			agent=self.editor(),
			output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_edit_task.md"
		)
	
	@task
	def newsletter_task(self) -> Task:
		return Task(
			config=self.tasks_config['newsletter_task'],
			agent=self.designer(),
			output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_newsletter_task.html"
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research crew"""
		return Crew(
			agents=[self.researcher(), self.editor(), self.designer()], # Automatically created by the @agent decorator
			tasks=[self.research_task(), self.edit_task(), self.newsletter_task()], # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)