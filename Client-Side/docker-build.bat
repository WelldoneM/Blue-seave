@echo off
REM
REM Windows BATCH script to build docker container
REM
@echo on
docker rmi blueseave-app-client
docker build -t blueseave-app-client .
