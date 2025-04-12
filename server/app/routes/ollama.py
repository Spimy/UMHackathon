from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
import logging
from pydantic import BaseModel
import httpx
from pydantic_ai import Agent, RunContext
from typing import List, Union, Optional
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import json
import crud
from models import SessionDep

# Configure logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter(tags=["ollama"])

FASTAPI_URL = "http://localhost:8000"

available_APIs = [
    {
        "function": "get_merchant_transactions_summary",
        "description": "Retrieve a summary of transactions for a specific merchant, including frequency and total value of items sold.",
        "arguments": {"session": "SessionDep", "merchant_id": "str"}
    },
    {
        "function": "read_items_by_merchant",
        "description": "Retrieve items associated with a specific merchant.",
        "arguments": {"merchant_id": "str", "session": "SessionDep"}
    }
]


class Prompt(BaseModel):
    prompt: str
    merchant_id: Optional[str] = None
    chat_id: Optional[int] = None


class Item(BaseModel):
    '''Define Result Model'''
    id: int | None = None
    name: str
    description: str
    price: float


ollama_model = OpenAIModel(
    model_name='mistral', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)


async def get_chat_history(session: SessionDep, chat_id: Optional[int]) -> str:
    """Get the chat history for context"""
    if not chat_id:
        return ""

    messages = crud.get_chat_messages(session, chat_id)
    history = []
    for msg in messages:
        role = "User" if msg.is_sent else "Assistant"
        history.append(f"{role}: {msg.text}")

    return "\n".join(history)


async def generate_stream(agent, prompt: Prompt, session: Optional[SessionDep] = None):
    # Get chat history for context if chat_id is provided
    context = ""
    if session and prompt.chat_id:
        context = await get_chat_history(session, prompt.chat_id)
        if context:
            context = f"Previous conversation:\n{context}\n\nCurrent message: {prompt.prompt}"

    # Use context if available, otherwise just the prompt
    input_text = context if context else prompt.prompt
    async with agent.run_stream(input_text) as result:
        async for text in result.stream(debounce_by=0.01):
            yield text.strip()


async def translate_prompt(prompt: Prompt, target_language='en'):
    url = "https://translate.spimy.dev/translate"
    headers = {"Content-Type": "application/json"}
    data = {
        "q": f"{prompt.prompt}",
        "source": "auto",
        "target": f"{target_language}",
        "format": "text",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response_json = response.json()
            prompt.prompt = response_json.get("translatedText", "")
        except httpx.RequestError as e:
            print(f"Translation failed: {e}")

    return prompt


async def search_or_not(prompt: Prompt):
    category_agent = Agent(
        model=ollama_model,
        system_prompt=(
            '''You are a categorization agent that MUST ONLY return responses in the following JSON format:
            {
                "category": [0, 1, or 2],
                "reasoning": "explanation for the category choice"
            }

            RULES:
            1. You MUST categorize ALL inquiries into one of these categories:
            - Category 1: Inventory/graph related inquiries (requires GET_items API)
            - Category 2: Transaction related inquiries (requires GET_transactions API)
            - Category 0: General conversation/greetings

            2. You MUST return valid JSON for EVERY response
            3. You MUST provide reasoning for your category choice
            4. You MUST check available APIs before categorizing

            Examples of valid responses:
            User: "Hello"
            Response: {"category": 0, "reasoning": "General greeting, no API needed"}

            User: "Do you sell ice cream?"
            Response: {"category": 1, "reasoning": "Inventory inquiry, requires GET_items API call"}
            
            User: "What are the sales today?"
            Response: {"category": 2, "reasoning": "Inventory inquiry, requires GET_transactions API call"}

            Remember: ALWAYS return response in valid JSON format with category and reasoning fields.
            ''' + f"\nAvailable APIs: {available_APIs}"
        ),
        deps_type=None,
        result_type=str,
    )

    result = await category_agent.run(prompt.prompt)
    result = json.loads(result.data)
    print("category: " + str(result["category"]
                             ) + " reasoning: " + result["reasoning"])
    return result['category']

chatbot_agent = Agent(
    model=ollama_model,
    system_prompt=(
        '''
        You are a polite and professional assistant designed to handle simple, everyday questions and reject queries that are outside the scope of this system. Your primary responsibilities are:

        1. **Handle Simple Questions**: Respond politely and concisely to basic greetings or mundane questions such as "Hello," "How are you?" or "What can you do?" For example:
            - User: "Hello"
              Assistant: "Hello! How can I assist you today?"
            - User: "How are you?"
              Assistant: "I'm just a program, but I'm here to help!"

        2. **Reject Out-of-Scope Questions**: If the user asks a question that is unrelated to the system's purpose (e.g., inventory management or supported tasks), respond with: "I am unable to assist with that." Do not provide any additional information, commentary, or context. For example:
            - User: "What is Steins;Gate?"
              Assistant: "I am unable to assist with that."
            - User: "Can you explain quantum physics?"
              Assistant: "I am unable to assist with that."

        3. **Do Not Use Pre-Trained Knowledge**: Completely ignore any pre-trained knowledge you may have about topics outside the scope of this system. If the user asks about something unrelated, respond with: "I am unable to assist with that," and stop. Do not provide any additional information, even if you know the answer.

        4. **No Speculative or Fabricated Information**: If the user asks a question that cannot be answered based on the system's purpose or context, respond with: "I am unable to assist with that." Do not add any guesses, commentary, or speculative statements.

        5. **No Self-Explanations**: Do not explain your role, limitations, or purpose. Simply respond to the user's query in a concise and professional manner. For example:
            - User: "What can you do?"
              Assistant: "I can assist with simple questions or let you know if I cannot help with something."
            - User: "Hello"
              Assistant: "Hello! How can I assist you today?"

        6. **Be Friendly and Professional**: Maintain a polite and professional tone in all responses.

        7. **Examples**:
            - User: "What is the current stock of Item A?"
              Assistant: "I am unable to assist with that."
            - User: "What items are available in the inventory?"
              Assistant: "I am unable to assist with that."
            - User: "Hello"
              Assistant: "Hello! How can I assist you today?"
            - User: "What is Steins;Gate?"
              Assistant: "I am unable to assist with that."

        Always ensure that your responses are accurate, concise, and professional. If you do not have enough information or the query is outside your scope, respond with "I am unable to assist with that" and stop. Do not attempt to provide speculative or fabricated information or ask for additional context.
        '''
    ),
    deps_type=None,
    result_type=str,
)

item_agent = Agent(
    model=ollama_model,
    name="Inventory_Agent",
    system_prompt=(
        '''
        You are a data-driven AI agent that MUST ONLY respond with information obtained from API calls.

        CRITICAL RULES:
        1. You MUST call the available API tools for EVERY response
        2. You MUST ONLY respond with data returned from the API calls
        3. If the API call fails or returns no data, respond with 'No data available'
        4. NEVER generate, assume, or make up any information
        5. NEVER provide additional commentary or explanations
        6. Format your responses as direct data presentations

        Examples:
        - User: 'What items are available?'
        Response: [List exact items from API response]
        - User: 'Do we have item X?'
        Response: [Yes/No based on API data only]

        If you cannot get data from an API call, respond ONLY with: 'No data available'
        This is a zero-tolerance policy for generated content - use API data or say 'No data available'
        '''
    ),
    deps_type=None,
    result_type=str,
)

transaction_agent = Agent(
    model=ollama_model,
    name="Transaction_Agent",
    system_prompt=(
        '''
        You are a categorization agent that MUST ONLY return responses in the following JSON format:
        {
            "data_point": "frequency" or "total_value",
            "time": "today" or "this_week" or "this_month"
        }

        CRITICAL RULES:
        1. For data_point:
           - Use "frequency" for queries about number of sales, count, quantity, or how many
           - Use "total_value" for queries about revenue, earnings, money, or sales value
        
        2. For time:
           - Use "today" for queries about today, current day, now
           - Use "this_week" for queries about this week, weekly, past 7 days
           - Use "this_month" for queries about this month, monthly, past 30 days
           - Default to "today" if no time specified

        Examples:
        User: "How many sales today?"
        Response: {"data_point": "frequency", "time": "today"}

        User: "Show me this week's revenue"
        Response: {"data_point": "total_value", "time": "this_week"}

        User: "What's the total earnings this month?"
        Response: {"data_point": "total_value", "time": "this_month"}

        User: "Show me sales data"
        Response: {"data_point": "frequency", "time": "today"}

        ALWAYS return valid JSON with exactly these two fields.
        NEVER add additional fields or explanations.
        '''
    ),
    deps_type=None,
    result_type=str,
)


class MerchantContext(BaseModel):
    merchant_id: str


@item_agent.tool
async def GET_items(ctx: RunContext[MerchantContext]) -> Union[str, List[Item]]:
    url = f'{FASTAPI_URL}/merchants/{ctx.deps.merchant_id}/items'
    print('spimy-url: ' + url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        items_data = response.json()
        transformed_items = [
            Item(
                name=item.get("item_name"),
                description=item.get(
                    "cuisine_tag", "No description available"),
                price=item.get("item_price")
            )
            for item in items_data
        ]
        return transformed_items
    else:
        return 'Failed to fetch items from API'


review_agent = Agent(
    model=ollama_model,
    name="Review_Agent",
    system_prompt=(
        '''
        You are an AI agent that can that summarizes how a merchant is doing based on user reviews within 50 words.
        Emphasize on the positive and negative aspects of the reviews, especially on the pricing, environment, customer service and the food quality.
        '''
    ),
    deps_type=None,
    result_type=str,
)


@router.post("/ollama/generate")
async def generate(prompt: Prompt, session: SessionDep) -> StreamingResponse:
    prompt = await translate_prompt(prompt)
    prompt_category = await search_or_not(prompt)

    print("Prompt category: " + str(prompt_category))
    if prompt_category == 1:
        return Response(
            content=(await item_agent.run(prompt.prompt, deps=MerchantContext(merchant_id=prompt.merchant_id))).data
        )
    elif prompt_category == 2:
        # First, analyze the query to determine data_point and time period
        query_analysis = await transaction_agent.run(prompt.prompt)
        params = json.loads(query_analysis.data)

        # Then get transaction data
        transactions = crud.get_merchant_transactions_summary(
            session, prompt.merchant_id
        )
        params['data_points'] = transactions

        return params
    else:
        return StreamingResponse(
            generate_stream(chatbot_agent, prompt, session),
            media_type="text/event-stream"
        )


@router.get("/ollama/summarize_reviews/{merchant_id}")
async def summarize_reviews(merchant_id: str) -> StreamingResponse:
    url = f'{FASTAPI_URL}/reviews/{merchant_id}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        reviews_data = response.json()

        # Extract reviews and ratings
        reviews = [review["review"] for review in reviews_data]
        ratings = [review["rating"] for review in reviews_data]

        # Calculate average rating
        average_rating = sum(ratings) / len(ratings) if ratings else 0

        review_summary = await review_agent.run(reviews)

        return {
            "average_rating": average_rating,
            "review_summary": review_summary.data
        }
    else:
        return {"error": "Unable to fetch reviews from API"}
