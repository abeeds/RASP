# RASP
RASP is a messaging application. This repository contains the source code for our Flask-RestX backend, which interacts with a MongoDB database. 

# Frontend Repository
You can find the React front-end repository [here](https://github.com/abeeds/RASP_Front_End).

# Endpoints Available
## Chatrooms
### GET - `/chatrooms`
- Returns the rooms as a list of objects.
- Does not take any request body.
- Sample return: `Room_name: { description: ________ }`

### POST - `/chatrooms`
- Creates a chatroom.
- Takes the following fields in the JSON request body:
  - "chatroom_name": "string"
  - "description": "string"
  - "owner": "string"

### PUT - `/chatrooms`
- Updates the description of an existing chatroom.
- Takes the following fields in the JSON request body:
  - "chatroom_name": "string"
  - "description": "string"

### DELETE - `/chatrooms/{room_name}`
- Deletes the specified chatroom.

## Messages
### GET - `/messages/{room_name}`
- Returns all messages from the specified chatroom.
- Sample return:
  -  `id: {
"Chatroom": ______,<
"User": ______,
"Timestamp: ______,
"Content": ______
}`

### POST - `/messages`
- Posts a message to a specific chatroom.
- Takes the following fields in the JSON request body:
  - "chatroom_name": "string"
  - "username": "string"
  - "content": "string"

### PUT - `/messages`
- Updates a specific message, specified by its "_id".
- Takes the following fields in the JSON request body:
  - "_id": "string"
  - "content": "string"

### DELETE - `/messages/{msg_id}`
- Deletes a message by its specified id.

## Users
### GET - `/users`
- Returns all users accounts.
- Sample return: `{"Username": {"_id": id}}`

### GET - `/users/login/{username}/{password}`
- Verifies the users login with a username and password.
- A proper post version of this is implemented but not integrated into the project.

### POST - `/users/register/{username}/{password}`
- Creates an account with the specified username and password.

### PUT - `/users/update_password`
- Takes the following fields in the JSON request body:
  - "user": "string"
  - "newUser": "string"
  - "pwd": "string"

### PUT - `/users/update_username`
- Takes the following fields in the JSON request body:
  - "user": "string"
  - "oldpwd": "string"
  - "newpwd": "string"
  - "newpwdConfirm": "string"

### DELETE - `/users/ban/{username}`
- Bans/Deletes the specified user's account.

### DELETE - `/users/deactivate/{username}/{password}`
- Deletes the user's account.

## Forms
### GET - `/forms/{form_name}`
- This is used to implement HATEOAS into the project. A form will be generated based on the whichever form is requested.

# Build
- Install requirements with `pip install -r requirements.txt`
- To build production, type `make prod`.
- To create the env for a new developer, run `make dev_env`.
- run `export CLOUD_MONGO=0` to configure for a local database
- run `export CLOUD_MONGO=1` to configure for a local database
  - this will require you to also set `GAME_MONGO_PW`
- To run the server type `./local.sh`

# Backup and Restore
- To backup the cloud database type `./bkup.sh` <br>
- To restore the backup into the local database type `./restore.sh` <br>
- Backups are found in db/bkup. This requires the cloud database password.
