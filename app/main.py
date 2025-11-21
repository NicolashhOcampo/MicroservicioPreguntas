from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Session
from contextlib import asynccontextmanager
from app.utils.errors import InvalidAuthError
from app.config.db import init_db, get_session
from app.utils.security import isValidToken
from app.routes.question import router as question_router
from app.routes.answers import router as answer_router
from app.rabbit.start_rabbit import start_rabbit_consumers

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_rabbit_consumers()
    yield

app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:5173",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # Skip authentication for documentation routes
    public_routes = ["/docs", "/redoc", "/openapi.json"]

    if request.method == "OPTIONS":
        return await call_next(request)

    if request.url.path in public_routes:
        response = await call_next(request)
        return response
    
    try:
        authorization = request.headers.get("Authorization", "")
        print("Authorization header:", authorization)
        if not authorization:
            raise InvalidAuthError()
        
        user = isValidToken(authorization)
        request.state.user = user
        response = await call_next(request)
        return response
    except InvalidAuthError:
        return JSONResponse(status_code=401, content={"detail": "Invalid authentication"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})




@app.get("/")
async def root(request: Request, session: Session = Depends(get_session)):
    user = request.state.user
    return {
        "message": "Welcome to the Questions and Answers Microservice!",
        "user": user
    }
    
app.include_router(question_router)
app.include_router(answer_router)
