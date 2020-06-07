# Flask-API

## TO DO LIST

- [x] Base code: Flask App + Swagger UI
- [x] How to install & Run Cockroachdb (CRDB)
- [x] How to install & Run RedisDB
- [x] Enable auth login and logout
    - [x] Enable connection with RedisDB for storing JWT information
- [x] Integrate with CRDB, e.g., CRUD of `User Model` with CRDB
    - [x] Sample `Create` new user
    - [x] Sample `Read` user all
    - [x] Sample `Read` user by username
    - [x] Sample `Delete` user by username
- [x] Complete documentation

## Included components
1. Python Flask
2. Swagger UI
3. Redis Database
4. Cockroach Database

## Requirements
1. Python 3, https://www.python.org/download/releases/3.0/
2. Python Flask Web Server, http://flask.pocoo.org
3. Redis Key-Value Database, https://redis.io

## Installation
1. Python library 
    ```
    pip install -r requirements.txt
    ```
2. Install Redis Database
    1. Install docker.io
    2. Install redis-tools
    3. Go to redis directory: `$ cd others/redis`
    4. Install `Dockerfile`: `$ docker build -t 5g-dive/redis:1.0 .`
    5. Instantiate redis container: `. run.sh`
    5. Test insert data into RedisDB: `. test.sh`
3. Install Coachroach Database
    - [MAC OS](https://kb.objectrocket.com/cockroachdb/how-to-install-cockroachdb-on-mac-os-x-307)
    - WINDOWS
    - LINUX
4. Configure CockroachDB:
    1. Follow step [here](https://www.cockroachlabs.com/docs/stable/secure-a-cluster.html) and [here](https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy.html)
    2. Add new user:
        - login: `$ cockroach sql --certs-dir=certs --host=localhost:26257`
        - Create new database: `CREATE DATABASE flaskapi;`
        - Create new user: 
            - Insecure Mode: `CREATE USER flaskuser;`
            - Secure Mode: `CREATE USER flaskuser WITH PASSWORD 'bismillah';`
        - Grant user the database access: `GRANT ALL ON DATABASE flaskapi TO flaskuser;`
    3. Generate cert: `cockroach cert create-client flaskuser --certs-dir=certs --ca-key=my-safe-directory/ca.key`

## How to use: <TBD>
1. Run RedisDB
2. Run CoachroachDB
    - [Insecure](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster.html) (For newbie):
        - RUN: `$ cockroach start --insecure --listen-addr=localhost`
        - Login SQL: `$ cockroach sql --insecure`
    - [Secure](https://www.cockroachlabs.com/docs/stable/secure-a-cluster.html) (Recommended):
        - RUN: <Please follow the steps from the given link above>
            - Node 1: 
                ``` 
                cockroach start \
                    --certs-dir=certs \
                    --store=node1 \
                    --listen-addr=localhost:26257 \
                    --http-addr=localhost:8080 \
                    --join=localhost:26257,localhost:26258,localhost:26259 \
                    --background
                ```
            - Node 2: 
                ``` 
                cockroach start \
                    --certs-dir=certs \
                    --store=node2 \
                    --listen-addr=localhost:26258 \
                    --http-addr=localhost:8080 \
                    --join=localhost:26257,localhost:26258,localhost:26259 \
                    --background
                ```
            - Node 3: 
                ``` 
                cockroach start \
                    --certs-dir=certs \
                    --store=node3 \
                    --listen-addr=localhost:26259 \
                    --http-addr=localhost:8080 \
                    --join=localhost:26257,localhost:26258,localhost:26259 \
                    --background
                ```
             - Run `Secure Mode`: `$ cockroach init --certs-dir=certs --host=localhost:26257`
                - Check status: `$ grep 'node starting' node1/logs/cockroach.log -A 11` 
        - Login SQL: `$ cockroach sql --certs-dir=certs --host=localhost:26257`
3. Run Flask Web Service

## Database: Redis Database
RedisDB used only to store JWT-related information
        
## Accessible APIs 
* AUTH
    * `POST /api/auth/login`
    * `GET /api/auth/login`
    * `GET /api/auth/logout`
    * `GET /api/refresh`
* USER
    * `GET /api/user`
    * `POST /api/user`
    * `GET /api/user/<username>` 
    * `DELETE /api/user/<username>` 

### Response

```javascript
{
  "status"  : bool,
  "message" : string,
  "results" : `LIST` or `DICT`
}
```

## Status Codes

This Web Service returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |
| 401 | `Unauthorized Access. Access Token should be provided and validated.` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

NB: More detail information regarding API Documentation please refer to [Here](https://gitlab.com/idn-games/idn-games-web-service/app/controllers/api/README.md).

## Contributing
Self-Maintained. If there any issue, please do not hesitate to contact me. 

## Contributors
1. Muhammad Febrian Ardiansyah, https://gitlab.com/ardihikaru

## Extra resources
1. **Thread** with `concurrent.futures`; https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
2. **Flask Restplus** in **HTTPS** ; https://stackoverflow.com/questions/47508257/serving-flask-restplus-on-https-server
3. **Monkey patch** : https://github.com/noirbizarre/flask-restplus/issues/54
4. About Redis (Tested on **Ubuntu**):
    * Restart Redis: `sudo service redis-server restart`
    * Redis Cli: `redis-cli`
    * Redis Conf file: `sudo vi /etc/redis/redis.conf`
    * Setting up password in Redis.
        * Open Conf file in `sudo vi /etc/redis/redis.conf`
        * Uncomment and Edit this line `requirepass <password>`
        * Example usage: `requirepass bismillah`
    * Flask-Redis Doc: 
        * Flask Redis. https://github.com/underyx/flask-redis
        * Redis Expire. https://redis.io/commands/expire
        * Delete Keys. https://www.shellhacks.com/redis-delete-all-keys-redis-cli/
            * `redis-cli FLUSHDB`
            * `redis-cli -n DB_NUMBER FLUSHDB`
            * `redis-cli -n DB_NUMBER FLUSHDB ASYNC`
            * `redis-cli FLUSHDB`
            * `redis-cli FLUSHALL`
            * `redis-cli FLUSHALL ASYNC`
         * Snippet Code in OpenSuse.
            * `systemctl daemon-reload`
            * `sudo redis-server /etc/redis/default.conf`
            * `sudo vi /etc/redis/default.conf`
            * `redis-cli`
            * `systemctl start redis@default`
            * `systemctl restart redis.target`
            * `systemctl enable redis@default`
            * `sudo vi /etc/systemd/system/redis@default.service.d/limits.conf`
    * Common Issues in Redis.
        * Decode Redis Response: https://stackoverflow.com/questions/33338801/how-to-decode-redis-responses-in-flask/33338802

## License
[MIT](https://choosealicense.com/licenses/mit/)