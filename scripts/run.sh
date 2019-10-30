docker stop collector receiver redis_service

docker rm $(docker ps -a -q)

docker image build . -t gloop
docker run -d -p 8080:8080 --name=receiver gloop
docker run -dp 6379:6379 --name=redis_service redis:5.0.6-alpine
docker run -d --name=collector gloop

docker exec -d receiver python -m gloop.match_starter.player_receiver
docker exec -d collector python -m gloop.match_starter.player_collector
