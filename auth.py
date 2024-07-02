from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from models import User, users_collection
from schemas import UserCreate, UserOut
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId
import datetime

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_jwt_secret_key"
ALGORITHM = "HS256"

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    new_user = User(**user_dict)
    await users_collection.insert_one(new_user.dict(by_alias=True))
    return new_user

def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(user)
    access_token = create_access_token(data={"sub": new_user.email})
    return UserOut(email=new_user.email, token=access_token)

@router.post("/login", response_model=UserOut)
async def login(user: UserCreate):
    db_user = await get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user["email"]})
    return UserOut(email=db_user["email"], token=access_token)
