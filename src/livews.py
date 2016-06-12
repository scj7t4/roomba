import json
import random
import threading
import datetime
import asyncio
import websockets

import control.openinterface.commands as commands
import control.openinterface.query as query
import control.openinterface.packets as packets
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)

def block_read(ser, num):
    reading = bytes([])
    while len(reading) < num:
        reading += ser.read(num)
    return reading

print(ser.name)

packets = [44, 43]
streamer = query.PacketStreamer(ser, packets)

lock = threading.Lock()
samples = []

def encoder_worker(streamer):
    global samples
    streamer.freshen()
    streamer.start()
    init = streamer.read()
    prev_el = init['LeftEncoderCounts'].int
    prev_er = init['RightEncoderCounts'].int
    prev_t = datetime.datetime.utcnow()
    while streamer.state == 'streaming':
        read = streamer.read()
        if read == None:
            continue
        t = datetime.datetime.utcnow()
        el = read['LeftEncoderCounts'].int
        er = read['RightEncoderCounts'].int
        encoder_left = (el - prev_el)
        encoder_right = (er - prev_er)
        if encoder_left == 0 and encoder_right == 0:
            continue
        delta_t = 0.015
        with lock:
            samples.append({'encoder_left': encoder_left, 'encoder_right': encoder_right, 'delta_t': delta_t})
        prev_el, prev_er, prev_t = el, er, t

thread = threading.Thread(target=encoder_worker,args=(streamer,))
thread.run()

async def telemetry_live(websocket, path):
    global samples
    while streamer.state == 'streaming':
        cmd = await websocket.recv()
        print("< {}".format(cmd))
        with lock:
            j = json.dumps(resp)
            del samples[:]
        await websocket.send(j)
        print("> {}".format(j))

start_server = websockets.serve(server, '0.0.0.0', 9998)

print("Preparing websocket")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
