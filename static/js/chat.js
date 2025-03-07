document.addEventListener('DOMContentLoaded', function() {
    const chatIcon = document.getElementById('chat-icon');
    const chatbotContainer = document.getElementById('chatbot-container');
    const closeChat = document.getElementById('close-chat');
    const minimizeChat = document.getElementById('minimize-chat');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.querySelector('.send-button');
    const quickActions = document.querySelectorAll('.quick-action');
    const notificationDot = document.querySelector('.notification-dot');

    // Toggle chatbot visibility
    function toggleChat() {
        const isVisible = chatbotContainer.style.display === 'flex';
        chatbotContainer.style.display = isVisible ? 'none' : 'flex';
        if (!isVisible) {
            userInput.focus();
            notificationDot.style.display = 'none';
        }
    }

    chatIcon.addEventListener('click', toggleChat);
    closeChat.addEventListener('click', toggleChat);
    minimizeChat.addEventListener('click', toggleChat);

    // Sample responses with improved content
    const responses = {
        'legal rights': 'Your legal rights include fundamental protections such as the right to a fair trial, freedom of speech, privacy, and equal treatment under the law. These rights are protected by various constitutional and statutory provisions.',
        'court procedures': 'Court procedures typically involve several steps: filing initial documents, discovery process, pre-trial motions, trial proceedings, and possible appeals. Each step has specific rules and deadlines that must be followed.',
        'legal documents': 'Common legal documents include contracts, wills, powers of attorney, court pleadings, and affidavits. Each document type serves a specific legal purpose and must be properly formatted and executed.',
        'criminal law': 'Criminal law addresses offenses against society, including investigation, arrest, charging, trial, and sentencing procedures. It covers various offenses from minor infractions to serious felonies.',
        'civil law': 'Civil law deals with disputes between parties, including contract disputes, property matters, and personal injury cases. It typically involves seeking monetary damages or specific actions rather than criminal penalties.',
        'constitutional law': 'Constitutional law interprets and applies the fundamental principles outlined in the constitution, including government powers, individual rights, and the relationship between federal and state authorities.'
    };

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function handleInput() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            
            setTimeout(() => {
                const lowerMessage = message.toLowerCase();
                let response = "I'll help you with that. Please provide more specific details about your legal inquiry.";
                
                for (const [key, value] of Object.entries(responses)) {
                    if (lowerMessage.includes(key)) {
                        response = value;
                        break;
                    }
                }
                
                addMessage(response);
            }, 500);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', handleInput);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleInput();
    });

    quickActions.forEach(button => {
        button.addEventListener('click', () => {
            const topic = button.textContent.toLowerCase();
            addMessage(button.textContent, true);
            setTimeout(() => {
                addMessage(responses[topic]);
            }, 500);
        });
    });

    // Prevent clicks inside chatbot from closing it
    chatbotContainer.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});