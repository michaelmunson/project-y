import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

class Agent:
  def __init__(self, system:str):
    self.api_key = os.getenv("ANTHROPIC_API_KEY")
    self.client = Anthropic(api_key=self.api_key)
    self.system = system
  
  
