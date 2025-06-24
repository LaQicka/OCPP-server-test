from ocpp.v201 import ChargePoint as OCPPChargePoint
from ocpp.v201 import call_result
import datetime

class ChargePoint(OCPPChargePoint):
    async def on_boot_notification(self, **kwargs):
        """Обработка BootNotification"""
        print(f"⚡ Станция {self.id} отправила BootNotification")
        return call_result.BootNotification(
            status="Accepted",
            current_time=datetime.now().isoformat(),
            interval=30
        )

    async def start(self):
        try:
            await super().start()  # Используем встроенный обработчик
        except Exception as e:
            print(f"Ошибка в ChargePoint: {e}")
            raise