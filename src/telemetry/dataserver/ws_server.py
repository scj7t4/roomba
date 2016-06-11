import asyncio
import websockets
import json
import random

async def server(websocket, path):
    for i in range(2):
        cmd = await websocket.recv()
        print("< {}".format(cmd))

        resp = {
            'encoder_left': random.randint(0, 100),
            'encoder_right': random.randint(100, 200),
            'delta_t': random.uniform(1,2)
        }
        j = json.dumps(resp)
        await websocket.send(j)
        print("> {}".format(j))

start_server = websockets.serve(server, 'localhost', 9998)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
