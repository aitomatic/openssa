let conversation = [
    // { "role": "system", "content": "You are a domain expert in semiconductor." }
];

function updateChatbox(sysmsgs) {
    let roleLabels = {
        "system": "SYSTEM",
        "user":	"USER",
        "assistant": "SSM"
    };

    var chatbox = document.getElementById('chatbox');
    chatbox.innerHTML = conversation.map(msg => `<div class="${roleLabels[msg.role]}">${roleLabels[msg.role]}: ${msg.content}</div>`).join('');
    chatbox.scrollTop = chatbox.scrollHeight;

    var syslog = document.getElementById('syslog');
    syslog.innerHTML += sysmsgs.map(msg => `<div>${msg}</div>`).join('');
    syslog.scrollTop = chatbox.scrollHeight;
}

document.getElementById('inputbox').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {

        // Show the spinner
        document.getElementById('loading').classList.remove('d-none');

        const userMessage = this.value;
        conversation.push({ "role": "user", "content": userMessage });

        const TIMEOUT = 10000; // Timeout after 10 seconds
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), TIMEOUT);

        // Get model name from the dropdown
        model = document.getElementById('models').value;

        // Send the conversation to the backend
        fetch('/discuss', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            signal: controller.signal,
            body: JSON.stringify({
                "model": "gpt3_chat_completion",
                // "model": "gpt3_completion",
                "message": userMessage
            })
        })
        .then(response => response.json())
        .then(data => {
            // Append the assistant's response to the conversation
            conversation.push({ "role": "assistant", "content": data.choices[0].message.content });

            // console.log(data.choices[0].syslog)
            updateChatbox(data.choices[0].syslog);

            // Hide the spinner
            document.getElementById('loading').classList.add('d-none');
        })
        .catch(error => {
            if (error.name === 'AbortError') {
                // Timeout occurred
                conversation.push({ "role": "system", "content": "<span style='color:red;'>Sorry, I'm taking too long to respond. Please try again.</span>" });
                updateChatbox();
            }

            // Hide the spinner
            document.getElementById('loading').classList.add('d-none');
        });

        // Clear the input box for the next message
        this.value = '';
        e.preventDefault();
    }
});