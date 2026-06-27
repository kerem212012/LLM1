# LLM1

A simple Python CLI project for interacting with Anthropics Claude models using `anthropic`, `environs`, and `rich`.

## Features

- CLI chat loop in `chat.py`
- Streaming response display with `rich`
- Token usage and cost tracking
- Environment-based configuration via `config.py`

## Requirements

- Python 3.12+
- `API_KEY` environment variable for Anthropics

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
python -m pip install -U pip
python -m pip install anthropic environs rich
```

Alternatively, install from the project package:

```bash
python -m pip install .
```

## Configuration

Create a `.env` file in the project root with the following content:

```env
API_KEY=your_anthropic_api_key_here
MODEL=claude-sonnet-4-6
MAX_TOKENS=2048
```

The default model is `claude-sonnet-4-6` and default max tokens is `2048`.

## Usage

Run the chat interface:

```bash
python chat.py
```

This starts an interactive prompt where you can enter messages and receive streamed replies.

`main.py` contains a small `rich` formatting demo and is not the chat runner.

## Project files

- `chat.py`: main chat loop with Anthropics streaming and token accounting
- `config.py`: loads environment variables
- `main.py`: simple `rich` output example
- `pyproject.toml`: project metadata and dependencies

## Notes

- `README.md` is referenced by `pyproject.toml`
- Adjust `MAX_TOKENS` in `.env` as needed for your use case

