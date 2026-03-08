from fastapi import FastAPI,Request,Depends,HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from jose import jwt,JWTError
import datetime
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials 

app = FastAPI()
SECRET_KEY = "#123MYAPP@$^"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Swagger UI Bearer token input
bearer_scheme = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    # Convert to bytes and truncate to 72 bytes
    password_bytes = password[:72]
    # Hash with bcrypt
    return pwd_context.hash(password_bytes)


def verify_password(plain, hashed):
    plain_pw = plain[:72]
    return pwd_context.verify(plain_pw, hashed)


def create_token(data):

    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token


def verify_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms="HS256")
        return payload.get('user_id')
    except JWTError:
        return None

@app.middleware("http")
async def authMiddleware(request:Request,call_next):
    exceptPaths = ['/register','/docs','/login','/','/openapi.json']

    if any(request.url.path.startswith(path) for path in exceptPaths):
        return await call_next(request)

    header = request.headers.get('Authorization')
    if not header or not header.startswith('Bearer '):
        return JSONResponse(status_code="401",detail="unauthorized request")

    token = header.split(" ")[1]
    user = verify_token(token)
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    request.state.user_id = user
    response = await call_next(request)
    return response 


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    user_id = verify_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id



        
