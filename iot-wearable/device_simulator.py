import paho.mqtt.publish as publish
import json, random, time, datetime

device_ID = 'smart_watch'
while True:
    payload = {
        "device_id": device_ID,
        "metric": "heart_rate",
        "value": random.randint(60,180),
        "time": datetime.datetime.utcnow().isoformat()
    }
    publish.single("wearables/wearable1/metrics", json.dumps(payload), hostname="localhost")
    print("sent: ", payload)
    time.sleep(2)