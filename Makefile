APP_NAME = marketplace
DOCKER_TAG = latest

.PHONY: build
build:
	docker build --tag $(APP_NAME):$(DOCKER_TAG) --target marketplace .

.PHONY: run
run:
	docker run --publish 8888:8888 --name $(APP_NAME) $(APP_NAME):$(DOCKER_TAG)

.PHONY: stop
stop:
	docker stop $(APP_NAME) || echo 0
	docker rm $(APP_NAME) || echo 0

.PHONY: clean
clean:
	docker rmi $(APP_NAME) || echo 0

.PHONY: rebuild
rebuild: stop build run

.PHONY: info
info:
	docker images
	docker ps -a
