test:
	pytest

test-cov:
	pytest --cov=src tests/

docker-image:
	docker build -t sb-crawler --rm .

docker-run:
	docker run -it --name sb-crawler-app --rm -v ./data:/app/data/ sb-crawler

