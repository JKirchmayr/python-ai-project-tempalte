from agents import Agent, Runner, WebSearchTool
from retrieval_functions import company_search, investor_search, CompanySearchContext
from pydantic import BaseModel
from typing import Optional, List

# ---------------------------------------------------------------------
# Step 1: Define output data models
# ---------------------------------------------------------------------

class CompanyResult(BaseModel):
    name: str # Required
    description: str # Required
    website: Optional[str]
    headquarters_location: Optional[str]
    employee_count: Optional[int]
    industry: Optional[str]
    year_founded: Optional[int]
    revenue: Optional[str]

class CompanySearchResponse(BaseModel):
    message: str  # Required message from the agent
    companies: List[CompanyResult]

class InvestorResult(BaseModel):
    name: str  # Required
    website: Optional[str] = None
    headquarters_location: Optional[str] = None
    employee_count: Optional[int] = None
    industry_focus: Optional[List[str]] = None
    year_founded: Optional[int] = None

class InvestorSearchResponse(BaseModel):
    message: str  # Required message from the agent
    investors: List[InvestorResult]    

# ---------------------------------------------------------------------
# Step 2: Define agents
# ---------------------------------------------------------------------

# Specialized agents for specific tasks
company_search_agent = Agent(
    name="Company Finder",
    handoff_description="Specialist agent for company search",
    instructions="""
    You are responsible for searching companies from a database or verified sources. 
    You will only respond with company data retrieved from the database using the company_search function. 
    You should never generate generic or unverified responses. 
    If required fields like company_description or country are missing, ask the user for clarification before proceeding. 
    Your response should only contain company search results based on database queries.
    """,
    tools=[company_search],
    output_type=CompanySearchResponse
)

investor_search_agent = Agent(
    name="Investor Finder",
    handoff_description="Specialist agent for investor search",
    instructions="You provide assistance with investor search. Ask follow-up questions if needed. Once you have completed your search, explain search method and results clearly.",
    tools=[investor_search],
    output_type=InvestorSearchResponse
)

research_agent = Agent(
    name="Web Research Agent",
    handoff_description="Specialist agent for web research",
    instructions="You provide help with web research. Retrieve information from the web and provide a summary of the results in a clear and concise manner.",
    tools=[WebSearchTool()]
)

# Orchestrator agent that dynamically routes tasks to the best agent
orchestrator_agent = Agent(
    name="Orchestrator Assistant", 
    instructions="""
    You are a task orchestrator. Your job is to identify the correct specialized agent to handle each user query. 
    You must route tasks to the appropriate agent (e.g., Company Search Agent or Investor Search Agent) if required.
    If the user asks a generic question unrelated to companies or investors, you should use the web research agent to find the answer.
    If there is missing context, prompt the user to provide it before routing to the responsible agent.
    """,
    handoffs=[company_search_agent, investor_search_agent],
    tools=[
         research_agent.as_tool(
            tool_name="search_the_web",
            tool_description="Search the web for information",          
         ),
           ]
)

async def main():
    result = await Runner.run(orchestrator_agent, "Show me a list of companies active in the healthcare industry")
    print(result.final_output)

await main()


# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.