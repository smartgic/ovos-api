<p align="center">
    <em>Expose a secure REST API on top of Open Voice OS core to perform actions on your instance without to SSH into it.</em>
</p>

[![Docker pulls](https://img.shields.io/docker/pulls/smartgic/ovos-api.svg?style=flat&logo=docker&logoColor=FFFFFF&color=87567)](https://hub.docker.com/r/smartgic/ovos-api)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache2.0-yellow.svg)](https://opensource.org/license/apache-2-0) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-pink.svg?style=flat)](https://github.com/smartgic/ovos-api/pulls) [![Discord](https://img.shields.io/discord/809074036733902888)](https://discord.gg/sHM3Duz5d3)

---

OVOS API goal is to provide a layer on top of Open Voice OS to perform actions such as:

- Retrieve information _(version, location, name, etc...)_
- Retrieve skill's settings
- Delete TTS cache files
- Microphone mute and un-mute _(software)_
- Stop any speech or audio output
- And more!

Here is a quick list of use cases where the API could be used:

- Monitoring and get information
- Interface other IoT devices with Mycroft
- Ask for speech from remote sources
- Connect buttons to trigger actions such as `stop` or `listen`
- _The sky is the limit..._

# Architecture

In order to interface with Open Voice OS instance, the API connects to the messages bus to send and receive messages. Some messages used by this API are native to the `ovos-core` such as `stop`, `mycroft.skills.list`, etc... but most of the messages used are custom for the API requirements such as `ovos.api.skill_settings`, `ovos.api.info`, etc...

The API will send messages to the bus but for non-native messages a skill is required to run on `ovos-core` to interpret these messages. This is why the [`skill-rest-api`](https://github.com/smartgic/skill-rest-api) skill must be installed on `ovos-core`. The API and the skill authenticate via an API key shared between both of them.

The `API_KEY` needs to be defined within the `.env` file and this same key must be defined in `~.config/mycroft/skills/skill-rest-api.smartgic/settings.json` file _(see the skill README for more information)_.

<p align="center">
  <img src="./docs/flow.png" alt="OVOS API Flow">
</p>

To consume the API, a user must be required, this user will allow you to retrieve a JSON Web Token _(`JWT`)_ using a basic authentication method. Once the authentication has been validated an access and a refresh tokens will be generated.

# Install

_Python `virtualenv` is always a good practice to keep a clean environment but it is not a mandatory step._

```bash
git clone https://github.com/smartgic/ovos-api.git
cd ovos-api
mkdir ~/virtualenvs
python -m venv ~/virtualenvs/ovos-api
. ~/virtualenvs/ovos-api/bin/activate
pip install -r requirements.txt
```

# Configuration

Before starting to use the API, some configurations must be applied to the `.env` file.

```ini
SECRET=""
WS_HOST="10.12.50.20"
WS_PORT="8181"
API_KEY=""
USERS_DB="/users.json"
```

| Variable   | Explaination                                                            |
| ---------- | ----------------------------------------------------------------------- |
| `SECRET`   | Random string used to generate the JWT token                            |
| `WS_HOST`  | IP address or hostname of the OVOS messages bus                         |
| `WS_PORT`  | TCP Port of the OVOS messages bus                                       |
| `API_KEY`  | Key used between the API and the `skill-rest-api` skill to authenticate |
| `USERS_DB` | File where users are declared with their status and encrypted password  |

The `USERS_DB` should match a path to an existing JSON file. The JSON file should looks like this:

```json
[
  {
    "user": "ovos",
    "password": "$2b$12$THfMtieVfCr3674n.15kcOmffKbJjkb8wX5bkmtP0beHVvEitP52K",
    "active": true
  },
  {
    "user": "jarvis",
    "password": "$2b$12$zmki74hriulBNST9kIE5S.T6jSgunRncw0afld74.aGuW4lV99pyW",
    "active": false
  }
]
```

The `password` field is encrypted using the `bcrypt` Python library _(part of the `requirements.txt` file)_. Use the `genpass.py` Python script to generate the password as demonstrated below.

```bash
. ~/virtualenvs/ovos-api/bin/activate
python genpass.py --password c-h-a-n-g-e-m-e

```

The Python script should return a string like this: `$2b$12$USwu6HcOXJV6u0Xpsa/2DOkS5Js8YizdeGUn.NdiYlywx9fUaVp1i`

# Start the API

`uvicorn` _(part of the `requirements.txt` file)_ is used to serve the API requests, by default it's looking for a `.env` file and if it exists then the variables will be passed to the application.

```bash
cd ovos-api
uvicorn app.api:app --host 10.12.50.21 --port 8000
```

`--host` and `--port` arguments are only used to define how to expose the API, here the API will listen only on `10.12.50.21` address and port `8000`.

# Docker

`Dockerfile` and `docker-compose.yml` files are provided to use this API with Docker.

### Supported architectures and tags

| Architecture | Information                       |
| ------------ | --------------------------------- |
| `amd64`      | Such as AMD or Intel processors   |
| `aarch64`    | Such as Raspberry Pi 3/4/5 64-bit |

_These are examples, many other boards use these CPU architectures._

| Tag               | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `stable`/`latest` | The latest stable version based on the `main` branch |

The `docker-compose.yml` contains variables that will loaded from the `.env` file. As for the users, the file will be mounted as a volume within the container.

```bash
cd ovos-api
docker-compose up -d
```

This command will download the `smartgic/ovos-api:latest` Docker image from Docker Hub and create the `ovos_api` Docker container.

# Consume the API

To consume the API you could use different tools from the very basic but powerful such as `curl` or something more user friendly like Postman _(a collection is provided, more about it below)_. Once the API is up and running, you could get the complete list of the available endpoints at http://10.12.50.21:8000/docs _(replace with your IP address and port)_.

<p align="center">
  <img src="./docs/swagger.png" alt="OVOS API Swagger">
</p>

Here are some `curl` examples to retrieve tokens, information, stop audio output, and more!

## Retrieve tokens

```bash
curl -s -H "Content-Type: application/json" -d '{"user": "ovos", "password": "c-h-a-n-g-e-m-e"}' -X POST http://10.12.50.21:8000/v1/auth/tokens
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNjQxMTY1MDA4LCJpYXQiOjE2NDExNjMyMDgsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJhY2Nlc3MifQ.iIXr0NhYo9A5X9xI06UjVWw8FDGm1ZC4AD8fuBFM2mQ",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNzE4OTIzMjA4LCJpYXQiOjE2NDExNjMyMDgsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJyZWZyZXNoIn0._bp2FUqAzoPWzgDHOlkjIfZvb76BdY6nShqDV1_lJPk"
}
```

If the basic authentication worked then two tokens will be generated:

1. An access token to consume the API only valid 30 minutes _(could be change in `config.py`)_
2. A refresh token valid 6 hours _(could be change in `config.py`)_ to refresh an access token without the user and password

## Retrieve system information

```bash
curl -s -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNjQxMTY1MDA4LCJpYXQiOjE2NDExNjMyMDgsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJhY2Nlc3MifQ.iIXr0NhYo9A5X9xI06UjVWw8FDGm1ZC4AD8fuBFM2mQ" -X GET http://10.12.50.21:8000/v1/system/info
{
  "results": {
    "core_version": "0.0.8",
    "locales": {
      "city": "Montreal",
      "country": "Canada",
      "lang": "en-us",
      "timezone": "America/Toronto"
    },
    "log_level": "info",
    "name": "hey_mycroft",
    "stt_engine": "ovos-stt-plugin-server",
    "system": {
      "architecture": "aarch64",
      "kernel": "6.6.29-v8+",
      "os": "Linux"
    },
    "tts_engine": "ovos-tts-plugin-server"
  }
}
```

## Stop speech or audio output

```bash
curl -s -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNjQxMTY1MDA4LCJpYXQiOjE2NDExNjMyMDgsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJhY2Nlc3MifQ.iIXr0NhYo9A5X9xI06UjVWw8FDGm1ZC4AD8fuBFM2mQ" -X DELETE -I http://10.12.50.21:8000/v1/voice/speech
HTTP/1.1 204 No Content
date: Sun, 02 Jan 2022 22:50:58 GMT
server: uvicorn
```

The `-I` option will return the HTTP status.

## Refresh an access token

```bash
curl -s -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNzE4OTIzMjA4LCJpYXQiOjE2NDExNjMyMDgsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJyZWZyZXNoIn0._bp2FUqAzoPWzgDHOlkjIfZvb76BdY6nShqDV1_lJPk" -X GET http://10.12.50.21:8000/v1/auth/refresh
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNjQxMTY2MjUxLCJpYXQiOjE2NDExNjQ0NTEsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJhY2Nlc3MifQ.V7UP3MHm19Db3P-28ZBCkL4pAZX2T3V-nMk6a9u0S0A"
}
```

# Postman

As previously mentioned, a Postman collection is provided in this repository under the `postman` directory with a list of multiple requests.

<p align="center">
  <img src="./docs/postman.png" alt="OVOS API Postman collection">
</p>

Please follow the [official documentation to import](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-data-into-postman) the Mycroft API Postman collection.

Once the collection has been imported, make sure to update the default variables and to set the right access token.
