# JWT service

Service for generating and refreshing JWTs.


## Install and run 

### 1. Clone repo:

```shell
git clone git@github.com:TeamSchedule/jwt.git
```

### 2. Run service:

#### 2.1 Run with docker:<br/>

```shell
docker build --tag jwt:latest -f Dev.dockerfile .
```

```shell
docker run --rm -it -p 8082:8082 jwt:latest
```

#### 2.2 Run with python (poetry):<br/>
```shell
make install
```

```shell
make env
```

```shell
make run
```

## OpenApi doc
Open in browser:

`http://localhost:8082/swagger`

or

`http://localhost:8082/openapi`
