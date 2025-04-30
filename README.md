# Functional Requirements Agent

A modular PySide6 application that serves as a functional requirements agent to help users define clear, complete, and validated functional requirements through structured dialogue. The application follows a clean, maintainable architecture with all files under 100 lines of code.

## Features

- Interactive chat interface with LLM integration
- Guided conversation to elicit requirements
- Structured approach to requirements gathering
- Project management with saving/loading capability
- Export requirements to JSON and text formats
- Clean, modular architecture with separation of concerns
- Simple and intuitive UI

## Requirements

- Python 3.6+
- PySide6
- Access to an LLM provider (OpenAI, Anthropic, etc.)

## Installation

Install the required dependencies:

```bash
pip install PySide6 openai anthropic
```

## Usage

Run the application with:

```bash
python main.py
```

## Architecture

The application follows a modular architecture with clear separation of concerns:

```
ui/
├── __init__.py
├── main_window.py (main coordinator)
├── dialogs.py (dialog components)
├── components/
│   ├── __init__.py
│   ├── header.py
│   ├── status_panel.py
│   ├── action_buttons.py
│   └── chat_area.py
└── handlers/
    ├── __init__.py
    ├── ui_handler.py (UI coordinator)
    ├── llm_handler.py (LLM integration)
    ├── requirements_handler.py (requirements management)
    ├── export_handler.py (export functionality)
    ├── conversation_handler.py (conversation management)
    ├── project_handler.py (project management)
    ├── requirements_ui_handler.py (requirements UI)
    ├── export_ui_handler.py (export UI)
    ├── message_handler.py (message handling)
    └── llm_ui_handler.py (LLM configuration UI)
```

## How It Works

The application implements a chat interface where the agent guides you through a structured conversation to:

1. Identify key stakeholders and their expectations
2. Elicit and clarify system goals, constraints, and operational scenarios
3. Translate stakeholder needs into unambiguous, testable functional requirements
4. Ensure traceability between stakeholder expectations and technical requirements
5. Validate requirements through iterative dialogue

The application automatically extracts potential requirements from the conversation and allows you to review, edit, and export them.

## Design Principles

- **Modularity**: Each component has a single responsibility
- **Maintainability**: All files are kept under 100 lines of code
- **Separation of Concerns**: UI components are separated from business logic
- **Extensibility**: Easy to add new features or modify existing ones
