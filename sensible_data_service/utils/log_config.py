BASE_PATH = "/home/riccardo/MODIS/SensibleData-Service/sensible_data_service"

LOGGER_DATABASE = {
	"backend":"mongodb",
	"params": {
		"url":"mongodb://%s:%s@ds029338.mongolab.com:29338/sensible-logger",
		"database":"sensible-logger",
		"collection":"logger-collection",
		"username":"logger",
		"password":"logger"
	}
}

LOGGER_KEYS = {
	"backend":"mongodb",
	"params": {
		"url":"mongodb://%s:%s@ds029338.mongolab.com:29338/sensible-logger",
		"database":"sensible-logger",
		"collection":"logger-keys",
		"username":"logger",
		"password":"logger"
	}
}



D0 = {
	"appID": "fb ",
	"payload": "dummyPayload",
	"userID": "riccardo "
}

Y0 = "THISIS_V0"
Z0 = "THISIS_Z0"
V0 = "THISIS_V0"
A0 = "THIS_IS_A0_THE_SECRET"

FIRST_ENTRY = 0

DIGEST_MODE = "SHA512Hash"
DIGEST_SIZE = "64"

FILE_A = BASE_PATH + "/utils/file_A"
FILE_A_TEMP = BASE_PATH + "/utils/file_A_temp"
