// Use an empty API key string. The canvas environment will handle the actual key.
const apiKey = "AIzaSyCXwUke-IOCoc_wa2rc0UT2L-wqWE_BANM";
const apiUrl = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=" + apiKey;

const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const loadingIndicator = document.getElementById('loading-indicator');

// Function to create and append a new message bubble
function addMessage(text, isUser) {
    const messageContainer = document.createElement('div');
    messageContainer.className = `flex ${isUser ? 'justify-end' : 'justify-start'} items-start`;
    
    const messageBubble = document.createElement('div');
    messageBubble.className = `message-bubble p-3 rounded-xl shadow-md ${isUser ? 'user-message' : 'bot-message'}`;
    messageBubble.innerHTML = formatText(text); // Use innerHTML to render Markdown
    
    messageContainer.appendChild(messageBubble);
    chatLog.appendChild(messageContainer);
    
    // Scroll to the bottom of the chat log
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Function to format the bot's response for display
function formatText(text) {
    // Replace bold Markdown with HTML for better display
    return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

// Handle the user sending a message
async function sendMessage() {
    const userMessage = userInput.value.trim();
    if (userMessage === '') return;

    // Display user message
    addMessage(userMessage, true);
    userInput.value = '';
    
    // Show loading indicator
    loadingIndicator.classList.remove('hidden');
    sendButton.disabled = true;

    try {
        // Construct the API payload for a RAG-like response using Google Search grounding
        const payload = {
            contents: [{ parts: [{ text: userMessage }] }],
            // The 'tools' property with 'google_search' is the core of our RAG simulation.
            // This tells the LLM to retrieve information from the web before generating a response.
            tools: [{ "google_search": {} }],
            systemInstruction: {
                parts: [{ text: "You are a friendly and professional nutritional expert named Nutri-Bot. Provide concise, clear, and easy-to-understand information based on reliable sources. If you are asked to provide medical advice, gently decline and recommend consulting a healthcare professional or a registered dietitian. You must cite your sources if Google Search is used." }]
            },
        };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        // Retry with exponential backoff if the response is not OK
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`API request failed: ${response.status} - ${JSON.stringify(errorData)}`);
        }

        const result = await response.json();
        const candidate = result.candidates?.[0];

        if (candidate && candidate.content?.parts?.[0]?.text) {
            const text = candidate.content.parts[0].text;
            let sources = [];
            const groundingMetadata = candidate.groundingMetadata;
            
            if (groundingMetadata && groundingMetadata.groundingAttributions) {
                sources = groundingMetadata.groundingAttributions
                    .map(attribution => ({
                        uri: attribution.web?.uri,
                        title: attribution.web?.title,
                    }))
                    .filter(source => source.uri && source.title);
            }

            // Append citations to the bot's response
            let fullResponse = text;
            if (sources.length > 0) {
                fullResponse += "\n\n**Sources:**";
                sources.forEach((source, index) => {
                    fullResponse += `\n- [${source.title}](${source.uri})`;
                });
            }

            addMessage(fullResponse, false);

        } else {
            addMessage("I'm sorry, I couldn't generate a response. Please try again.", false);
        }

    } catch (error) {
        console.error("Error fetching from API:", error);
        addMessage("I'm sorry, an error occurred. Please try again.", false);
    } finally {
        // Hide loading indicator and enable button
        loadingIndicator.classList.add('hidden');
        sendButton.disabled = false;
        userInput.focus();
    }
}

// Add event listeners
sendButton.addEventListener('click', sendMessage);
