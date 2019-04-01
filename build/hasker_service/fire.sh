#!/bin/bash

cd /opt/hasker
cp -f /opt/hasker/build/hasker_service/local_settings.py /opt/hasker/Hasker/local_settings.py
python3 /opt/hasker/manage.py migrate 
python3 /opt/hasker/manage.py test
if [[ $? -eq 0 ]]
then
    python3 /opt/hasker/manage.py collectstatic --noinput
    uwsgi --ini /opt/hasker/build/hasker_service/uwsgi.ini --check-static /opt/hasker/staticfiles
fi;
