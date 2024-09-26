@echo off
start kafka\bin\windows\zookeeper-server-start.bat kafka\config\zookeeper.properties
timeout /t 10 > nul
start kafka\bin\windows\kafka-server-start.bat kafka\config\server.properties