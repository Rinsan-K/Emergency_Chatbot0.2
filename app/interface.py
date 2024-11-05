import gradio as gr
import requests

def chat(query):
    try:
        response = requests.post("http://127.0.0.1:8000/query", json={"user_input": query})
        response.raise_for_status()  # Raises an error for HTTP 4xx/5xx responses
        return response.json().get("response", "Sorry, I didn't understand that.")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with server: {e}"

# Set up the Gradio interface
gr.Interface(fn=chat, inputs="text", outputs="text", title="Emergency Preparedness Chatbot").launch()
