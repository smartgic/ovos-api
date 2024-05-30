<p align="center">
    <em>Expose a secure REST API on top of Open Voice OS core to perform actions on your instance without to SSH into it.</em>
</p>

[![Docker pulls](https://img.shields.io/docker/pulls/smartgic/mycroft-api.svg?style=flat&logo=docker&logoColor=FFFFFF&color=87567)](https://hub.docker.com/r/smartgic/mycroft-api)
 [![License: Apache 2.0](https://img.shields.io/badge/License-Apache2.0-yellow.svg)](https://opensource.org/license/apache-2-0) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-pink.svg?style=flat)](https://github.com/smartgic/mycroft-api/pulls) [![Discord](https://img.shields.io/discord/809074036733902888)](https://discord.gg/sHM3Duz5d3)

---

OVOS API goal is to provide a layer on top of Open Voice OS Core to perform actions such as:

* Install or uninstall skills
* Retrieve information *(version, location, name, etc...)*
* Reload configuration to notify services if a change occurred
* Delete TTS cache files
* Microphone mute and un-mute *(software)*
* Stop any speech or audio output
* And more!

Here is a quick list of use cases where the API could be used:

* Install or uninstall skills remotely
* Monitoring and get information
* Interface other IoT devices with Mycroft
* Ask for speech from remote sources
* Connect buttons to trigger actions such as `stop` or `listen`
* Update skills via an external scheduler
* The sky is the limit...

# Architecture

In order to interface with Open Voice OS core instance, the API connects to the core messages bus to send and receive messages. Some messages used by this API are native to the core such as `stop`, `mycroft.skills.list`, etc... but most of the messages used are custom for the API requirements such as `ovos.api.skill_settings`, `ovos.api.websocket`, etc...

The API will send messages to the bus but for non-native messages a skill is required on the core to interpret these messages. This is why the [`skill-rest-api`](https://github.com/smartgic/mycroft-rest-api-skill) skill should be installed on the core. The API and the skill authenticate via an API key shared between both of them.

The `API_KEY` needs to be defined within the `.env` file and this same key must be defined on [home.mycroft.ai](https://home.mycroft.ai) *(see the skill README for more information)*.

<p align="center">
  <img src="./docs/flow.png" alt="Mycroft API Flow">
</p>

To consume the API a user is required, this user will allow to retrieve a JSON Web Token *(`JWT`)* using a basic authentication method. Once the authentication has been validated an access and a refresh tokens will be provided.

# Install

Python `virtualenv` is always a good practice to keep a clean environment but it is not a mandatory step.

```bash
git clone https://github.com/smartgic/ovos-api.git
cd ovos-api
mkdir ~/virtualenvs
python -m venv ~/virtualenvs/ovos-api
. ~/virtualenvs/ovos-api/bin/activate
pip install -r requirements.txt
```

# Configuration

Before starting the API, some configuration must be applied to the `.env` file.

```ini
SECRET=""
WS_HOST="10.12.50.20"
WS_PORT="8181"
API_KEY=""
USERS_DB="/users.json"
```

| Variable   | Explaination                                           |
| ---        | ---                                                    |
| `SECRET`   | String used to generate the JWT token                  |
| `WS_HOST`  | IP address or hostname of the Mycroft messages bus     |
| `WS_PORT`  | TCP Port of the Mycroft messages bus                   |
| `API_KEY`  | Key used between the API and the skill to authenticate |
| `USERS_DB` | File where users are declared with status and password |

The `USERS_DB` should match a path to an existing JSON file that looks like this:

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

The `password` field is encrypted using the `bcrypt` Python library *(part of the `requirements.txt` file)*. Use the `genpass.py` Python wrapper to generate the password as demonstrated below.

```bash
. ~/virtualenvs/mycroft-api/bin/activate
pip install argparse
python genpass.py --password c-h-a-n-g-e-m-e

```

The wrapper should return a string like this: `$2b$12$USwu6HcOXJV6u0Xpsa/2DOkS5Js8YizdeGUn.NdiYlywx9fUaVp1i`

# Start the API

`uvicorn` *(part of the `requirements.txt` file)* is used to serve the API requests, by default it looks for a `.env` file and if it exists then the variables will be passed to the application.

```bash
cd mycroft-api
uvicorn app.api:app --host 10.12.50.21 --port 8000
```

`--host` and `port` arguments are only used to define how to expose the API, here the API will listen only on `10.12.50.21` address and port `8000`.

# Docker

`Dockerfile` and `docker-compose.yml` files are provided to use this API with Docker.

### Supported architectures and tags

| Architecture | Information                                        |
| ---          | ---                                                |
| `amd64`      | Such as AMD and Intel processors                   |
| `arm/v6`     | Such as Raspberry Pi 1                             |
| `arm/v7`     | Such as Raspberry Pi 2/3/4                         |
| `arm64`      | Such as Raspberry Pi 4 64-bit                      |

*These are examples, many other boards use these CPU architectures.*

| Tag | Description                                                                         |
| --  | ---                                                                                 |
| `stable`/`latest`  | The latest stable version based on the `main` branch                  |

The `docker-compose.yml` contains variables that will loaded from the `.env` file. As for the users, the file will be mounted as a volume within the container.

```bash
cd ovos-api
docker-compose --env-file .env up -d
```

This command will download the `smartgic/ovos-api:latest` Docker image from Docker Hub and create the `ovos_api` Docker container.

# Consume the API

To consume the API you could use different tools from the very basic but powerful such as `curl` or something more user friendly like Postman *(a collection is provided, more about it below)*. Once the API is up and running, you could get the complete list of the available endpoints at http://10.12.50.21:8000/docs *(replace with your IP address and port)*.

<p align="center">
  <img src="./docs/swagger.png" alt="Mycroft API Swagger">
</p>

Here are some `curl` examples toe retrieve tokens, information, stop audio output, and more!

## Retrieve tokens

```bash
curl -s -H "Content-Type: application/json" -d '{"user": "mycroft", "password": "c-h-a-n-g-e-m-e"}' -X POST http://10.12.50.21:8000/v1/auth/tokens
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNjQxMTY1MDA4LCJpYXQiOjE2NDExNjMyMDgsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJhY2Nlc3MifQ.iIXr0NhYo9A5X9xI06UjVWw8FDGm1ZC4AD8fuBFM2mQ",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNzE4OTIzMjA4LCJpYXQiOjE2NDExNjMyMDgsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJyZWZyZXNoIn0._bp2FUqAzoPWzgDHOlkjIfZvb76BdY6nShqDV1_lJPk"
}
```

If the basic authentication worked then two tokens will be returned:

1. An access token to consume the API only valid 30 minutes *(could be change in `config.py`)*
2. A refresh token valid 6 hours *(could be change in `config.py`)* to refresh an access token without the user and password

## Retrieve system information

```bash
curl -s -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNjQxMTY1MDA4LCJpYXQiOjE2NDExNjMyMDgsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJhY2Nlc3MifQ.iIXr0NhYo9A5X9xI06UjVWw8FDGm1ZC4AD8fuBFM2mQ" -X GET http://10.12.50.21:8000/v1/system/info
{
  "results": {
    "core_version": "21.2.2",
    "device_uuid": "74318843-0812-4903-a1c2-36da5a98e041",
    "name": "docker",
    "audio_backend": "vlc",
    "city": "Montréal",
    "country": "Canada",
    "lang": "en-us",
    "platform": "mycroft_mark_2",
    "timezone": "America/Toronto",
    "tts_engine": "mimic2"
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

## Update all installed skills

```bash
curl -s -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJteWNyb2Z0IiwiZXhwIjoxNjQxMTY1MDA4LCJpYXQiOjE2NDExNjMyMDgsImlzcyI6Im15Y3JvZnQtYXBpIiwic2NvcGUiOiJhY2Nlc3MifQ.iIXr0NhYo9A5X9xI06UjVWw8FDGm1ZC4AD8fuBFM2mQ" -X PUT -I http://10.12.50.21:8000/v1/skills/update
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
  <img src="./docs/postman.png" alt="Mycroft API Postman collection">
</p>

Please follow the [official documentation to import](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-data-into-postman) the Mycroft API Postman collection.

Once the collection has been imported, make sure to update the default variables and to set the right access token.
