#!/bin/bash

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ -e /$CONTAINER_FIRST_STARTUP ]; then
	
	echo >&2 "The database was already initialized before. Skipping script execution."

else

	while ! nc -z mongodb 27017; do
		echo >&2 "Waiting for database"
		sleep 1
	done
	
	while ! nc -z elasticsearch 9200; do
		echo >&2 "Waiting for elasticsearch"
		sleep 1
	done

	python3 /populate.py

	touch /$CONTAINER_FIRST_STARTUP
	echo >&2 "Saving control file. DO NOT DELETE THIS FILE!"

fi
