# FastAPI Server

A basic FastAPI server setup.

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

To run the server, use:

```bash
python main.py
```

The server will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Available Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check endpoint
