#!/usr/bin/env python3
import asyncio
import os
import anthropic
from typing import Any
from dotenv import load_dotenv
import json
load_dotenv()
import mcp

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from contextlib import AsyncExitStack


class Tool:
    """Represents a tool with its properties and formatting."""

    def __init__(
        self, name: str, description: str, input_schema: dict[str, Any]
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.input_schema: dict[str, Any] = input_schema

    def format_for_llm(self) -> str:
        """Format tool information for LLM.

        Returns:
            A formatted string describing the tool.
        """
        args_desc = []
        if "properties" in self.input_schema:
            for param_name, param_info in self.input_schema["properties"].items():
                arg_desc = (
                    f"- {param_name}: {param_info.get('description', 'No description')}"
                )
                if param_name in self.input_schema.get("required", []):
                    arg_desc += " (required)"
                args_desc.append(arg_desc)

        return f"""
Tool: {self.name}
Description: {self.description}
Arguments:
{chr(10).join(args_desc)}
"""

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
        self.tools = [Tool(tool.name, tool.description, tool.inputSchema) for tool in response.tools]
        self.toolbox = set([tool.name for tool in self.tools])
        print("\nConnected to server with tools:", [tool.name for tool in self.tools])


    async def execute_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        return await self.session.call_tool(tool_name, arguments)


async def main():
    client = MCPClient()
    await client.connect_to_server("docker run -i --rm --init -e DOCKER_CONTAINER=true mcp/puppeteer")

    import sys
    user_prompt = sys.argv[1]

    tools_description = "\n".join([tool.format_for_llm() for tool in client.tools])

    system_message = (
        "You are a helpful assistant with access to these tools:\n\n"
        f"{tools_description}\n"
        "Choose the appropriate tool based on the user's question. "
        "If no tool is needed, reply directly.\n\n"
        "IMPORTANT: When you need to use a tool, you must ONLY respond with "
        "the exact JSON object format below, nothing else:\n"
        "{\n"
        '    "tool": "tool-name",\n'
        '    "arguments": {\n'
        '        "argument-name": "value"\n'
        "    }\n"
        "}\n\n"
        "After receiving a tool's response:\n"
        "1. Transform the raw data into a natural, conversational response\n"
        "2. Keep responses concise but informative\n"
        "3. Focus on the most relevant information\n"
        "4. Use appropriate context from the user's question\n"
        "5. Avoid simply repeating the raw data\n\n"
        "Please use only the tools that are explicitly defined above."
    )

    messages = [{"role": "user", "content": user_prompt}, {"role": "assistant", "content": "{"}]

    # Start conversation with Claude
    claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    while True:
        message = claude.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=3000,
            # thinking={
            #     "type": "enabled",
            #     "budget_tokens": 32000
            # },
            messages=messages,
            system=system_message
        )
        msg_txt = message.content[0].text.strip()
        msg_txt = '{' + msg_txt if not msg_txt.startswith('{') else msg_txt
        print('LLM response:')
        print(message.content[0].text)
        messages.append({"role": "assistant", "content": msg_txt})

        try:
            tool_call = json.loads(msg_txt)
            tool_name = tool_call["tool"]
            tool_args = tool_call["arguments"]
            result = await client.execute_tool(tool_name, tool_args)
            print(f'Tool response: {result}')
            if result is not None:
                for content in result.content:
                    if content.type == "text":
                        messages.append({"role": "user", "content": content.text})
                    elif content.type == "image_url":
                        messages.append({"role": "user", "content": content.image_url.url})
                    else:
                        messages.append({"role": "user", "content": f"Tool response: {content}"})
        except Exception as e:
            print(f"Error: {e}")
            messages.append({"role": "user", "content": f"Error: {e}"})
        
        messages.append({"role": "assistant", "content": "{"})

        import pdb; pdb.set_trace()





if __name__ == "__main__":
    asyncio.run(main())
