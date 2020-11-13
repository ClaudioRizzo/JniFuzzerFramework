#!/bin/bash
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "usage: $0 host port build<true|false>"
    exit 0
fi

echo "[info] setting PRODUCTION to true"
export PRODUCTION=true

if [ "$3" = "true" ]; then
	echo "[info] building react app"
	cd react_application
	npm install && npm audit fix && npm run build
	cd ..
else
	echo "[info] dkipping build of react app"
fi

echo "[info] trying to start gunicorn with 4 workers"

gunicorn --bind "$1":"$2" --ciphers TLSv1.2 --ssl-version 5 --certfile=./certificates_production/cert.pem --keyfile=./certificates_production/key.pem server:application -w 4 -t 120 --access-logfile server_production.log
