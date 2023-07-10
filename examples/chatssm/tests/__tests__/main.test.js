const { JSDOM } = require("jsdom");
const fs = require("fs");
const path = require("path");

describe("Chat Application", () => {
    let window;
    let document;

    beforeAll(() => {
	const html = `
            <textarea id="chatbox"></textarea>
            <input id="inputbox" />
	`;
        const dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable" });
        window = dom.window;
        document = window.document;

        // Get the JavaScript
        const script = fs.readFileSync(path.resolve(__dirname, "../../static/js/main.js"), "utf-8");
	window.eval(script);
    });

    it("should append the input box value to the chatbox", () => {
        const chatbox = document.getElementById("chatbox");
        const inputbox = document.getElementById("inputbox");

        inputbox.value = "Hello there!";

        // Simulate the form submission
        const event = new window.Event("submit");
        window.appendMessage(event);

        expect(chatbox.value).toBe("Hello there!\n");
        expect(inputbox.value).toBe("");
    });
});
