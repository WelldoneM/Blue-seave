#!/bin/bash
#
# Linux/Mac BASH script to build docker container
#
docker rmi blueseave-app-client
docker build -t blueseave-app-client .
