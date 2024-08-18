# Seek-Next: AI-Powered Education Platform

Welcome to Seek-Next, an AI-powered education platform that provides students with personalized course recommendations, interactive learning modules, the ability to ask questions and summarize lecture transcripts using AI and a coding programming portal that is integrated with genAI. This project is built with a modern tech stack and aims to make education more accessible and tailored to individual needs.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Frontend Setup](#frontend-setup)
  - [Install Vue CLI and Vue Router](#install-vue-cli-and-vue-router)
  - [Install Additional Packages](#install-additional-packages)
  - [Run the Frontend](#run-the-frontend)
- [Backend Setup](#backend-setup)
  - [Create a Virtual Environment](#create-a-virtual-environment)
  - [Activate the Virtual Environment](#activate-the-virtual-environment)
  - [Install Python Requirements](#install-python-requirements)
  - [Install Ollama](#install-ollama)
  - [Start FastAPI](#start-fastapi)
- [Note](#Note)

## Overview

This project combines a Vue.js frontend for managing coding assignments, a Python backend for evaluating code submissions, and an AI chat feature for assistance.

## Project Structure
``` 
SOFT-ENGG-PROJ/
├── seek-next (frontend)/
│   ├── public/
│   │   ├── transcript_data/
│   ├── src/
│   │   ├── assets/
│   │   ├── pages/
│   │   │   └── (vue-pages)
│   │   ├── routes/
│   │   └── store/
│   │       ├── App.vue/
│   │       └── main.ts/
│   ├── index.html
│   └── package.json
├── server (backend)/
│   ├── api/
│   │   ├── middleware/
│   │   └── payload_schema/
│   ├── constants/
│   │   └── (AI prompts)
│   ├── database/
│   │   └── (Models, SQL and NoSQL db)
│   ├── docs/
│   ├── resources/
│   │   └── (API endpoints)
│   ├── test_resouces/
│   ├── dockerfile
│   ├── requirements.txt
│   └── main.py
└── LICENSE
└── README.md
```

## Running the Application

To run the full application:
1. Start the backend server by following the instructions in the Backend section.
2.  Run the frontend by following the instructions in the Frontend section.
3.  Access the application in your browser at 
    - http://localhost:8000 : back-end (server)
    - http://localhost:5173/ : front-end (seek-next)

## Frontend Setup

### Install Vue CLI and Vue Router

```sh
npm install -g @vue/cli
npm install vue-router
```

### Install Additional Packages

All necessary packages are listed in the package.json file. To install them, run:

```sh
npm install
```

### Run the Frontend

To start the development server, run:

```sh
npm run serve
```

## Backend Setup
### Create a Virtual Environment

To create a virtual environment, run:
```sh
python3 -m virtualenv venv
```

### Activate the Virtual Environment

For Linux and macOS:

```sh
source venv/bin/activate
```
For Windows:
```sh
venv\Scripts\activate
```
Install Python Requirements

To install the required Python packages, run:
```sh
pip install -r requirements.txt
```

### Install Ollama
For Linux:
```sh
curl -fsSL https://ollama.com/install.sh | sh
```
For Windows:

Refer to the [Ollama Installation Guide](https://ollama.com/download/windows) for detailed instructions.

Inistall codellama:7b
```sh
ollama run codellama
```

### Start FastAPI: 
```sh
fastapi run main.py
```
To refer to the API docs hit the url:
```
localhost:8000/docs
```
## Note
For executing code, docker is used in the backend that uses a java container for compilation. It is higly recommended that you have it locally.


