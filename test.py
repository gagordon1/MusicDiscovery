import base64
CLIENT_ID = "5361fa0e7d3945f3b78faf916d34e7bb"
CLIENT_SECRET = "e08fd9f28c23451f813b56dca6f31384"
string = "{}:{}".format(CLIENT_ID, CLIENT_SECRET)
dataBytes = string.encode('utf-8')
base64encoded = base64.b64encode(dataBytes)
headers = {"Authorization": "Basic {}".format(base64encoded)}
print(headers)
