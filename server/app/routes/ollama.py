from fastapi import APIRouter
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


async def search_or_not(prompt: Prompt, context: str = ""):
    category_agent = Agent(
        model=ollama_model,
        system_prompt=(
            'You are not an AI assistant. Your only task is to decide if an API call is needed and if any of the APIs that are available is suitable to obtain additional information to answer the users prompt,' +
            'or to just act as a normal chatbot for normal conversation.' +
            'If you do not know an answer to a question, do not make things up! that means an API call is needed.' +
            'Respond with "1" if it is an inquiry/plotting a graph about inventory ' +
            'Respond with "2" if it is an inquiry about competitors '
            'Respond with "0" otherwise' +
            'Example: User : "Hello" Mistral: "{ "category": 0, "reasoning":"it is just a common greeting."  }" ' +
            'User : "Do you sell any ice cream?" Mistral: "{"category": 1, "reasoning":"Get_Items needs to be called" }" ' +
            'Respond in json format.' +
            f'\nThe available APIs are: {available_APIs}'
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

inventory_agent = Agent(
    model=ollama_model,
    name="Inventory_Agent",
    system_prompt=(
        "You are an AI agent that can call tools to help answer a store owner's questions about his inventory.\n"
        "You HAVE access to some APIs, you MUST use the tools directly first and use its result to respond.\n"
        "You are not to generate speculative or irrelevant content, additional commentary, explanations, questions or off-topic facts.\n"
        "Do not provide any information that is not based on the tools available, and do not mention what you are going to do.\n"
        "If you user asks you to plot a graph, you MUST get the data from the API first and then generate the data points in JSON,\n"
        "For example:\n"
        "user: 'What are the items currently available', Mistral: '{\"items\": [{\"name\": \"Item A\", \"quantity\": 10}, {\"name\": \"Item B\", \"quantity\": 5}]}, placeholder information must be replaced with REAL information'\n"
        "user: 'Do we still have any more X?', Mistral: '{\"item\": \"X\", \"available\": false}'\n"
        "user: 'Plot a graph of my inventory' Mistral: '{\"graph\": {\"type\": \"pie\", \"data\": [{\"name\": \"Item A\", \"quantity\": 10}, {\"name\": \"Item B\", \"quantity\": 5}]}}'\n"
        "If you do not have any information to generate from the tools, simply reply '{\"error\": \"I am unable to provide that information\"}'.\n"
        "DO NOT ever provide placeholder text or invent information. ONLY provide factual results based on the tools available.\n"
    ),
    deps_type=None,
    result_type=str,
)


@inventory_agent.tool
async def GET_items(ctx: RunContext[None]) -> Union[str, List[Item]]:
    url = f'{FASTAPI_URL}/items'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        items_data = response.json()
        return [Item(**item) for item in items_data]
    else:
        return 'Failed to fetch items from API'


review_agent = Agent(
    model=ollama_model,
    name="Review_Agent",
    system_prompt=(
        "You are an AI agent that can that summarizes how a merchant is doing based on user reviews in json.\n"
        "Emphasize on the positive and negative aspects of the reviews, especially on the pricing, environment, customer service and the food quality\n"
    ),
    deps_type=None,
    result_type=str,
)


@router.post("/ollama/generate")
async def generate(prompt: Prompt, session: SessionDep) -> StreamingResponse:
    prompt = await translate_prompt(prompt)
    prompt_category = await search_or_not(prompt)
    agent = inventory_agent if prompt_category == 1 else chatbot_agent

    return StreamingResponse(
        generate_stream(agent, prompt, session),
        media_type="text/event-stream"
    )


@router.post("/ollama/summarize_reviews")
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
