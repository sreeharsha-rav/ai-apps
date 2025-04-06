import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Optional
from src.prompts.search import SHOULD_USE_WEB_SEARCH, GENERATE_SEARCH_QUERY, SUMMARIZE_WEB_CONTENT
from src.llm.models.base_llm import BaseLLM
from src.schemas.search import SearchEngineID, SearchResult, AISearchResult, WebRAGResponse
from src.schemas.chat import Role, UserMessage, AssistantMessage
from src.search.search_registry import SearchRegistry

class WebRAGService:
    """Web Retrieval-Augmented Generation (RAG) service for handling web searches and content summarization."""

    TRUNCATE_SCRAPED_TEXT: int = 10000      # adjust based on Model's context window
    CHARACTER_LIMIT: int = 1000             # adjust for tokenization considerations

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._search_registry = SearchRegistry()

    async def perform_web_search(self, user_message: UserMessage, llm: BaseLLM, engine_id: SearchEngineID = SearchEngineID.GOOGLE) -> List[SearchResult]:
        """
        Perform a web search using the specified search engine, generate a search query, and return search results.

        Args:
            user_message: The user's message
            llm: The language model instance
            engine_id: The search engine ID to use (defaults to Google)

        Returns:
            List[SearchResult]: A list of search results
        """
        # Generate a web search query
        search_query: AssistantMessage = await llm.get_completion(
            system_instruction=GENERATE_SEARCH_QUERY,
            messages=[user_message]
        )
        self.logger.info(f"Generated search query: {search_query.content}")

        # Get the search engine and fetch results
        search_engine = self._search_registry.get_engine(engine_id)
        search_results: List[SearchResult] = search_engine.search(
            query=search_query.content,
            num_results=5
        )

        self.logger.info(f"Found {len(search_results)} search results")
        return search_results

    async def retrieve_content(self, url: str) -> Optional[str]:
        """
        Retrieve and extract the main content from a web page.

        Args:
            url: The URL of the web page to scrape from SearchResult

        Returns:
            Optional[str]: The extracted text content or None if an error occurs
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove non-content elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()

            # Extract text content
            text = soup.get_text(separator="\n", strip=True)

            # Basic text cleaning
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            content = '\n'.join(lines)

            # Truncate if too long (LLM context window limitations)
            max_content_length = self.TRUNCATE_SCRAPED_TEXT * 4         # 4x the limit to account for tokenization
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."     # add ellipsis to indicate truncation for LLM

            return content
        except Exception as e:
            self.logger.error(f"Error retrieving content from {url}: {str(e)}")
            return None

    async def summarize_content(self, content: str, query: str, llm: BaseLLM) -> str:
        """
        Summarize web page content using the LLM.

        Args:
            content: The content to summarize from `retrieve_content()`
            query: The original search query (not the generated one)
            llm: The language model instance

        Returns:
            str: The summarized content
        """

        # Check if content is empty
        if not content:
            self.logger.warning("No content to summarize.")
            return "No content available for summarization."

        # generate a system prompt for summarization, add query, character limit
        system_prompt = SUMMARIZE_WEB_CONTENT.format(
            search_query=query,
            character_limit=self.CHARACTER_LIMIT,
        )
        self.logger.info(f"System prompt for web content summarization: {system_prompt}")

        # Create a user message with the web content to summarize
        user_message = UserMessage(
            role=Role.USER,
            content=f"search_query: {query}\nweb_page_content:{content}"
        )
        self.logger.info(f"User message for summarization: {user_message.content}")

        # Generate the summary using the LLM
        summary_response: AssistantMessage = await llm.get_completion(
            system_instruction=system_prompt,
            messages=[user_message]
        )

        self.logger.info(f"Summarization response: {summary_response.content}")

        return summary_response.content

    async def build_search_context(self, search_results: List[SearchResult], search_query: str, llm: BaseLLM) -> List[AISearchResult]:
        """
        Build a search context by retrieving and summarizing content from search results.

        Args:
            search_results: List of search results from `perform_web_search()`
            search_query: The original search query (not the generated one)
            llm: The language model instance

        Returns:
            List[AISearchResult]: A list of AI-enhanced search results with summaries
        """
        ai_search_results: List[AISearchResult] = []

        for result in search_results:
            # Retrieve content from the link
            self.logger.info(f"Retrieving content from: {result.link}")
            content = await self.retrieve_content(result.link)

            # create ai_search_result object
            ai_search_result = AISearchResult(
                title=result.title,
                link=result.link,
                snippet=result.snippet,
                summary="",         # placeholder for now
            )

            # get summary of the content if available
            if content:
                self.logger.info(f"Summarizing content for: {result.link}")
                summary = await self.summarize_content(content, search_query, llm)
                ai_search_result.summary = summary

            # add the ai_search_result to the list
            ai_search_results.append(ai_search_result)

        return ai_search_results

    async def execute_web_rag(
            self,
            user_message: UserMessage,
            llm: BaseLLM,
            engine_id: SearchEngineID = SearchEngineID.GOOGLE
    ):
        """
        Execute the Web RAG process: perform web search, retrieve content, and summarize it.

        Args:
            user_message: The user's message
            llm: The language model instance
            engine_id: The search engine ID to use (defaults to Google)

        Returns:
            RAGResponse: A response object containing search results and summaries
        """
        # initialize RAG response
        rag_response = WebRAGResponse(
            search_performed=False,
            search_query=user_message.content,
            search_results=[],
            total_results=0,
            engine_id=engine_id
        )
        self.logger.info(f"Executing Web RAG for query: {user_message.content}")

        # determine if a web search is needed
        should_use_web_search = await llm.get_completion(
            system_instruction=SHOULD_USE_WEB_SEARCH,
            messages=[user_message]
        )
        self.logger.info(f"Should use web search: {should_use_web_search.content}; Content type: {type(should_use_web_search.content)}")

        if should_use_web_search.content == "true":         # currently using string comparison, TODO: improve this to bool data type
            self.logger.info("Performing web search...")

            # perform web search
            search_results: List[SearchResult] = await self.perform_web_search(
                user_message=user_message,
                llm=llm,
                engine_id=engine_id
            )

            # build search context
            ai_search_results: List[AISearchResult] = await self.build_search_context(
                search_results=search_results,
                search_query=user_message.content,
                llm=llm
            )
            self.logger.info(f"AI-enhanced search results: {ai_search_results}")

            # update rag response
            rag_response.search_performed = True
            rag_response.search_results = ai_search_results
            rag_response.total_results = len(search_results)
        else:
            self.logger.info("Web search not needed.")

        return rag_response