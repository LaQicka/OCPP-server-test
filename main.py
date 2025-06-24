import asyncio
from datetime import datetime
import json
import os
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result
from ocpp.v16.enums import Action
import websockets

class ChargePoint(cp):
    def __init__(self, id, connection):
        super().__init__(id, connection)
        self.log_dir = "ocpp_logs"
        os.makedirs(self.log_dir, exist_ok=True)

    async def log_message(self, message, direction="IN"):
        """Логирует сообщение в файл и консоль"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "direction": direction,
            "message": message
        }
        
        # Вывод в консоль
        print(f"[{timestamp}] {direction}: {json.dumps(message, indent=2)}")
        
        # Сохранение в файл
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.log_dir, f"{date_str}.json")
        
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    @on(Action.boot_notification)
    async def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        await self.log_message({
            "action": Action.boot_notification,
            "vendor": charge_point_vendor,
            "model": charge_point_model,
            **kwargs
        })
        return call_result.BootNotification(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status='Accepted'
        )

    @on(Action.status_notification)
    async def on_status_notification(self, connector_id, error_code, status, **kwargs):
        await self.log_message({
            "action": Action.status_notification,
            "connector_id": connector_id,
            "error_code": error_code,
            "status": status,
            **kwargs
        })
        return call_result.StatusNotification()

    @on(Action.meter_values)
    async def on_meter_values(self, connector_id, meter_value, **kwargs):
        await self.log_message({
            "action": Action.meter_values,
            "connector_id": connector_id,
            "meter_value": meter_value,
            **kwargs
        })
        return call_result.MeterValues()

    @on(Action.heartbeat)
    async def on_heartbeat(self, **kwargs):
        await self.log_message({
            "action": Action.heartbeat,
            **kwargs
        })
        return call_result.Heartbeat(
            current_time=datetime.utcnow().isoformat()
        )

async def on_connect(charge_point_id, websocket):
    """Обработчик нового подключения"""
    print(f"Новое подключение: {charge_point_id}")
    charge_point = ChargePoint(charge_point_id, websocket)
    await charge_point.start()

async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )
    print("OCPP сервер запущен на ws://0.0.0.0:9000")
    await server.wait_closed()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Сервер остановлен")