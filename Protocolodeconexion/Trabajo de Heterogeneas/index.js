const WebSocket = require('ws');
const mqtt = require("mqtt");
const express = require('express')

const setupWebSockets = () => {
  const webSocketServer = new WebSocket.Server({ port: 9000 });

  webSocketServer.on('connection', (socket) => {
    console.log('New client connected');

    // Listening for messages from the client
    socket.on('message', (data) => {
      console.log("WS received:", data.toString());
      socket.send(JSON.stringify({received: `${data}`}));
    });

    // Handling client disconnection
    socket.on('close', () => {
      console.log('Client disconnected');
    });

  });

  console.log('WebSocket server is running on ws://localhost:9000');
}

const setupMqtt = () => {
  const mqttClient = mqtt.connect("mqtt://test.mosquitto.org");

  mqttClient.on("message", (topic, payload) => {
    console.log("MQTT received:", payload.toString());
  });

  mqttClient.emit("message", "matricula", '{"matricula": "m042332"}')
}

const setupExpress = () => {
  const expressApp = express()
  const serverPort = 8080
  expressApp.use(express.json());

  expressApp.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
  })
  expressApp.post('/', (req, res) => {
    console.log(`HTTP received: ${JSON.stringify(req.body)}`);
    res.send({received: req.body})
  })
  expressApp.listen(serverPort, () => {
    console.log(`Express app listening on port ${serverPort}`)
  })
}

setupWebSockets();
setupMqtt();
setupExpress();