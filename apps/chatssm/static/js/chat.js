let conversation = [
    { "role": "system", "content": "You are a domain expert in industrial boilers." }
];

document.getElementById('inputbox').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {

	// Show the spinner
	document.getElementById('loading').classList.remove('d-none');

        const userMessage = this.value;
        conversation.push({ "role": "user", "content": userMessage });

        // Send the conversation to the backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "model": "gpt-3.5-turbo",
                "messages": conversation
            })
	}).then(response => response.json())
          .then(data => {
              // Append the assistant's response to the conversation
              conversation.push({ "role": "assistant", "content": data.choices[0].message.content });

              // Update the chatbox
	      let roleLabels = {
		  "system":	"SYSTEM",
		  "user":	"USER",
		  "assistant":	"SSM"
	      };

	      var chatbox = document.getElementById('chatbox');
	      //chatbox.value = conversation.map(msg => `<div class="${roleLabels[msg.role]}">${roleLabels[msg.role]}: ${msg.content}</div>`).join('');
	      chatbox.innerHTML = conversation.map(msg => `<div class="${roleLabels[msg.role]}">${roleLabels[msg.role]}: ${msg.content}</div>`).join('');
	      chatbox.scrollTop = chatbox.scrollHeight;

	      // Hide the spinner
	      document.getElementById('loading').classList.add('d-none');
	  });

	// Clear the input box for the next message
        this.value = '';
        e.preventDefault();
    }
});
