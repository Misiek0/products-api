1. connecting to docker container
docker compose exec db psql -U POSTGRES_PASSWORD -d products_db

2. querying
remember about semicolon(;) at the end of query
select * from products;