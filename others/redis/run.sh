docker run -d \
  -h redis \
  -e REDIS_PASSWORD=bismillah \
  -p 6379:6379 \
  --name redis \
  --restart always \
  myredisdb/redis:1.0 /bin/sh -c 'redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}'
