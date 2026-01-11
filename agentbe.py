from autogen_agentchat.agents import CodeExecutorAgent
import asyncio
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from problemsolver import problem_solver_agent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
import streamlit as st


async def main():
    docker=DockerCommandLineCodeExecutor(
        work_dir="/tmp",
        timeout=120
    )
    code_executor_agent=CodeExecutorAgent(
        name="CodeExecAgebnt",
        code_executor=docker
    )
    task=TextMessage(
        content="""Here is some code
        ```python
print('Hello world docker')```
        """, source="user"
    )

    #problem_solver_agent=problem_solver_agent
    termination=TextMentionTermination('TERMINATE')

    team=RoundRobinGroupChat([problem_solver_agent, code_executor_agent],
    termination_condition=termination,
    max_turns=10)




    await docker.start()
    try:

        task=""" Write a python code to calculate average of 10 random numbers"""
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print('=='*20)
                print(message.source,':',message.content)
            elif isinstance(message, TaskResult):
                print("Stop Reason",message.stop_reason)
        result=await code_executor_agent.on_messages(
            messages=[task],
            cancellation_token=CancellationToken()
        )
        print(result.chat_message.content)

    except Exception as e:
        print(f"Error {e}")
    finally:
        print("Stopping Container")
        await docker.stop()
if __name__=="__main__":
    asyncio.run(main())
