/* global updateSyslog */ // for ESLint
// import { updateSyslog } from './discuss.js';

// const { update } = require("lodash");

class KnowledgeEventHandlers {

    // Common function to make POST requests
    _postData(url = '', data = {}) {
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(data).toString(),
        })
        .then(response => response.json());
    }

    // Define the event handler function for 'knowledge'
    handleKnowledgeInput = (event) => {
        // Prevent the form from being submitted in the traditional way
        event.preventDefault();

        let knowledgeText = document.getElementById('knowledge').value;

        self._postData('/knowledge', { knowledge: knowledgeText })
        .then(data => {
            // Handle the response here
            updateSyslog(data);
            // console.log(data);
            // if (data.message) { alert(data.message); }
        })
        .catch(error => {
            // Handle any errors here
            updateSyslog(`Error: ${JSON.stringify(error)}`);
            // console.error('Error:', error);
        });
    }

    // Define the event handler function for 'upload'
    handleKnowledgeUpload = (event) => {
        // Prevent the form from being submitted in the traditional way
        event.preventDefault();

        let file = document.getElementById('file').files[0];
        let formData = new FormData();
        formData.append('file', file);

        // Make a POST request to the '/upload' route
        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response here
            updateSyslog(data);
            console.log(data);
            // if (data.filename) { alert(`File uploaded successfully: ${data.filename}`); }
        })
        .catch(error => {
            // Handle any errors here
            updateSyslog(`Error: ${JSON.stringify(error)}`);
            // console.error('Error:', error);
        });
    }
}

// Register the events
const keh = new KnowledgeEventHandlers();
document.getElementById("upload-file-button").addEventListener('click', keh.handleKnowledgeUpload);
document.getElementById("send-text-button").addEventListener('click', keh.handleKnowledgeInput);
