# How to run project

### Step 1.

### Run redis image for channels layer

```shell
docker network create -d bridge redisnet
docker run -d -p 6379:6379 --name wanted_broker_polygon --network redisnet redis
```

### Step 2.
Create .env file on root directory

### Step 3.
```shell
python3 manage.py migrate && python3 manage.py runserver
```

### Step 4.
### Open new terminal
```shell
python3 manage.py runworker polygon
```
### Step 5.
```shell
python3 manage.py connect_polygon
```