from crewai import Agent, Crew, Process, Task
from langchain_anthropic import ChatAnthropic
from research_crew.tools.research import SearchAndContents, FindSimilar, GetContents
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
from utils.callback import step_callback

load_dotenv()

# Instantiate tools here

@CrewBase
class ResearchCrew():
	"""Research crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	
	def llm(self, model_name: str, model_provider: str = "openai"):
		if model_provider == "openai":
			openai_api_key = os.getenv("OPENAI_API_KEY")
			if not openai_api_key:
				raise ValueError("OPENAI_API_KEY not found in environment variables")
			return ChatOpenAI(
				model=model_name, 
				api_key=openai_api_key,
			)
		elif model_provider == "anthropic":
			anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
			if not anthropic_api_key:
				raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
			return ChatAnthropic(
				model_name=model_name, 
				api_key=os.getenv("ANTHROPIC_API_KEY"),
				max_tokens = 4096,
			)
		else:
			raise ValueError(f"Invalid model provider: {model_provider}")
	
	callback = step_callback
	
	
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[SearchAndContents(), FindSimilar(), GetContents()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=self.llm(model_provider="openai", model_name="gpt-4-turbo"),
			step_callback=lambda step: self.callback(step, "Research Agent")
		)
	
	
	@agent
	def editor(self) -> Agent:
		return Agent(
			config=self.agents_config['editor'],
			verbose=True,
			tools=[SearchAndContents(), FindSimilar(), GetContents()],
			llm=self.llm(model_provider="openai", model_name="gpt-4-turbo"),
			step_callback=lambda step: self.callback(step, "Chief Editor")
		)
	
	@agent
	def designer(self) -> Agent:
		return Agent(
			config=self.agents_config['designer'],
			# tools = [read_tool, write_tool],
			verbose=True,
			allow_delegation=False,
			llm=self.llm(model_provider="openai", model_name="gpt-4-turbo"),
			step_callback=lambda step: self.callback(step, "HTML Writer")
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