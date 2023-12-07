const { JSDOM } = require("jsdom");
const fs = require("fs");
const path = require("path");

describe("Chat Application", () => {
    let window;
    let document;

    beforeAll(() => {
        const html = `
            <div id="chatbox"></div>
            <div id="syslog"></div>
            <input id="inputbox" />
            <select id="models"></select>
            <div id="loading" class="d-none"></div>
        `;
        const dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable" });
        window = dom.window;
        document = window.document;

        // This is the global object that fetch-mock needs
        global.fetch = require("jest-fetch-mock");

        // Get the JavaScript
        const script = fs.readFileSync(path.resolve(__dirname, "../../static/js/discuss.js"), "utf-8");
        eval(script);
    });

    it("should update the conversation when the user presses Enter", async () => {
        const inputbox = document.getElementById("inputbox");
        const chatbox = document.getElementById("chatbox");

        // Mock the server's response
        fetch.mockResponseOnce(JSON.stringify({
            choices: [
                { message: { content: "Hello!" } }
            ]
        }));

        // Trigger the Enter key press
        inputbox.value = "Hello there!";
        const event = new window.KeyboardEvent("keydown", { key: "Enter" });
        inputbox.dispatchEvent(event);

        // Wait for the fetch call to resolve
        await new Promise(resolve => setTimeout(resolve, 100));

        expect(chatbox.innerHTML).toContain("Hello there!");
        expect(chatbox.innerHTML).toContain("Hello!");
    });
});

