let conversation = [
  // { "role": "system", "content": "You are a domain expert in semiconductor." }
];

function updateChatbox(sysmsgs) {
  let roleLabels = {
      "system": "SYSTEM",
      "user":	"USER",
      "assistant": "SSM"
  };

  var chatbox = document.getElementById("chatbox");
  chatbox.innerHTML = conversation.map(msg => `<div class="${roleLabels[msg.role]}">${roleLabels[msg.role]}: ${msg.content}</div>`).join("");
  chatbox.scrollTop = chatbox.scrollHeight;

  var syslog = document.getElementById("syslog");
  syslog.innerHTML += sysmsgs.map(msg => `<div>${msg}</div>`).join("");
  syslog.scrollTop = syslog.scrollHeight;
}

document.getElementById("inputbox").addEventListener("keydown", function (e) {
  if (e.key === "Enter") {

      // Show the spinner
      document.getElementById("loading").classList.remove("d-none");

      const userMessage = this.value;
      conversation.push({ "role": "user", "content": userMessage });

      const TIMEOUT = 10000; // Timeout after 10 seconds
      const controller = new AbortController();
      // const id = setTimeout(() => controller.abort(), TIMEOUT);
      setTimeout(() => controller.abort(), TIMEOUT);

      // Get model name from the dropdown
      let selected_model = document.getElementById("models").value;

      // Send the conversation to the backend
      fetch("/discuss", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          signal: controller.signal,
          body: JSON.stringify({
              "model": selected_model,
              "message": userMessage
          })
      })
      .then(response => {
          if (!response.ok) {
              var errMsg = `<span style="color:red;">HTTP error status: ${response.status}</span>`; 
              conversation.push({ "role": "system", "content": errMsg });
              updateChatbox([errMsg]);
          }
          return response.json();
      })
      .then(data => {
          // Append the assistant's response to the conversation
          conversation.push({ "role": "assistant", "content": data.choices[0].message.content });
          updateChatbox(data.choices[0].syslog);

          // Hide the spinner
          document.getElementById("loading").classList.add("d-none");
      })
      .catch(error => {
          if (error.name === "AbortError") {
              // Timeout occurred
              var errMsg = `<span style="color:red;">Sorry, I'm taking too long to respond. Please try again.</span>`;
              conversation.push({ "role": "system", "content": errMsg });
              updateChatbox([errMsg]);
          }

          // Hide the spinner
          document.getElementById("loading").classList.add("d-none");
      });

      // Clear the input box for the next message
      this.value = "";
      e.preventDefault();
  }
});
