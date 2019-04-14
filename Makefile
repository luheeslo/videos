build_app:
	docker build --no-cache -t videos .

wait_for_mongo:
	until docker-compose run --rm check_mongodb_up > /dev/null; do \
	    echo "Waiting for db to come up..."; \
	done

run_dev_backend:
	docker-compose up -d mongodb

run_dev_server:
	$(MAKE) run_dev_backend
	$(MAKE) wait_for_mongo
	docker-compose up videos

stop_server:
	docker-compose stop	-t 0 videos mongodb
	docker-compose rm -f videos mongodb

run_test_backend:
	docker-compose up -d mongodb_test

wait_for_mongo_test:
	until docker-compose run --rm check_mongodb_test_up > /dev/null; do \
	    echo "Waiting for db to come up..."; \
	done

run_tests:
	$(MAKE) run_test_backend
	$(MAKE) wait_for_mongo_test
	docker-compose up videos_test

stop_mongodb_test:
	docker-compose stop	-t 0 mongodb_test


run_all: run_tests
	run_dev_server




