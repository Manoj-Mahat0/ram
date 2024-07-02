from motor.motor_asyncio import AsyncIOMotorClient
import urllib.parse

username = "codeinlastbench"
password = "Picsonix@001$Mj"
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)
MONGO_DETAILS = f"mongodb+srv://{encoded_username}:{encoded_password}@shreeram.k8xmah3.mongodb.net/?retryWrites=true&w=majority&appName=shreeram"

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client["mydatabase"]

users_collection = database.get_collection("users")
