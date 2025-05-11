#!/usr/bin/env python3
import asyncio
import os
import anthropic

from dotenv import load_dotenv
import json
load_dotenv()
import mcp

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from contextlib import AsyncExitStack


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: ClientSession|None = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, command: str):
        cmd, args = command.split(" ", 1)
        server_params = StdioServerParameters(
            command=cmd,
            args=args.split(" "),
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])



async def main():
    client = MCPClient()
    await client.connect_to_server("docker run -i --rm --init -e DOCKER_CONTAINER=true mcp/puppeteer")

    input("Press Enter to continue...")
    # api_key = os.getenv("ANTHROPIC_API_KEY")
    # if not api_key:
    #     print("Error: set ANTHROPIC_API_KEY")
    #     return

    # client = anthropic.Client(api_key=api_key)

    # print("Chat with Claude (type 'exit' or 'quit' to end)\n")
    # while True:
    #     user = input("You: ")
    #     if user.lower() in ("exit", "quit"):
    #         break

    #     prompt = f"{anthropic.HUMAN_PROMPT}{user}{anthropic.AI_PROMPT}"
    #     resp = client.completions.create(
    #         model="claude-2",
    #         prompt=prompt,
    #         max_tokens_to_sample=500,
    #     )
    #     print("Claude:", resp.completion.strip(), "\n")

if __name__ == "__main__":
    asyncio.run(main())
