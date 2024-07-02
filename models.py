from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
import urllib.parse

username = "codeinlastbench"
password = "Picsonix@001$Mj"
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)
connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@shreeram.k8xmah3.mongodb.net/?retryWrites=true&w=majority&appName=shreeram"

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: EmailStr
    hashed_password: str

client = AsyncIOMotorClient(connection_string)
database = client.mydatabase
users_collection = database.get_collection("users")
