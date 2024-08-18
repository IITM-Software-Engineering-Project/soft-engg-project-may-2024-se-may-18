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
  - [Set Environment Variables](#install-ollama)
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
# npm 7+, extra double-dash is needed:
npm create vite@latest seek-next -- --template vue
npm install vue-router
npm install vuex@next --save
```

### Install Additional Packages

All necessary packages are listed in the package.json file. To install them, run:

```sh
npm install
```

### Run the Frontend

To start the development server, run:

```sh
npm start
```

## Backend Setup
### Create a Virtual Environment

To create a virtual environment, run:
```sh
pip install virtualenv
virtualenv -p 3.12 .venv
```

### Activate the Virtual Environment

For Linux and macOS:

```sh
source .venv/bin/activate
```
For Windows:
```sh
.venv\Scripts\activate
```
Install Python Requirements

To install the required Python packages, run:
```sh
pip install -r requirements.txt
```

### Set Environment Variables
Create a .env file with the following variables:
```
DATABASE_SQL_URL
GEMINI_API_KEY
MONGO_CONNECTION_URI
JDOODLE_CLIENT_ID
JDOODLE_CLIENT_SECRET
```

### Start FastAPI: 
```sh
fastapi dev main.py
```
To refer to the API docs hit the url:
```
localhost:8000/docs
```



