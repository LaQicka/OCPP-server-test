import asyncio
import websockets
from datetime import datetime

LOG_FILE = "websocket_messages.log"

def log_to_file(message):
    """Записывает сообщение в файл с меткой времени."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry)


async def handle_connection(websocket):
    try:
        async for message in websocket:
            print(f"Получено сообщение: {message}")
            log_to_file(f"{message}")         
            
    except websockets.exceptions.ConnectionClosed:
        print(f"Клиент отключился: {websocket.remote_address}")


async def start_server():
    async with websockets.serve(handle_connection, "0.0.0.0", 9000):
        print("WebSocket сервер запущен на ws://0.0.0.0:9000")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_server())