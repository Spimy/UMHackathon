from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import logging
import ollama
from pydantic import BaseModel
import httpx
from pydantic_ai import Agent, RunContext
from typing import List, Union
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

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

# Define Result Models
class Item(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: float

# Define response for failed or missing data
class APIError(BaseModel):
    error: str

ollama_model = OpenAIModel(
    model_name='mistral', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)

async def search_or_not(user_input: str, context: str):
    try:
        # Define the agent responsible for handling API calls and responses
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

        isSearch = await api_agent.run(user_input)
        # print(isSearch.data)

        if 'true' in isSearch.data.lower():
            print('Checking through database for additional information...')
        else :
            print('Oh I know! I can answer that without searching!')
        return 'true' in isSearch.data.lower()
    except Exception as e:
        logging.error(f"Error in search_or_not: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def call_APIs(user_input):
    try:
        print('Making API call...')
        

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
        async def GET_items(ctx: RunContext[None]) -> Union[List[Item], APIError]:
            url = f'{FASTAPI_URL}/items'
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            if response.status_code == 200:
                items_data = response.json()
                return [Item(**item) for item in items_data]
            else:
                return APIError(error='Failed to fetch items from API')

        return await api_agent.run(user_input)
    except Exception as e:
        logging.error(f"Error in call_APIs: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def handle_user_input(user_input, context = "These are the previous prompts and responses: " + str(convo_history)):
    global convo_history
    try:
        async def translate_text(user_input, target_language='en'):
            url = "https://translate.spimy.dev/translate"
            headers = {"Content-Type": "application/json"}
            data = {
                "q": f"{user_input}",
                "source": "auto",
                "target": f"{target_language}",
                "format": "text",
            }

            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(url, json=data, headers=headers)
                except httpx.RequestError as e:
                    print(f"Request failed: {e}")
                    return user_input
                
            try:
                response_json = response.json()
                translated_text = response_json.get("translatedText", "")
                return translated_text
            except Exception as e:
                logging.error(f"Error in translate_text: {e}")
                return user_input

        user_input = await translate_text(user_input)

        augmented_context = f"Here’s what I know: {context}"

        isSearch = await search_or_not(user_input, augmented_context)
        if isSearch:
            model_response = await call_APIs(user_input)
            bot_response = model_response.data
        else:
            chatbot_agent = Agent(
                model=ollama_model,
                system_prompt=(
                    'You are a friendly AI assistant, DO NOT MAKE stuff up, only respond to the user with the information you have and say you do not know'
                ),
                deps_type=None,  
                result_type=str,  
            )

            response = await chatbot_agent.run(user_input)
            bot_response = response.data

        convo_history.append({"user": user_input, "bot": bot_response})
        return bot_response
    except Exception as e:
        logging.error(f"Error in handle_user_input: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/ollama/generate")
async def generate(prompt: Prompt):
    try:
        response = await handle_user_input(prompt)
        return response
    except Exception as e:
        logging.error(f"Error in generate endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



