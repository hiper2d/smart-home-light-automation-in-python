# Mosquitto Server

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
The custom config `mosquitto.conf` is needed to avoid the weird [Address not available issue](https://github.com/eclipse/mosquitto/issues/2040).