import sys
import json

beacons = {}

def worker():
    global beacons
    while True:
        line = sys.stdin.readline()
        parts = line.split(",")
        chunks = map(lambda x: x.split(":"), parts)
        r = {}
        for (key,value) in chunks:
            r[key.strip()] = value.strip()
        beacons[r['MINOR']] = r
        print(json.dumps(beacons, indent=2))

worker()
