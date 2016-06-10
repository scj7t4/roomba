import json
import datetime
import subprocess
import threading

from flask import Flask, jsonify

beacons = {}
beacons_lock = threading.Lock()

def beacon_worker(subp):
    global beacons, beacons_lock
    subp.poll()
    while subp.returncode == None:
        line = subp.stdout.readline()
        print(line)
        parts = line.split(",")
        chunks = map(lambda x: x.split(":"), parts)
        r = {}
        for (key,value) in chunks:
            r[key.strip()] = value.strip()
        r['date'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f %z')
        with beacons_lock:
            beacons[r['MINOR']] = r
        subp.poll()

app = Flask(__name__)

@app.route("/")
def index():
    global beacons, beacons_lock
    with beacons_lock:
        return jsonify(**beacons)

if __name__ == "__main__":
    subp = subprocess.Popen(['/bin/bash', './ibeacon_scan'], stdout=subprocess.PIPE,
            universal_newlines=True)
    worker = threading.Thread(target=beacon_worker, args=(subp,))
    worker.start()
    app.run(port=6661)
    subp.terminate()
    worker.join()
