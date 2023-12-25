# RASP - A Messaging App Server
Our project is an API server for a messaging app. It uses Flask-RESTX
to interface with a MongoDB database. The server is tested through Swagger.<br>


## Endpoints Available
<ul>
 <li><strong> deactivate </strong> - deletes a user account</li>
 <li><strong> delete_chatroom </strong> - deletes a chatroom and its associated messages</li>
 <li><strong> delete_msg </strong> - deletes a message by id</li>
 <li><strong> get_chatrooms </strong> - displays all chatrooms</li>
 <li><strong> get_msgs </strong> - displays all messages from a specific room</li>
 <li><strong> get_msgs_test_version </strong> - same as above, but doesn't check for a valid room name to allow for testing</li>
 <li><strong> get_users </strong> - displays all users and their ids</li>
 <li><strong> insert_chatroom </strong> - creates a new chatroom</li>
 <li><strong> register </strong> - creates a new user</li>
 <li><strong> update_chatroom_desc </strong> - updates the chatroom's description</li>
 <li><strong> update_password </strong> - updates a user's password</li>
 <li><strong> update_username </strong> - updates a user's username</li>
 <li><strong> write_message </strong> - inserts a user's message to a specific chatroom</li>
</ul>


## Build
Install requirements with `pip install -r requirements.txt` <br>
To build production, type `make prod`. <br>
To create the env for a new developer, run `make dev_env`. <br>
To run the server type `./local.sh` <br>

## Backup and Restore
To backup the cloud database type `./bkup.sh` <br>
To restore the backup into the local datbaase type `./restore.sh` <br>
Backups are found in db/bkup. This requires the cloud database password.
