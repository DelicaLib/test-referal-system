FROM redis:8.0.3

ARG REDIS_PASSWORD
ARG REDIS_USER
ARG REDIS_USER_PASSWORD

RUN mkdir -p /usr/local/etc/redis && \
    echo "bind 0.0.0.0" > /usr/local/etc/redis/redis.conf && \
    echo "requirepass $REDIS_PASSWORD" >> /usr/local/etc/redis/redis.conf && \
    echo "user $REDIS_USER on >$REDIS_USER_PASSWORD ~* +@all" >> /usr/local/etc/redis/users.acl


CMD [ "redis-server", "/usr/local/etc/redis/redis.conf", "--aclfile", "/usr/local/etc/redis/users.acl"]
