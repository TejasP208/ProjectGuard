import { getEnv } from "../env.js";

document.addEventListener('DOMContentLoaded', async () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    // Auto-resize textarea
    if (chatInput) {
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
            if (this.value === '') {
                this.style.height = 'auto';
            }
        });
        
        // Enter to submit (Shift+Enter for new line)
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
            }
        });
    }

    // Load AI API Key dynamically
    const env = await getEnv();
    const aiApiKey = env.aiApiKey;
    
    // Maintain Chat History for Context & Persistence
    let chatHistory = JSON.parse(localStorage.getItem('projectguard_chat_history')) || [];

    const appendMessage = (text, isAi = false, save = true) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isAi ? 'ai-message' : 'user-message'}`;
        
        if (isAi) {
            msgDiv.innerHTML = `<i class="ph-fill ph-sparkle"></i>
                                <span>${text.replace(/\n/g, '<br>')}</span>`;
        } else {
            msgDiv.textContent = text;
        }
        
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll

        if (save) {
            localStorage.setItem('projectguard_chat_history', JSON.stringify(chatHistory));
        }
    };

    // Load Existing Chat History onto UI
    const loadHistory = () => {
        // Clear the initial "Hello" if there's actual history
        if (chatHistory.length > 0) {
            chatMessages.innerHTML = '';
            chatHistory.forEach(msg => {
                const text = msg.parts[0].text;
                const isAi = msg.role === 'model';
                appendMessage(text, isAi, false);
            });
        }
    };

    loadHistory();

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userText = chatInput.value.trim();
            if (!userText) return;

            // Show User Message & push to history
            chatHistory.push({ role: "user", parts: [{ text: userText }] });
            appendMessage(userText, false);
            
            chatInput.value = '';
            chatInput.style.height = 'auto';

            if (!aiApiKey) {
                appendMessage("Server error: AI_API_KEY is missing.", true);
                return;
            }

            // Create temporary AI "typing..." message
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message ai-message';
            typingDiv.innerHTML = '<i class="ph-fill ph-sparkle ph-spin"></i> <span>Asking Gemini...</span>';
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                // Call Google Gemini API with conversational history
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${aiApiKey}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        contents: chatHistory
                    })
                });

                if (chatMessages.contains(typingDiv)) chatMessages.removeChild(typingDiv);
                
                if (!response.ok) {
                    throw new Error(`API Error: ${response.status}`);
                }

                const data = await response.json();
                const aiText = data.candidates?.[0]?.content?.parts?.[0]?.text || "Sorry, I couldn't understand that.";
                
                // Show AI Message & push to history
                chatHistory.push({ role: "model", parts: [{ text: aiText }] });
                appendMessage(aiText, true);

            } catch (error) {
                console.error("Chat Error:", error);
                if (chatMessages.contains(typingDiv)) chatMessages.removeChild(typingDiv);
                appendMessage("server error", true);
                chatHistory.pop();
            }
        });
    }
});
