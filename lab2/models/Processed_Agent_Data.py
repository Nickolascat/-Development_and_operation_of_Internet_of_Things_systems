from datetime import datetime
from pydantic import BaseModel, field_validator
from models.Agent_Data import AgentData

class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData
