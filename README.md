# RASP - A Group Messaging App
Our goal for this project is to create a group messaging app in Flask.
We hope to create a system that allows users to create and 
connect to groups or organizations, send messages to group
chats within the server, and schedule events. The project
will run entirely in a terminal through 
[this](https://github.com/gcallah/TextGame). 
## Required Installations
* [MongoDB Community Edition](https://www.mongodb.com/try/download/community)
  * Please create a database named RASP once installed
  * Make sure to update the environment variable. The path is ...\MongoDB\Server\7.0\bin\

## Project Mockup:
![Project Mockup](https://i.imgur.com/YHBZUQW.png)

## Build
To build production, type `make prod`.

To create the env for a new developer, run `make dev_env`.
