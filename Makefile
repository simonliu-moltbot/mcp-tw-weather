IMAGE_NAME=mcp-tw-weather
PORT=8000

.PHONY: build run dev dev-http

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -p $(PORT):$(PORT) --env-file .env $(IMAGE_NAME)

dev:
	python src/server.py --mode stdio

dev-http:
	python src/server.py --mode http --port $(PORT)
