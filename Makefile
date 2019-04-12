wait_for_mongo:
	until docker-compose run --rm check_mongodb_up > /dev/null; do \
	    echo "Waiting for db to come up..."; \
	done

run_backend:
	docker-compose up -d mongodb
	$(MAKE) wait_for_mongo

run_server:
	$(MAKE) wait_for_mongo
	docker-compose up videos

stop_server:
	docker-compose stop	-t 0 videos mongodb
	docker-compose rm -f videos mongodb




