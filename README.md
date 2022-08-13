# StoreKeeper API

StoreKeeper is a service to help small stores control their sales, supplies, profit, etc.

## Installation
You need to setup some .env files

**pg.env**
```
POSTGRES_DB=store_keeper
POSTGRES_USER=store_keeper_admin
POSTGRES_PASSWORD=qwerty123
```
**backend.env**
```
SECRET_KEY=YOUR_SUPER_STRONG_SECRET_KEY
```
**Build docker images**
```
docker-compose build
```

## Run application
```
docker-compose up
```