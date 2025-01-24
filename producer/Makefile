.DEFAULT_GOAL := help

.PHONY: help
help:  ## show this help.
	@grep -e '^\s+:.*?## .*$$' $(firstword $(makefile_list)) | \
		awk 'begin {fs = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: test
test:
	docker compose run --build --rm producer poetry run pytest tests -ra
