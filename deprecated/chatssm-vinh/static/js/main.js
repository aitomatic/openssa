function appendMessage(event) {
    // Prevent the default form submission that occurs when enter is pressed
    event.preventDefault();
    
    // Get the current text of the chatbox and the input box
    var chatbox = document.getElementById('chatbox');
    var inputbox = document.getElementById('inputbox');
    
    // Append the text from the input box to the chatbox, followed by a newline
    chatbox.value += inputbox.value + '\n';
    
    // Clear the input box for the next message
    inputbox.value = '';
}
