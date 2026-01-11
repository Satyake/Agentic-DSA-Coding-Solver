import asyncio
import streamlit as st

from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

from problemsolver import problem_solver_agent


def _run_async(coro):
    """
    Streamlit runs scripts top-to-bottom; this helper runs async code safely.
    """
    try:
        return asyncio.run(coro)
    except RuntimeError:
        # Fallback if an event loop is already running in the environment
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


async def run_team_stream(problem: str, max_turns: int = 10):
    docker = DockerCommandLineCodeExecutor(work_dir="/tmp", timeout=120)
    code_executor_agent = CodeExecutorAgent(
        name="CodeExecAgent",
        code_executor=docker,
    )

    termination = TextMentionTermination("TERMINATE")

    team = RoundRobinGroupChat(
        [problem_solver_agent, code_executor_agent],
        termination_condition=termination,
        max_turns=max_turns,
    )

    await docker.start()
    try:
        async for message in team.run_stream(task=problem):
            if isinstance(message, TextMessage):
                yield f"**{message.source}:**\n\n{message.content}"
            elif isinstance(message, TaskResult):
                yield f"✅ **Stop reason:** {message.stop_reason}"
            else:
                # In case other message types appear (tool calls/results, etc.)
                src = getattr(message, "source", type(message).__name__)
                content = getattr(message, "content", repr(message))
                yield f"**{src}:**\n\n{content}"
    finally:
        await docker.stop()


def main():
    st.set_page_config(page_title="AlgoGenie", layout="wide")

    st.title("AlgoGenie — Agentic DSA Problem Solver [LOCAL]")
    st.write(
        "Ask a DSA problem. The problem-solver agent will generate a solution and the Docker executor will run code locally."
    )

    problem = st.text_area(
        "Enter your DSA problem",
        height=180,
        placeholder="Example: Write Python code to calculate the average of 10 random numbers.",
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        run_btn = st.button("Run", type="primary")
    with col2:
        max_turns = st.slider("Max turns", min_value=2, max_value=30, value=10, step=1)

    st.divider()
    output = st.container()

    if run_btn:
        if not problem.strip():
            st.warning("Please enter a problem first.")
            return

        with output:
            st.subheader("Live output")
            placeholder = st.empty()
            log_lines = []

            async def _runner():
                async for line in run_team_stream(problem=problem.strip(), max_turns=max_turns):
                    log_lines.append(line)
                    # Render progressively
                    placeholder.markdown("\n\n---\n\n".join(log_lines))

            with st.spinner("Running..."):
                _run_async(_runner())


if __name__ == "__main__":
    main()
