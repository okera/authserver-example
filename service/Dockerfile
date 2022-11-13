FROM python:3.10.5 AS builder

COPY requirements.txt /requirements.txt
RUN python3 -m venv /venv && \
    /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM python:3.10.5-alpine3.16 AS runner

ENV PORT=5010

COPY --from=builder /venv /venv
COPY ./src /app

RUN apk add --no-cache \
    libstdc++ \
    gcompat \
    curl

EXPOSE ${PORT}

CMD [ "/venv/bin/python", "-u", "/app/service.py" ]