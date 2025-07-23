build:
  docker-compose build --no-cache

start:
  docker compose up --force-recreate -d && docker attach $(docker-compose ps -q article-parser-api)

stop:
  docker compose down

bash:
  docker exec -it qiosq-np4k-article-parser-api-1 bash

# Deploy
setup:
  KAMAL_REGISTRY_PASSWORD=`grep -i '^KAMAL_REGISTRY_PASSWORD=' secrets.env | cut -d '=' -f2` kamal setup

deploy:
  KAMAL_REGISTRY_PASSWORD=`grep -i '^KAMAL_REGISTRY_PASSWORD=' secrets.env | cut -d '=' -f2` kamal deploy

ssh:
  kamal app exec -i bash

logs:
  kamal app logs -f
