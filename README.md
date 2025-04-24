# LangGraph Intro

This project gives a brief introduction to LangGraph by using it to build a simple but powerful data analytics AI agent. It's meant to be a starting point for building your own LangGraph applications. I encourage you to build off of this example to create your own AI agents and expand on the capabilities covered here.

Topics covered:

- What is langgraph and should you use it?
- State management
- Tool usage
- Memory and persistance
- Streaming

## Requirements

- Python 3.12
- Docker
- Supabase account (optional)
- Langsmith account (optional)

## Project Structure

- `onlyvans`: The package containing the agent definition.
    - `graph.py`: The agent definition.
- `sample_data`: The sample data we'll load into our postgresql database.
- `chat.py`: A simple chat interface for testing the agent.
- `app.py`: A simple web server for testing the agent.
- `langgraph.json`: The LangGraph configuration file.
- `.env.sample`: The environment variables used by the agent. This should be copied to `.env` and filled in with your own secrets.

## Setup

### Clone the repo

Clone it to your local machine.

```bash
git clone https://github.com/onlyvans/langgraph-intro.git
```

### Install packages in a virtual environment

The recommended way is to use the package manager uv. This will automatically create a virtual environment and install the packages defined in pyproject.toml. It will also install the onlyvans package in editable mode so any code changes you make will be reflected in the package.

```bash
uv pip install -e .
```

You can also install the packages manually using pip. It's recommended you first create a virtual environment in the project directory.

```bash
pip install -e .
```

### Set up the database

We are using Supabase which offers a generous free tier, for our postgresql database. You can optionally use your own provider and simply change the database URI in the .env file.

1. Create a Supabase account at supabase.com.
2. Create a new project.
3. Create three new tables using the `sample_data` files to define the schema:
    - creators
    - customers
    - transactions
4. Navigate to the Table Editor in the side menu.
5. Import the sample data from the `sample_data` folder.

### Create a Langsmith account (optional)

Langsmith is used for logging and monitoring. This is completely optional but highly recommended as it makes it easy to track and debug your LangGraph applications. You can create a free account at [langsmith.com](https://langsmith.com/).

### Set up the .env file

1. Copy the `.env.sample` file to `.env`.
2. Fill in the environment variables with your own secrets.

### Build the langgraph image


### Run the langgraph server in docker

docker run --env-file .env -p 8123:8000 langgraph-intro