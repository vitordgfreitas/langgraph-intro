from onlyvans.graph import agent


config = {
    "configurable": {
        "thread_id": "test_thread"
    }
}


# Inspect the graph
agent.inspect_graph()


# Run by invoking
response = agent.invoke("Who are the top 5 creators by revenue?", config=config)
response


# Stream a response 
for chunk in agent.stream("Who are the top 3 customers by total amount spent?", config=config):
    print(chunk, end="", flush=True)


# Test the memory saver
for chunk in agent.stream("Show me the SQL you used to answer the last question", config=config):
    print(chunk, end="", flush=True)
