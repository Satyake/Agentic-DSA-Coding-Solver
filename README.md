# Project Structure and Logic

This repo hosts a small Autogen-based agent pair: a DSA problem-solver agent and a code-executor agent that runs generated Python in a Docker sandbox.

## Folder Structure

```
E:\Python DSA Master Agentic
|-- DSA Solver Agentic.ipynb
|-- agent-be.py
|-- problemsolver.py
|-- requirements.txt
|-- .env
|-- .gitignore
|-- __init__.py
|-- __pycache__
```

## File-by-File Notes

- `DSA Solver Agentic.ipynb`: Notebook that writes the project files to disk (agent, solver, env, requirements). It captures the same logic as the .py files and can be used to regenerate them.
- `agent-be.py`: Entry point. Builds a Docker-backed `CodeExecutorAgent` and a `RoundRobinGroupChat` with the problem-solver agent. Sends a DSA task prompt and streams responses, then executes generated code.
- `problemsolver.py`: Defines the `DSASolverAgent` using `OpenAIChatCompletionClient` and a system prompt that enforces plan + code block output, with a final `TERMINATE` token.
- `requirements.txt`: Python dependencies for Autogen and OpenAI client usage.
- `.env`: Holds `OPENAI_API_KEY` (kept out of version control).
- `.gitignore`: Ignores `.env` and `__pycache__`.
- `__init__.py`: Marks the folder as a Python package.
- `__pycache__`: Bytecode cache directory (generated).

## Runtime Flow

1. `problemsolver.py` loads `OPENAI_API_KEY`, creates the model client, and instantiates `problem_solver_agent`.
2. `agent-be.py` starts a Docker code executor, then creates a `RoundRobinGroupChat` with the solver and executor agents.
3. The task prompt is sent; messages stream until the termination condition (`TERMINATE`) is reached.
4. The code executor runs the generated Python and prints the final output, then the Docker container stops.

## Notes

- The Docker code executor uses `/tmp` inside the container as its work directory.
- Keep `.env` local and never commit it.

