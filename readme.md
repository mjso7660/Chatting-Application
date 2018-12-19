to do for db configuration

# 1. Install mongodb

# 2. Turn on mongod

	make sure directory exists for mongod and that the program running has permission
	on windows a folder needs to be created at C:\data\db
	This will fail if mongo does not have permission to create file in C:\

# 3. Run injectusers, injectchatrooms, injectchats in order

	first two operations will take less than 20 min
	the last program will run for around 4 hours - probably because it is not to well optimized

# 4. Create index for chats in mongo shell

	// Indexing for text search
	db.chats.createIndex({chatroom:1,message:"text"})
	// Indexing for date sort query
	db.chats.createIndex({chatroom:1,date:-1})
	// Indexing for users to query chatrooms
	db.chatrooms.createIndex({users:1})

	// this could be used for search of java, coffee, and shop
	db.chats.find( chatroom: ______, { $text: { $search: "java coffee shop" } } )

#5. Once running ...

Log-in page

![Alt text](login.png?raw=true "Title")

Sign-in page

![Alt text](sign_up.png?raw=true "Title")

Chatting page

![Alt text](chat.png?raw=true "Title")
