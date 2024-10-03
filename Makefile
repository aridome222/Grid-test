clean:
	cd ./python/inout && find . -type f -delete

build:
	docker-compose stop && docker-compose build && docker-compose up -d

up:
	docker-compose stop && docker-compose up -d && python3 python/bin/local_server.py

run:
	@SCRIPT_PATH="bin/test-selenium.py"; \
	CONTAINER_NAME="selenium-python-container"; \
	docker exec -it "$$CONTAINER_NAME" /bin/bash -c "python3 $$SCRIPT_PATH"

stop:
	docker-compose stop
