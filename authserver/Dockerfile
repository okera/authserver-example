FROM alpine:3.16.2

ENV PORT=5001
ENV TOKEN_DIR=/tmp/tokens 
ENV SECRET_DIR=/etc/secrets/
ENV PRIVATE_KEY_FILE=${SECRET_DIR}/JWT_PRIVATE_KEY
ENV ALGORITHM=rsa512
ENV GID=okera

RUN set -x \
    && apk update \
    && apk --no-cache add \
        libc6-compat \
        curl \
    && adduser -D -g '' -s /sbin/nologin -u 1000 ${GID}

COPY bin/* /usr/local/bin/

#VOLUME ["${SECRET_DIR}"]

EXPOSE ${PORT}

USER ${GID}

ENTRYPOINT ["entrypoint.sh"]