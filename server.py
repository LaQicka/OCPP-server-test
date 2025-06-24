import asyncio
import json
import os
from datetime import datetime
from typing import Dict

from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.enums import Action, RegistrationStatusEnumType
import websockets
from ocpp.v201 import call, ChargePoint as cp

class ChargePoint(cp):
    @on(Action.boot_notification)
    def on_boot_notitication(self, **kwargs):
        print("received boot_notification")
        return call_result.BootNotification(
            current_time=datetime.now().isoformat(),
            interval=10,
            status=RegistrationStatusEnumType.accepted
        )


async def on_connect(websocket):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    charge_point_id = websocket.request.path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    print(f"started cp {charge_point_id}")
    await cp.start()
    print(f"started cp {charge_point_id}")


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp2.0.1']
    )

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())