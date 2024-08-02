clean:
	cd /Users/naoki_mac/workspace/research/Grid-test/python/inout && find . -type f -delete

build:
	docker-compose stop && docker-compose up -d

run:
	@SCRIPT_PATH="bin/test-serenium.py"; \
	CONTAINER_NAME="selenium-python-container"; \
	docker exec -it "$$CONTAINER_NAME" /bin/bash -c "python3 $$SCRIPT_PATH"

stop:
	docker-compose stop
