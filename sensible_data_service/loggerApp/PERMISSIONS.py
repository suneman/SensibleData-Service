# Methods:
DROP_DATABASE = "drop_method"
DELETE_ENTRY = "delete_method"
DATAFLOW = "append_dataflow"

# Roles:
ADMIN = {
	"id" : "admin",
	"methods" : 	[
			DROP_DATABASE,
			DELETE_ENTRY
			]
}

USER = {
	"id" : "user",
	"methods" : 	[
			DATAFLOW,
			DELETE_ENTRY
			]
}

OWNER = {
	"id" : "owner",
	"methods" : 	[
			DATAFLOW,
			DELETE_ENTRY
			]
}

USER_ID = USER["id"]
ADMIN_ID = ADMIN["id"]
OWNER_ID = OWNER["id"]
