from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import logging
from pydantic import BaseModel
import httpx
from pydantic_ai import Agent, RunContext
from typing import List, Union
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Configure logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

FASTAPI_URL = "http://localhost:8000"

convo_history = []

available_APIs = [
    {
        "function": "get_all_items",
        "description": "Retrieve all items from the database.",
        "arguments": {}
    }
]


class Prompt(BaseModel):
    prompt: str


class Item(BaseModel):
    '''Define Result Model'''
    id: int | None = None
    name: str
    description: str
    price: float


ollama_model = OpenAIModel(
    model_name='mistral', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)


async def generate_stream(agent, prompt: Prompt):
    async with agent.run_stream(prompt.prompt) as result:
        async for text in result.stream(debounce_by=0.01):
            yield text

    convo_history.append({"user": prompt, "bot": result})


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


async def search_or_not(prompt: Prompt, context: str):
    api_agent = Agent(
        model=ollama_model,
        system_prompt=(
            'You are not an AI assistant. Your only task is to decide if an API call is needed and if any of the APIs that are available is suitable to obtain additional information to answer the users prompt,' +
            'or to just act as a normal chatbot for normal conversation.' +
            'If you do not know an answer to a question, do not make things up! that means an API call is needed.' +
            'Generate "True" if API call is needed or "False" if a chatbot is needed as a response in this conversation.' +
            'Example: User : "Hello" Mistral: "False, it is a greeting." ' +
            'Example: User : "Do you sell any ice cream?" Mistral: "True, will have to call get_all_items to check inventory." ' +
            f'\nThe available APIs are: {available_APIs}'
        ),
        deps_type=None,
        result_type=str,
    )

    isSearch = await api_agent.run(prompt.prompt)

    if 'true' in isSearch.data.lower():
        print('Checking through database for additional information...')
    else:
        print('Oh I know! I can answer that without searching!')
    return 'true' in isSearch.data.lower()

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

api_agent = Agent(
    model=ollama_model,
    name="API_Caller_Responder",
    system_prompt=(
        "You are an AI agent that can call tools to help answer a store owner's questions.\n"
        "You HAVE access to some APIs, you MUST use the tools directly first and use its result to respond.\n"
        "You are not to generate speculative or irrelevant content, additional commentary, explanations, questions or off-topic facts.\n"
        "For example:\n"
        "user: 'What are the items currently available', Mistral: 'Here are the items currently available: Item A, Item B, ...'\n"
        "user: 'Do we still have any more X?', Mistral: 'It seems that we do not have any more X left.'\n"
        "If you do not have any information to generate from the tools, simply reply 'I am unable to provide that information'.\n"
        "DO NOT ever provide placeholder text or invent information. ONLY provide factual results based on the tools available.\n"
    ),
    deps_type=None,
    result_type=str,
)


@api_agent.tool
async def GET_items(ctx: RunContext[None]) -> Union[str, List[Item]]:
    url = f'{FASTAPI_URL}/items'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        items_data = response.json()
        return [Item(**item) for item in items_data]
    else:
        return 'Failed to fetch items from API'


@router.post("/ollama/generate")
async def generate(prompt: Prompt, context="These are the previous prompts and responses: " + str(convo_history)) -> StreamingResponse:
    global convo_history

    prompt = await translate_prompt(prompt)

    isSearch = await search_or_not(prompt, context)
    if isSearch:
        return StreamingResponse(generate_stream(api_agent, prompt), media_type="text/event-stream")

    else:
        return StreamingResponse(generate_stream(chatbot_agent, prompt), media_type="text/event-stream")
