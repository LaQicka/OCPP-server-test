import asyncio
import websockets
from datetime import datetime

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result


class ChargePoint(cp):
    @on(Action.boot_notification)
    def on_boot_notitication(self, charge_point_vendor, charge_point_model, **kwargs):
        print(f"receive boot from {charge_point_model}")
        return call_result.BootNotification(
            current_time=datetime.now().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )


async def on_connect(websocket):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    
    charge_point_id = websocket.request.path.strip('/')
    print(f"connection from {charge_point_id}")
    cp = ChargePoint(charge_point_id, websocket)
    print(f"started cp {charge_point_id}")
    await cp.start()
    print(f"started cp {charge_point_id}")


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )

    print(f"Started 1.6 ocpp server")

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())