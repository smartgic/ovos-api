FROM python:3.10

LABEL vendor=Smartgic.io \
  io.smartgic.maintainer="Gaëtan Trellu <gaetan.trellu@smartgic.io>" \
  io.smartgic.image-name="ovos-api" \
  io.smartgic.is-beta="no" \
  io.smartgic.is-production="yes" \
  io.smartgic.version="${TAG}" \
  io.smartgic.release-date="2024-05-26"

EXPOSE 8000

RUN useradd --no-log-init mycroft -m

USER mycroft

ENV PATH $PATH:/home/mycroft/.local/bin

RUN pip install -U pip fastapi uvicorn passlib[bcrypt] pyjwt python-decouple websocket-client

COPY ./app /app

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]