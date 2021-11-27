#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=test-user.settings
pylint --rcfile=.pylintrc `ls`
