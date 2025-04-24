import os
import json
import uuid
import httpx
from typing import Tuple


langgraph_url = os.getenv("LANGGRAPH_URL", "http://localhost:8123")


async def create_thread(user_id: str) -> dict:
    """Create a new thread for the given user."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{langgraph_url}/threads",
                json={
                    "thread_id": str(uuid.uuid4()),
                    "metadata": {
                        "user_id": user_id
                    },
                    "if_exists": "do_nothing"
                }
            )
            response.raise_for_status()

            return response.json()
    except Exception as e:
        print(f"Request failed: {e}")
        raise


async def get_thread_state(thread_id: str) -> dict:
    """Get the state of the thread."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{langgraph_url}/threads/{thread_id}/state"
            )
            response.raise_for_status()

            return response.json()
    except Exception as e:
        print(f"Request failed: {e}")
        raise


def process_line(line: str, current_event: str) -> str:
    """Process a single data line from the streaming response."""
    try:
        # Process data lines
        if line.startswith("data: "):
            data_content = line[6:]

            if current_event == "messages":
                message_chunk, metadata = json.loads(data_content)
            
                if "type" in message_chunk and message_chunk["type"] == "AIMessageChunk":
                    return message_chunk['content']
                        
                if "tool_calls" in message_chunk:
                    if message_chunk["tool_calls"] and message_chunk["tool_calls"][0]["name"]:
                        tool_name = message_chunk["tool_calls"][0]["name"]
                        tool_args = message_chunk["tool_calls"][0]["args"]

                        tool_call_str = f"\n\n[ TOOL CALL: {tool_name} ]"
                        for arg, value in tool_args.items():
                            tool_call_str += f"\n<{arg}>: \n{value}\n\n"
                        return tool_call_str
                
                # You can handle other event types here
                
            elif current_event == "metadata":
                return

    except Exception as e:
        print(f"Error processing line: {type(e).__name__}: {str(e)}")
        raise


async def get_stream(thread_id: str, message: str):
    """Send a message to the thread and process the streaming response.

    Args:
        thread_id: The thread ID to send the message to
        message: The message content

    Returns:
        str: The complete response from the assistant
    """
    full_content = ""
    current_event = None

    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                url=f"{langgraph_url}/threads/{thread_id}/runs/stream",
                json={
                    "assistant_id": "scout",
                    "input": {
                        "messages": [
                            {"role": "human", "content": message}
                        ]
                    },
                    "stream_mode": "messages-tuple"
                },
                timeout=100.0 # increased timeout to allow Render spin up time
            ) as stream_response:
                async for line in stream_response.aiter_lines():
                    if line:
                        # Process event lines
                        if line.startswith("event: "):
                            current_event = line[7:].strip()

                        # Process data lines
                        else:
                            message_chunk = process_line(line, current_event)
                            if message_chunk:
                                full_content += message_chunk
                                print(message_chunk, end="", flush=True)

        return full_content
    except Exception as e:
        print(f"Error in get_stream: {type(e).__name__}: {str(e)}")
        raise


async def main():
    try:
        # Create a thread
        response = await create_thread(user_id="kenny")
        thread_id = response["thread_id"]

        current_chart = None
        # Stream responses
        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            print(f"\n---- User ---- \n\n{user_input}\n")

            print(f"---- Assistant ---- \n")
            # Get the response using our simplified get_stream function
            result = await get_stream(thread_id, user_input)

            # check state after run
            thread_state = await get_thread_state(thread_id)

            if "chart_json" in thread_state["values"]:
                chart_json = thread_state["values"]["chart_json"]
                if chart_json and chart_json != current_chart:
                    # render any charts generated
                    import plotly.io as pio
                    fig = pio.from_json(chart_json)
                    fig.show()

                    current_chart = chart_json
            print("")

    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise


if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()

    print("\n###\n\nGreetings!\n\nTry asking Scout a question about the company data.\n\n###\n\n")

    asyncio.run(main())


