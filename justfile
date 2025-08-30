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

setup-hel:
  KAMAL_REGISTRY_PASSWORD=`grep -i '^KAMAL_REGISTRY_PASSWORD=' secrets.env | cut -d '=' -f2` kamal setup -d hel

deploy:
  KAMAL_REGISTRY_PASSWORD=`grep -i '^KAMAL_REGISTRY_PASSWORD=' secrets.env | cut -d '=' -f2` kamal deploy

deploy-hel:
  KAMAL_REGISTRY_PASSWORD=`grep -i '^KAMAL_REGISTRY_PASSWORD=' secrets.env | cut -d '=' -f2` kamal deploy -d hel

ssh:
  kamal app exec -i bash

logs:
  kamal app logs -f
