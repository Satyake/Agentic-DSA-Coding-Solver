from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os 
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
model_client=OpenAIChatCompletionClient(model="gpt-4o", api_key=api_key)
problem_solver_agent=AssistantAgent(
    name="DSASolverAgent",
    model_client=model_client,
    system_message="""   You are a overall problem solver agent, that is an expert in solving DSA problems in Python,
    Your working with your fellow code executor agent, 
    you can generate code outputs for the code executor agent to run,
    you write code to solve the task, your colde will be in python, which the code executor agent can run,
    at the beginning of response, specify your plan to solve the task ,
    then you should give the code in a single code block that you can pass to the code executor agent.
    Once the code is executed, you have to make sure the output is correct.

    In the end once the code is executed successfully, you have to stay "TERMINATE"

      """                
)
