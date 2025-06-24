import asyncio
import websockets

from ocpp.v201 import call, ChargePoint as cp
from ocpp.v201.enums import RegistrationStatusEnumType, BootReasonEnumType

from ocpp.v201.datatypes import ChargingStationType

class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotification(
            charging_station = ChargingStationType("TempVendor", "TempModel"),
            reason = BootReasonEnumType.power_up
        )

        response = await self.call(request)

        # if response.status ==  RegistrationStatusEnumType.accepted:
        #     print("Connected to central system.")


async def main():
    async with websockets.connect(
        'ws://localhost:9000/CP_1',
         subprotocols=['ocpp2.0.1']
    ) as ws:

        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification())


if __name__ == '__main__':
    asyncio.run(main())