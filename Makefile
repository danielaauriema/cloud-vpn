.ONESHELL:
MAKEFLAGS += --no-print-directory

ACTIVATE_LINUX:=. .venv/bin/activate

.PHONI: init activate config-test docker-testexit

init:
	@sudo apt update && sudo apt install -y gnutls-bin wireguard python3 python3-venv
	@test -d .venv || python3 -m venv .venv
	@$(ACTIVATE_LINUX)
	@python -m pip install -r requirements.txt

activate:
	@$(ACTIVATE_LINUX)

config-test:
	@python3 -m unittest discover config/test test_*.py config

docker-test:
	@cd test && ./test.sh
