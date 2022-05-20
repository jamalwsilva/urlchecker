#!/bin/bash

docker build -t urlchecker:1.0 .
docker run -it urlchecker:1.0 shared_code/urlchecker.py $@
