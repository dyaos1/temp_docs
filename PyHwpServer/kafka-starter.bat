@echo off
start bin\windows\zookeeper-server-start.bat config\zookeeper.properties
timeout /t 10 > nul
start bin\windows\kafka-server-start.bat config\server.properties