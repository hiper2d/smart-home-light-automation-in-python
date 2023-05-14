# Mosquitto Server

The custom config `mosquitto.conf` is needed to avoid the weird [Address not available issue](https://github.com/eclipse/mosquitto/issues/2040).

To run a shell inside of Mosquitto Docker container use the following
```bash
docker-compose exec mosquitto sh
```
or
```bash
docker exec -it $(container_id) sh
```
When connected to the container, you can send and receive test messages:
```bash
mosquitto_sub -h localhost -p 1883 -t "test/topic"
mosquitto_pub -h localhost -p 1883 -t "test/topic" -m "Hello, world!"
```

Simulate a new device ping message, so the webserver can pick it up:
```bash
mosquitto_pub -h localhost -t "home/ping" -m '{"id": "abc", "rgba": [0, 1023, 61, 1]}'
 ```
New device should appear on the webpage. If it doesn't send ping messages regularly, the webserver will consider it as inactive in 60 seconds and remove from the webpage.

While the device is on the webpage, you can control it. To monitor messages from the frontend to devices you can subscribe to the device topic:

```bash
mosquitto_sub -h localhost -t "home/abc"
 ```