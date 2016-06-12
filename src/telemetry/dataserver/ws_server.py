import asyncio
import websockets
import json
import random

async def server(websocket, path):
    for i in range(2000):
        cmd = await websocket.recv()
        print("< {}".format(cmd))

        resp = {
            'encoder_left': random.randint(0, 150),
            'encoder_right': random.randint(0, 150),
            'delta_t': random.uniform(2,3)
        }
        j = json.dumps(resp)
        await websocket.send(j)
        print("> {}".format(j))

start_server = websockets.serve(server, 'localhost', 9998)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
