RAG Nutritional Chatbot
This is a simple, command-line and Streamlit-based chatbot that provides nutritional information. It uses the principles of Retrieval-Augmented Generation (RAG) to provide accurate and up-to-date responses.

Instead of relying solely on a pre-trained language model's internal knowledge, this chatbot "retrieves" real-time information from the web using the Gemini API's search grounding feature. This ensures that the answers are not only accurate but also grounded in reliable, external sources.

Key Features
Retrieval-Augmented Generation (RAG): The chatbot leverages the Gemini API to perform live web searches, ensuring its knowledge base is current and factual.

Source Citation: Every response includes citations from the web sources used to generate the answer, promoting transparency and trust.

Dual Interface: The project includes both a basic command-line interface (app.py) and a more user-friendly web interface built with Streamlit (streamlit_app.py).

Project Files
app.py: Contains the core logic for the RAG chatbot. This Python script handles API calls, response generation, and source attribution. It can be run directly from the command line.

streamlit_app.py: A Python script that provides a web-based user interface using the Streamlit library. It imports the core logic from app.py to create a clean and interactive chat experience.

Getting Started
Follow these steps to set up and run the chatbot on your local machine.

Prerequisites
You will need Python 3.7+ installed on your system. You also need to install the required libraries.

pip install requests streamlit

1. Set Up the API Key
The application uses the Gemini API. The API key is automatically handled by the development environment, so you do not need to provide one directly.

2. Run the Chatbot
You have two options for running the chatbot:

Option A: Command-Line Interface (CLI)
This is a simple text-based interface that runs in your terminal.

python app.py

After running the command, you can start a conversation with the bot by typing your questions and pressing Enter. To exit, type exit or quit.

Option B: Web Interface (Streamlit)
This provides a more visual and interactive chat experience in your web browser.

streamlit run streamlit_app.py

This will launch a local web server and open a new browser tab with the chatbot interface. You can interact with the bot directly from there.

How It Works
The magic of RAG happens inside the generate_response function in app.py. When a user's prompt is sent to the Gemini API, a special tools parameter with Google Search is included in the payload. This tells the model to perform a web search to find relevant information.

The model then uses the retrieved search results as "context" to formulate its final response. This allows the bot to answer questions it was not specifically trained on and to provide information that is up-to-date. The groundingMetadata in the API response is used to extract the source URLs and titles, which are then displayed to the user for validation.
