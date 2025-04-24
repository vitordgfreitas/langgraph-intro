# LangGraph Intro

This project gives a brief introduction to LangGraph by using it to build a simple but powerful data analytics AI agent that can query your database, perform analyses, and generate visualizations. It's meant to be a starting point for building your own LangGraph applications. Build off of this example to create your own AI agents, add tools and logic, and expand on the capabilities covered here.

What we'll cover:

1. Building a single node graph.
2. Add tool usage.
3. Add state management.
4. Add streaming.
5. Add memory and persistance.
6. Deploy the agent.

Concepts discussed:

- What is langgraph and should you use it?
- Overview of LangGraph library and ecosystem
- Langsmith tracing
- State management
- Tool usage
- Streaming
- Memory and persistance
- Agent deployment

## Requirements

- Python 3.12
- Docker
- Supabase account (optional for persistance and deployment)
- Langsmith account (optional for tracing)
- Render account (optional for deployment)

## Project Structure

- `onlyvans`: The package containing the agent definition.
- `sample_data`: The sample data we'll load into our postgresql database.
- `chat.py`: A simple test chat to test the agent in the local environment.
- `app.py`: A simple command-line "frontend" for testing the deployed agent.
- `langgraph.json`: The LangGraph configuration file where we specify the agent graph to expose via the API.
- `.env.sample`: The environment variables required to run the project. This should be copied to `.env` and filled in with your own secrets.

## Setup

Only steps 1 through 3 are required to get the agent up and running. Steps 4-7 are optional if you want to build a fully-deployed agent.

### 1. Clone the repo

Clone it to your local machine.

```bash
git clone https://github.com/onlyvans/langgraph-intro.git
```

### 2. Install packages in a virtual environment

The recommended way is to use the package manager uv. This will automatically create a virtual environment and install the packages defined in pyproject.toml. It will also install the onlyvans package in editable mode so any code changes you make will be reflected in the package.

```bash
uv pip install -e .
```

You can also install the packages manually using pip. It's recommended you first create a virtual environment in the project directory.

```bash
pip install -e .
```

### 3. Set up the .env file

1. Copy the `.env.sample` file to `.env`.
2. Fill in the environment variables with your own secrets.

### 4. Set up the database (optional)

We are using Supabase which offers a generous free tier, for our postgresql database. You can optionally use your own provider and simply change the database URI in the .env file.

1. Create a Supabase account at supabase.com.
2. Create a new project.
3. Create three new tables using the `sample_data` files to define the schema:
    - creators
    - customers
    - transactions
4. Navigate to the Table Editor in the side menu.
5. Import the sample data from the `sample_data` folder.

### 5. Create a Langsmith account (optional)

Langsmith is used for logging and monitoring. This is completely optional but highly recommended as it makes it easy to track and debug your LangGraph applications. You can create a free account at [langsmith.com](https://langsmith.com/).

## Deployment

### 1. Build the langgraph image

```bash
langgraph build -t langgraph-intro
```

### 2. Run the langgraph server in docker

docker run --env-file .env -p 8123:8000 langgraph-intro
