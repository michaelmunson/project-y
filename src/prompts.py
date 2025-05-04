import os
import json
def create_system_base():
  # Read system_base.md file
  dir_path = os.path.dirname(os.path.realpath(__file__))
  with open(os.path.join(dir_path, "base_prompts/system_base.md"), "r") as f:
    system_base = f.read()
  
  with open(os.path.join(dir_path, "base_prompts/openapi.json"), "r") as f:
    tool_spec = json.load(f)
  # Replace {{tool_spec}} with provided tool_spec
  return system_base.replace("{{tool_spec}}", json.dumps(tool_spec))

def create_message_base(task: str, ticket_list: list[dict]):
  return [
    {
      "role": "user",
      "content": "Here is a list of the current tickets:" + json.dumps(ticket_list)
    },
    {
      "role": "assistant",
      "content": "I understand, what is my task?"
    },
    {
      "role": "user",
      "content": "Your task is as follows:\n\n" + task
    }
  ]
  
def create_prompt(task:str, ticket_list:list[dict]):
  ticket_list = [] if ticket_list is None else ticket_list
  system_base = create_system_base()
  message_base = create_message_base(task, ticket_list)
  return {
    "system": system_base,
    "messages": message_base
  }