// Replace 'PORT_NUMBER' with the port number your WebSocket server is running on
const socket = new WebSocket('ws://localhost:8000/smart-editor/ws');

// Event handler for when the connection is established
socket.onopen = function(event) {
    console.log("Connected to local WebSocket server");
    socket.send("Hello from the local client!");
};

// Event handler for when a message is received from the server
socket.onmessage = function(event) {
    console.log("Message from server: ", event.data);
};

// Event handler for when the connection is closed
socket.onclose = function(event) {
    if (event.wasClean) {
        console.log(`Connection closed cleanly, code=${event.code}, reason=${event.reason}`);
    } else {
        console.error("Connection closed abruptly");
    }
};

// Event handler for when an error occurs
socket.onerror = function(error) {
    console.error("WebSocket error:", error);
};