
# Emergency Preparedness Chatbot

## Project Overview
This chatbot application provides emergency preparedness information based on expert guidelines, including childbirth assistance in emergencies.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation
1. Clone this repository:
   ```bash
   git clone <your_repo_url>
   cd emergency_chatbot
   ```
   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
To start the application, run:
```bash
python app/main.py
```
This will launch a Gradio interface in your web browser where you can interact with the chatbot.

## Usage Guide
- To interact with the chatbot, open the Gradio UI in your browser.
- You can also use a REST endpoint for the chatbot. Send a POST request to `/chat` with a JSON body:
  ```json
  {
    "query": "How can I prepare for emergency childbirth?"
  }
  ```
- The bot will return a response with relevant emergency preparedness information.
