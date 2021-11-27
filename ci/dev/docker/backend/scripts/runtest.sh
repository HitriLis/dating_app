#!/usr/bin/env sh
dockerize -wait tcp://psql:5432
if coverage run --source='.' ./manage.py test; then
  coverage report
  coverage xml
else
  exit 1
fi

