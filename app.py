import json
import requests
import time

# --- RAG Core Logic ---

def generate_response(prompt, chat_history, api_key):
    """
    Generates a response using the Gemini API with RAG.

    Args:
        prompt (str): The user's input query.
        chat_history (list): A list of previous messages for context.
        api_key (str): The user-provided API key.

    Returns:
        str: The generated response from the chatbot.
    """
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    # The payload for the API request
    payload = {
        "contents": chat_history,
        "tools": [
            {"google_search": {}}
        ],
        "systemInstruction": {
            "parts": [
                {
                    "text": "You are a helpful nutritional expert chatbot. Your purpose is to provide accurate and helpful nutritional advice. You will use your search tool to find the most relevant and up-to-date information, and then summarize it to answer the user's question. Always cite your sources at the end of your response, if available."
                }
            ]
        },
    }

    retries = 3
    for i in range(retries):
        try:
            response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
            response.raise_for_status()

            # Process the response and extract the text and sources
            result = response.json()
            candidate = result.get('candidates', [None])[0]
            if candidate and candidate.get('content') and candidate['content'].get('parts'):
                text = candidate['content']['parts'][0]['text']

                sources = []
                grounding_metadata = candidate.get('groundingMetadata', {})
                if grounding_metadata and grounding_metadata.get('groundingAttributions'):
                    sources = [
                        source['web'] for source in grounding_metadata['groundingAttributions']
                        if source.get('web')
                    ]

                # Append sources to the response
                if sources:
                    source_links = "\n\n**Sources:**\n"
                    for idx, source in enumerate(sources):
                        source_links += f"{idx + 1}. [{source.get('title', 'Link')}]({source.get('uri', '#')})\n"
                    text += source_links
                
                return text
            else:
                return "I'm sorry, I could not generate a response. Please try again."

        except requests.exceptions.RequestException as e:
            if i < retries - 1:
                time.sleep(2 ** i)
            else:
                return f"An error occurred: {e}"

    return "An unknown error occurred after multiple retries."

if __name__ == "__main__":
    # This block is for command-line interface (CLI) only
    print("Welcome to Nutri-Bot! Your AI Nutritional Expert.")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("-" * 30)

    chat_history = []
    
    # In a CLI context, we would need to manually ask for the API key
    cli_api_key = input("Please enter your API Key: ")
    if not cli_api_key:
        print("API Key is required to run the chatbot.")
    else:
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                print("Nutri-Bot: Goodbye!")
                break

            # Add user message to history for context
            chat_history.append({"role": "user", "parts": [{"text": user_input}]})

            print("Nutri-Bot: Thinking...", end="", flush=True)

            # Get the response from the imported function
            response_text = generate_response(user_input, chat_history, api_key=cli_api_key)
            print("\r" + " " * 20, end="\r") # Clear the "Thinking..." message
            print("Nutri-Bot:", response_text)

            # Add assistant message to history for context
            chat_history.append({"role": "model", "parts": [{"text": response_text}]})
