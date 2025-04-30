from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4.1-mini-2025-04-14")

llm.invoke("Hello world!")




# State - Keeps track of interactions with the agent
state: dict = {
    "messages": [],
}


# Nodes - functions that do some work and then update the state
def assistant_node(state: dict) -> dict:
    """Assistant"""
    response = llm.invoke(["Choose one: <tool>, <end>"])
    state["messages"] += [f"Assistant: Okay, let's route to {response.content}!"]
    return state


def tool_node(state: dict) -> dict:
    """Executes a tool and appends the result as a Tool Message"""
    state["messages"] += ["Successfully executed tool! \n\n<RESULT>\n\n"]
    return state


# In Langgraph, all agent interactions start with passing in an intial state
intial_state = {
    "messages": ["Hola, I'm the user. Help me with..."]
}

assistant_node(intial_state)



# Edges - functions with logic defining how we move from one node to another. Edges do NOT modify the state.

# Normal Edge - Directly routes from one node to another

# Conditional Edge - Has logic to determine which node to route to next, based on some condition
def assistant_conditional_edge(state: dict) -> str:
    """Assistant conditional edge
    
    Edges do not modify the state, they only return a string name of the next node to run.
    """
    last_message = state["messages"][-1]
    if "<tool>" in last_message:
        return "tool_node"
    else:
        return "end"
    


my_state = {
    "messages": ["Hola, I'm the user. Help me with..."]
}


my_state = assistant_node(my_state)
next_node = assistant_conditional_edge(my_state)
if next_node == "tool_node":
    my_state = tool_node(my_state)
elif next_node == "end":
    print("END OF GRAPH RUN")



my_state