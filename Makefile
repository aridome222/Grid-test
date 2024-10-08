clean:
	cd ./python/inout && find . -type f -delete

build:
	docker-compose stop && docker-compose build && docker-compose up -d

up:
	docker-compose stop && docker-compose up -d && python3 python/bin/local_server.py

run: clean mkdir
	@SCRIPT_PATH="bin/test-selenium.py"; \
	CONTAINER_NAME="selenium-python-container"; \
	docker exec -it "$$CONTAINER_NAME" /bin/bash -c "python3 $$SCRIPT_PATH"

stop:
	docker-compose stop

mkdir:
	@if [ ! -d "/Users/youtome/dev/research/Grid-test/python/inout" ]; then \
		mkdir -p "/Users/youtome/dev/research/Grid-test/python/inout"; \
		echo "Directory created: /Users/youtome/dev/research/Grid-test/python/inout"; \
	else \
		echo "Directory already exists: /Users/youtome/dev/research/Grid-test/python/inout"; \
	fi
