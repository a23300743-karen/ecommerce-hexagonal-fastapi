from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.customer_connections: dict[int, WebSocket] = {}
        self.admin_connections: list[WebSocket] = []

    async def connect_customer(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.customer_connections[user_id] = websocket

    async def connect_admin(self, websocket: WebSocket):
        await websocket.accept()
        self.admin_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.admin_connections = [item for item in self.admin_connections if item != websocket]
        disconnected = [user_id for user_id, item in self.customer_connections.items() if item == websocket]
        for user_id in disconnected:
            self.customer_connections.pop(user_id, None)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def send_to_customer(self, user_id: int, message: dict):
        websocket = self.customer_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)

    async def notify_admins(self, message: dict):
        for websocket in list(self.admin_connections):
            try:
                await websocket.send_json(message)
            except Exception:
                self.disconnect(websocket)
