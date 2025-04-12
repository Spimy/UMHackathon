from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import logging
from pydantic import BaseModel
import httpx
from pydantic_ai import Agent, RunContext
from typing import List, Union
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import json

# Configure logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter(tags=["ollama"])

FASTAPI_URL = "http://localhost:8000"

convo_history = []

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

class Item(BaseModel):
    '''Define Result Model'''
    id: int | None = None
    name: str
    description: str
    price: float


ollama_model = OpenAIModel(
    model_name='mistral', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)


async def generate_stream(agent, prompt: str):
    async with agent.run_stream(prompt) as result:
        async for text in result.stream(debounce_by=0.01):
            yield text.strip()

    convo_history.append({"user": prompt, "bot": result})


async def translate_prompt(prompt: str, target_language='en') -> str:
    url = "https://translate.spimy.dev/translate"
    headers = {"Content-Type": "application/json"}
    data = {
        "q": f"{prompt}",
        "source": "auto",
        "target": f"{target_language}",
        "format": "text",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response_json = response.json()
            prompt = response_json.get("translatedText", "")
        except httpx.RequestError as e:
            print(f"Translation failed: {e}")

    return prompt


async def search_or_not(prompt: str, context: str):
    category_agent = Agent(
        model=ollama_model,
        system_prompt=(
            'You are not an AI assistant. Your only task is to decide if an API call is needed and if any of the APIs that are available is suitable to obtain additional information to answer the users prompt,' +
            'or to just act as a normal chatbot for normal conversation.' +
            'If you do not know an answer to a question, do not make things up! that means an API call is needed.' +
            'Respond with "1" if it is an inquiry about items ' +
            'Respond with "2" if it is an inquiry about plotting transactions '
            'Respond with "0" otherwise' +
            'Example: User : "Hello" Mistral: { "category": 0, "reasoning":"it is just a common greeting."  } ' +
            'User : "Do you sell any ice cream?" Mistral: {"category": 1, "reasoning":"Get_Items needs to be called" } ' +
            'Make sure to respond in json format.' +
            f'\nThe available APIs are: {available_APIs}'
        ),
        deps_type=None,
        result_type=str,
    )

    result = await category_agent.run(prompt)
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
        "You are an AI agent that can call tools to help answer a store owner's questions.\n"
        "You HAVE access to some APIs, you MUST use the tools directly first and use its result to respond.\n"
        "You are not to generate speculative or irrelevant content, additional commentary, explanations, questions or off-topic facts. \n"
        "For example:\n"
        "user: 'What are the items currently available', Mistral: 'Here are the items currently available: Item A, Item B, ...'\n"
        "user: 'Do we still have any more X?', Mistral: 'It seems that we do not have any more X left.'\n"
        "DO NOT use hypothetical data or mention any hypothetical functions. ONLY provide factual results based on the tools available.\n"
    ),
    deps_type=None,
    result_type=str,
)

@item_agent.tool
async def GET_items(ctx: RunContext[None]) -> Union[str, List[Item]]:
    url = f'{FASTAPI_URL}/merchants/2e8a5/items'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        items_data = response.json()
        transformed_items = [
            Item(
                name=item.get("item_name"),
                description=item.get("cuisine_tag", "No description available"),
                price=item.get("item_price")
            )
            for item in items_data
        ]
        print(transformed_items)
        return transformed_items
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
async def generate(userMessage: dict, context="These are the previous prompts and responses: ") -> StreamingResponse:
    global convo_history


    prompt = userMessage["prompt"].replace("<p>", "").replace("</p>", "")

    prompt = await translate_prompt(prompt)
    print("prompt after translation:" + prompt)

    prompt_category = await search_or_not(prompt, context)
    
    print("Prompt category: ", prompt_category)

    # Check if prompt_category is already an integer
    if isinstance(prompt_category, int):
        category = prompt_category
    else:
        # Convert the string to JSON
        prompt_category_json = json.loads(
            prompt_category.replace("category:", '"category":').replace("reasoning:", '"reasoning":').replace("'", '"')
        )
        # Extract the category number
        category = int(prompt_category_json["category"])

    if category == 1: 

        return StreamingResponse(generate_stream(item_agent, prompt), media_type="text/event-stream")
    else:
        return StreamingResponse(generate_stream(chatbot_agent, prompt), media_type="text/event-stream")
    
@router.post("/ollama/summarize_reviews")
async def summarize_reviews(merchant_id: str) -> StreamingResponse:
    url = f'{FASTAPI_URL}/reviews/{merchant_id}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        reviews_data = response.json()
        reviews_text = " ".join([review['review'] for review in reviews_data])
        prompt = Prompt(prompt=reviews_text)
        return StreamingResponse(generate_stream(review_agent, prompt), media_type="text/event-stream")
    else:
        return StreamingResponse("Failed to fetch reviews from API", media_type="text/event-stream")
