#!/usr/bin/env bash

python3 /opt/hasker/manage.py test
if [[ $? -eq 0 ]]
then

    uwsgi --ini /opt/hasker/build/hasker_service/uwsgi.ini
fi;
