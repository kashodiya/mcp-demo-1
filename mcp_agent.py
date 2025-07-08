# Internal FR - Source Code
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
# import ollama
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
import random
import string
import json

checkpointer = InMemorySaver() 



def generate_random_string(length: int) -> str:
    # Define the characters that can be used in the random string
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate a random string of the specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string

class MCPAgent:
    def __init__(self):
        # This is quick and simple
        self.model_name = "qwen2.5:7b" 

        # This is very verbose and explains you how it got the answer
        # self.model_name = "llama3:70b" 

        # This is very verbose and explains you how it got the answer
        # self.model_name = "qwen3:14b" 

        # self.model_name = "qwen2.5vl:7b" 
        # self.model_name = "qwen2.5-coder:7b-instruct" 
        # self.model_name = "mistral:latest" 
        # self.model_name = "gemma3:12b" 
        # self.model_name = "gemma3:4b" 
        self.client = None
        self.agent = None
        self.config = {
            "configurable": {
                "thread_id": "1"  
            }
        }


    async def initialize(self):

        config_mcp_server_file_path = 'config_mcp_server.json'

        # Read the JSON file as a string
        with open(config_mcp_server_file_path, 'r') as file:
            # config_mcp_server_config = file.read()
            config_mcp_server_config = json.load(file)


        self.client = MultiServerMCPClient(config_mcp_server_config)

    #    async with client.session(server_name) as session:
    #        tools = await load_mcp_tools(session)

        # await self.client.__aenter__()
        print("*** Getting tools:")
        tools = await self.client.get_tools()
        print(f"*** Found tools: {len(tools)}")
        for tool in tools:
            print(tool.name)        

        ollama_model = ChatOllama(model=self.model_name)  # Replace with your model name

        self.agent = create_react_agent(
            model=ollama_model,
            tools=tools,
            checkpointer=checkpointer
        )        
        print("*** Agent created")

    async def cleanup(self):
        if self.client:
            await self.client.__aexit__(None, None, None)

    def new_chat(self):
        new_id = generate_random_string(25)
        self.config["configurable"]["thread_id"] = new_id
        print(f"New thread id: {new_id}")
        return new_id

    async def question(self, message):
        print(f"Asking: {message}")

        test_response = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": message}]},
            self.config
        )
        return test_response

# Example usage
async def main():
    agent = MCPAgent()
    await agent.initialize()
    response = await agent.question("List roles")
    print(response)
    await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
    # pass