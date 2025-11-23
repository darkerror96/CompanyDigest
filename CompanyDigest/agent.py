from google.adk.agents import ParallelAgent, SequentialAgent
from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search

from CompanyDigest.tools import (
    get_google_news_about_company,
    get_yahoo_finance_data_about_company,
)

ticker_finder_agent = Agent(
    name="ticker_finder_agent",
    model="gemini-2.5-flash-lite",
    description="Finds the correct stock ticker symbol for any company using Google Search built-in tool calls.",
    instruction="""
    You are the Ticker Finder Agent. Your job is to determine the correct stock ticker symbol for any publicly traded company using the Google Search built-in tool call.
    
	INSTRUCTIONS:
	
	1. When the user provides a company name:
	   - Use the Google Search API tool call with a short, targeted query:
	     Example: “<company name> stock ticker” OR “<company name> ticker symbol”.
	   - Read the search results and extract the correct ticker.
	   - Validate that the ticker is accurate and corresponds to a public company.
	
	2. Output Format:
	   Return all results in this EXACT format: "Company Name = X and Company Ticker Symbol = Y"
	
	3. Rules:
	   - Do NOT guess ticker symbols.
	   - If multiple companies match the search, list all of them with short differences.
	   - If no ticker exists (private company, subsidiary, etc.), clearly state that.
	   - Keep responses concise and factual.
	   - Only use information gathered from the search tool results.
	
	4. Helper logic:
	   - If Google Search returns a Knowledge Panel, extract the ticker from it.
	   - If Yahoo Finance or MarketWatch appears in results, prioritize those pages.
	   - Never rely on memory; always use search tool call per query.""",
    tools=[google_search],
    output_key="ticker_data",
)


yahoo_finance_agent = Agent(
    name="yahoo_finance_agent",
    model="gemini-2.5-flash-lite",
    description="Fetches structured financial data, fundamentals, and market metrics from Yahoo Finance.",
    instruction="""
    You are the Yahoo Finance Agent. Your job is to invoke `get_yahoo_finance_data_about_company(ticker_symbol)` function to fetch the real-time finance info of the company.
	
	You have access to below function:
	
	* `get_yahoo_finance_data_about_company(ticker_symbol)`: Retrieves finance data about the company based on company ticker symbol.    
    
    INSTRUCTIONS:
    
    - Make sure to invoke the `get_yahoo_finance_data_about_company(ticker_symbol)` function.
    - Extract company ticker symbol from {ticker_data} and pass as input parameter value to `get_yahoo_finance_data_about_company(ticker_symbol)` function.
    - DO NOT make up random news on your own.
    """,
    tools=[get_yahoo_finance_data_about_company],
    output_key="financial_data",
)


google_search_agent = Agent(
    name="google_search_agent",
    model="gemini-2.5-flash-lite",
    description="Performs Google search queries and extracts the most relevant, trustworthy information.",
    instruction="""
    You are the Google Search Agent. Your role is to execute Google searches and extract the top verified, high-quality information for the company.
    
    Company Information: {ticker_data}
    
    INSTRUCTIONS:
    
    - Summaries must be factual, concise, and organized.
    - Exclude ads, SEO spam, irrelevant blog content, or low-credibility sources.
    - Return results as short bullet points. Do not hallucinate or infer content that is not found from search results.""",
    tools=[google_search],
    output_key="search_data",
)

google_news_agent = Agent(
    name="google_news_agent",
    model="gemini-2.5-flash-lite",
    description="Retrieves the most recent and relevant news about a company from Google News API",
    instruction="""
    You are the Google News Agent. Your job is to invoke `get_google_news_about_company(company_name)` function to fetch the latest news stories for the company.
    
    You have access to below function:
	
	* `get_google_news_about_company(company_name)`: Retrieves google news about the company based on company name.    
	
    INSTRUCTIONS:
    
    - Make sure to invoke the `get_google_news_about_company(company_name)` function.
    - Extract company name from {ticker_data} and pass as input parameter value to `get_google_news_about_company(company_name)` function.
    - DO NOT make up random news on your own.""",
    tools=[get_google_news_about_company],
    output_key="news_data",
)

data_aggregator_agent = Agent(
    name="data_aggregator_agent",
    model="gemini-2.5-flash-lite",
    instruction="""Combine these three collected company information into a single concise summary:

    **Financial Data:**
    {financial_data}

    **Google Search Data:**
    {search_data}

    **Google News Data:**
    {news_data}

    Do NOT create new information. You must only synthesize what the other agents provided.
    
    Organize the final output into these sections unless otherwise requested:
		- Company Snapshot
	    - Financial Highlights
	    - Recent News & Events
	    - Future Outlook Based on Verified Info Only

    Your tone must be analytical, neutral, and easy to understand. The final summary should be around 200 words.""",
    output_key="final_summary",
)

data_collector_team = ParallelAgent(
    name="data_collector_team",
    sub_agents=[yahoo_finance_agent, google_search_agent, google_news_agent],
)

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[ticker_finder_agent, data_collector_team, data_aggregator_agent],
)


session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent, app_name="CompanyDigest", session_service=session_service
)
