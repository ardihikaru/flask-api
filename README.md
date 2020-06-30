# Python Flask API Boilerplate

## To Do List

- [x] Base code: Flask App + Swagger UI
- [x] How to install & Run Cockroach Database
- [x] How to install & Run RedisDB
- [ ] How to install & Run Elasticsearch
- [x] Enable auth login and logout
    - [x] Enable connection with RedisDB for storing JWT information
- [x] Integrate with [CockroachDB](https://www.cockroachlabs.com/), e.g., CRUD of `User Model` with CRDB
    - [x] Sample `Create` new user
    - [x] Sample `Read` user all
    - [x] Sample `Read` user by username
    - [x] Sample `Delete` user by username
    - [x] Nested URL input parameters
    - [x] Combination with POST & GET parameters
    - [x] Simple migration (auto add new table model)
    - [ ] Advanced migration (auto detect new update of the table pattern)
- [ ] Integration with [Elasticsearch](https://www.elastic.co/elasticsearch/)
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

3. Install Coachroach Database: [Click here](https://www.cockroachlabs.com/docs/stable/install-cockroachdb.html)

4. Configure CockroachDB:
    1. Follow step [here](https://www.cockroachlabs.com/docs/stable/secure-a-cluster.html) and [here](https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy.html)
    2. Add new user:
        - login: `$ cockroach sql --certs-dir=certs --host=localhost:26257`
        - Create new database: `CREATE DATABASE flaskapi;`
        - Create new user ([Insecure Mode](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster.html)): `CREATE USER flaskuser;`
        - Grant user the database access: `GRANT ALL ON DATABASE flaskapi TO flaskuser;`

## How to use: <TBD>
1. Run RedisDB
    - Go to directory "`others/redis`" : `$ cd others/redis`
    - Instantiate redis container: `$ . run.sh`
    - Test inserting data into RedisDB: `$ . test.sh`
    
2. Run CoachroachDB
    - Instantiate Database server: `$ cockroach start --insecure --listen-addr=localhost`
    - Login SQL: `$ cockroach sql --insecure`
        
3. Run Flask Web Service
    - Run flask web server: `$ flask run`

## Database: Redis Database
RedisDB used only to store JWT-related information
        
## Accessible APIs 
* AUTH
    * `POST /api/auth/login`
    * `GET /api/auth/logout`
    * `GET /api/refresh`
* USER
    * `POST /api/users`
    * `GET /api/users`
    * `DELETE /api/users`
    * `GET /api/users/username/<username>` 
    * `DELETE /api/users/username/<username>`
    * `GET /api/users/hobby/register_between/<start_date>/<end_date>` 
    * `GET /api/users/<hobby>/<register_after>` 
    * `GET /api/users/<user_id>`
    * `PUT /api/users/<user_id>`
    * `DELETE /api/users/<user_id>` 

### Response

```
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
| 403 | `FORBIDDEN` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

## Contributing
Self-Maintained. If there any issue, please do not hesitate to contact me. 

## Contributors
1. Muhammad Febrian Ardiansyah, https://github.com/ardihikaru

## Extra resources
1. **Thread** with `concurrent.futures`; https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
2. **Flask Restplus** in **HTTPS** ; https://stackoverflow.com/questions/47508257/serving-flask-restplus-on-https-server
3. **Monkey patch** : https://github.com/noirbizarre/flask-restplus/issues/54

## License
[MIT](https://choosealicense.com/licenses/mit/)