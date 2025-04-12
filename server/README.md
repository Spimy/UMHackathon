# Server Setup

The server is built using the following frameworks: 
[FastAPI](https://fastapi.tiangolo.com/)
[Pydantic](https://docs.pydantic.dev/latest/)
[Pydantic AI](https://ai.pydantic.dev/)
[OpenCV](https://opencv.org/)
[Ollama](https://ollama.com/)

## Recommedned Python Version Manager

1. Use pyenv to manage your Python versions

To install [pyenv](https://github.com/pyenv-win/pyenv-win) on Windows use in Powershell:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

2. Download version 3.12.9

```bash
pyenv install 3.12.9
```

3. Use the installed python version

```bash
pyenv global 3.12.9
```

4. Test your python version

```bash
python --version
```

## Setup

1. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

1. You will need Docker to start the database:

```bash
docker compose up -d
# and wait a bit until the postgres container has fully started
```

2. You will need to upload the dataset into `/app/_dataset` folder

> This is because the CSV files are too large and cannot be pushed to GitHub. Download the remaining datasets here: https://drive.google.com/drive/folders/1q8wpploa41fXcw823SSEkb6xfyDQcsVd?usp=sharing

3. To run the server, use:

```bash
python app/main.py
```

The server will be available at `http://localhost:8000`

## Environment Variables
you will have to create a `.env` file here to store the API keys and other variables

```
GEMINI_API_KEY=
DATABASE_URI=postgresql://devuser:devpassword@localhost:5432/umhackathon
```

You may get your Gemini API keys from [here](https://aistudio.google.com/app/apikey).

## Ollama
To run an LLM in your local device, you may get [Ollama](https://ollama.com/)

after installation, run the following commands:

```
# to download mistral:7b model
ollama run mistral

# Optionally: run ollama at background
ollama serve
```

## API Documentation

Once the server is running, you can access:

- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Available Endpoints

- `GET /`: Welcome message
- `POST /ollama/generate`: Use ollama (Mistral) to stream output
