from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import CodeInterpreterTool

class SimpleAgent:
  def __init__(self, project_client: AIProjectClient, model: str, agent_id: str = None):
    self.project_client = project_client
    self.model = model
    self.name = "simpe-agent-01"
    self.agent_id = agent_id
    self.agent = None

  def __create_agent(self):
    instructions = (
        "You are a friendly AI Agent that uses emojis to communicate."
        "Your capabilities are simple and your answers must be short and concise."
    )
    
    agent = self.project_client.agents.create_agent(
        model=self.model,
        name=self.name,
        instructions=instructions,
    )

    return agent
    

  def init_agent(self):
    if self.agent_id is not None:
      self.agent = self.project_client.agents.get_agent(self.agent_id)

    if self.agent is None:
      self.agent = self.__create_agent()

    self.thread = self.project_client.agents.threads.create()
    # TODO: Add logger
    #print(f"Created thread with ID: {thread.id}")

  
  def run_agent(self, message):
    if not self.agent:
      raise ValueError("Agent is not initialized. Call init_agent() first.")

    _ = self.project_client.agents.messages.create(
      thread_id=self.thread.id,
      role="user",
      content=message
    )

    response = self.project_client.agents.runs.create_and_process(
      thread_id=self.thread.id,
      agent_id=self.agent.agent_id
    )

    messages = self.project_client.agents.messages.list(
      thread_id=self.thread.id
    )

    messages = list(messages)
    
    msg = {
      "role": messages[0]["role"],
      "content": messages[0]["content"][0]["text"]["value"]
    }

    return msg
