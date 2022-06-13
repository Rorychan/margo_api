# MakeUP Show API
 This API p basically is a clone of [MakeupApi](https://makeup-api.herokuapp.com), but it suppors some additional features like adding users, authorization, making orders and etc.
 
For now it is using SQLite as a database, you can find raw db file here with all products and categories, but without users

## How to use this api
1. Clone this repository
2. From the repository directory run `docker-compose up`
3. That's it api is working under [http://localhost:8000](http://localhost:8000)

### Important
After deploying, the db file will be updated by your requests, if you want to keep it raw, remove volumes part from `docker-compose.yaml`