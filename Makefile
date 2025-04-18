.ONESHELL:
MAKEFLAGS += --no-print-directory

.PHONI: init pytest build-cloud-vpn build-wireguard

init:
	sudo apt update
	sudo apt install -y gnutls-bin wireguard
	sudo apt install -y python3 python3-venv python3-jinja2 python3-netaddr python3-yaml python3-dotenv
	if [ ! -d .venv ]; then
		python3 -m venv .venv
	fi

config-test:
	@python3 -m unittest discover config/test test_*.py config

docker-test:
	@cd test && ./test.sh
