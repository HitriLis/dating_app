#!/usr/bin/env sh

set -e

# Ожидаем запуска postgres и tarantool
DB_HOST=`echo ${DSN__DATABASE} | sed -r 's/.*@([^:]+):.*/\1/'`
DB_PORT=`echo ${DSN__DATABASE} | sed -e 's,^.*:,:,g' -e 's,.*:\([0-9]*\).*,\1,g' -e 's,[^0-9],,g'`

#dockerize -wait tcp://${DB_HOST}:${DB_PORT}

# Миграция и синхронизация
./manage.py migrate --noinput

# Запуск команды
./manage.py runserver 0.0.0.0:8000
