from typing_extensions import TypedDict
from agents import function_tool, RunContextWrapper
from pydantic import BaseModel
from typing import Optional

# Define the structure for a company
class Company(TypedDict):
    description: str
    name: str
    industry: str
    country: str
    employee_count: int

# TODO: Implement context management  
class CompanySearchContext(BaseModel):
    company_description: str = None   # Required
    country: str = None   # Required
    name: Optional[str] = None
    website: Optional[str] = None
    revenue: Optional[str] = None
    industry: Optional[str] = None

class Investor(TypedDict):
    name: str
    focus_sector: str
    headquarters: str
    aum_millions: int  # Assets under management in millions

# Define the function tool for company search
@function_tool
async def company_search() -> list[Company]:
    """Search for companies and return example data."""
    # Check if description and country are missing
    #if not wrapper.context.description or not wrapper.context.country:
    #    return ["Missing required fields: description and/or country"]
    
    # Proceed with search if context is complete    
    # TODO: Implement actual search logic here
    return [
        Company(name="TechCorp", industry="Technology", location="San Francisco", employee_count=500),
        Company(name="HealthInc", industry="Healthcare", location="New York", employee_count=200),
        Company(name="EduGlobal", industry="Education", location="London", employee_count=150),
    ]


@function_tool
async def investor_search() -> list[Investor]:
    """Search for investors and return example data."""
        # TODO: Implement actual search logic here
    return [
        Investor(name="CapitalX Partners", focus_sector="Technology", headquarters="San Francisco, CA", aum_millions=1500),
        Investor(name="HealthVest Ventures", focus_sector="Healthcare", headquarters="Boston, MA", aum_millions=800),
        Investor(name="EduGrowth Capital", focus_sector="Education", headquarters="London, UK", aum_millions=500),
    ]