import asyncio
import websockets

from ocpp.v16 import call, ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus


class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotification(
            charge_point_model="Optimus",
            charge_point_vendor="The Mobility House"
        )

        response = await self.call(request)

        if response.status ==  RegistrationStatus.accepted:
            print("Connected to central system.")


async def main():
    try:
        async with websockets.connect(
            'ws://192.168.120.114:9000/CP_1',
            subprotocols=['ocpp1.6']
        ) as ws:

            cp = ChargePoint('CP_1', ws)

            await asyncio.gather(cp.start(), cp.send_boot_notification())
    except Exception as e:
        print(f"Catch exeption:\n{e}")


if __name__ == '__main__':
    asyncio.run(main())