### Install Nautobot in Podman
```
podman run -d --pod nautobot-pod --name nautobot-web \
  -e NAUTOBOT_DB_HOST=127.0.0.1 \
  -e NAUTOBOT_DB_NAME=nautobot \
  -e NAUTOBOT_DB_USER=nautobot \
  -e NAUTOBOT_DB_PASSWORD=nautobotpass \
  -e NAUTOBOT_REDIS_HOST=127.0.0.1 \
  -e NAUTOBOT_REDIS_PORT=6379 \
  -e NAUTOBOT_SECRET_KEY=supersecretdevelopmentkeydontuseinprod12345 \
  -e NAUTOBOT_ALLOWED_HOSTS=* \
  docker.io/networktocode/nautobot:stable-py3.13
```