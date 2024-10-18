import asyncio
import websockets
import json

async def test_websocket(uri):
    async with websockets.connect(uri) as websocket:
        print(f"Connected to {uri}")

        # Send a test message
        test_message = {
            'message': 'Hello, WebSocket!',
            'sender': 'test_user'
        }
        await websocket.send(json.dumps(test_message))
        print("Message sent:", test_message)

        # Wait for a response from the server
        response = await websocket.recv()
        print("Message received:", response)

if __name__ == "__main__":
    # Replace the WebSocket URL with your server's WebSocket URL
    websocket_url = 'ws://localhost:8000/ws/private/Ariana/'
    asyncio.get_event_loop().run_until_complete(test_websocket(websocket_url))
