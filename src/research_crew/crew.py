from crewai import Agent, Crew, Process, Task
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool
)
from langchain_community.agent_toolkits import FileManagementToolkit
from research_crew.tools.search import SearchTool
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
import streamlit as st
from typing import Union, List, Tuple, Dict
from langchain_core.agents import AgentFinish
import json
from dotenv import load_dotenv
import os
from langsmith.run_helpers import traceable

load_dotenv()

my_openai_key = os.getenv("OPENAI_API_KEY")
my_serper_key = os.getenv("SERPAPI_API_KEY")
my_langchain_key = os.getenv("LANGCHAIN_API_KEY")

WORKING_DIRECTORY = "/Users/ibrahimsaidi/Desktop/Builds/crewAIBuilds/researchCrew/docs"

# Instantiate tools
docs_tool = DirectoryReadTool("./docs")
file_tool = FileReadTool("./docs")
search_tool = SearchTool()

tools = FileManagementToolkit(
    root_dir=WORKING_DIRECTORY,
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()
read_tool, write_tool, list_tool = tools

@CrewBase
class ResearchCrew():
	"""Research crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	
	def llm(self):
		llm = ChatOpenAI(
			model_name='gpt-4',
			api_key=my_openai_key
		)
		return llm
	
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
			tools=[search_tool], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=self.llm(),
			step_callback=lambda step: self.step_callback(step, "Research Agent")
		)
	
	
	@agent
	def editor(self) -> Agent:
		return Agent(
			config=self.agents_config['editor'],
			verbose=True,
			tools=[read_tool, write_tool],
			llm=self.llm(),
			step_callback=lambda step: self.step_callback(step, "Chief Editor")
		)
	
	
	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			tools = [read_tool, write_tool],
			verbose=True,
			llm=self.llm(),
			step_callback=lambda step: self.step_callback(step, "HTML Writer")
		)

	
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher(),
			output_file='./docs/research_report.md'
		)

	@task
	def edit_task(self) -> Task:
		return Task(
			config=self.tasks_config['edit_task'],
			agent=self.editor(),
			output_file='./docs/edited_report.md'
		)
	
	@task
	def newsletter_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.writer(),
			output_file='./docs/research_report.html'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research crew"""
		return Crew(
			agents=[self.researcher(), self.editor(), self.writer()], # Automatically created by the @agent decorator
			tasks=[self.research_task(), self.edit_task(), self.newsletter_task()], # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)