# Project 6: Brevet time calculator service
This project is built off of our project 5, and adds some APIs that can retrieve everything in the database, only the open times, or only the close times. You are able to get the data from the APIs in either json or csv format. You can also specify if you want only the top k entries in the database, and you will get a list that is sorted in ascending order of the top k entries. There is a consumer program written in php that requests the data on its own and displays it. The flask application, consumer program, and database are all running in different docker containers that get linked together using docker-compose.yml. 

# Author
Chritopher Barbato
cbarbato@uoregon.edu
