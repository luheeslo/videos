#!/bin/sh
if [ "$1" != "test" ]; then 
    env/bin/pytest --cov --cov-report=term-missing
else
    env/bin/pserve development.ini --reload
fi
