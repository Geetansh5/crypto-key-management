from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_db
from .auth import authenticate_user
from .middlewares import AuditLoggingMiddleware
from .routers import keys, policies, audit_logs, compliance

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify allowed origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Session Dependency
@app.middleware("before_request")
async def add_db_session(request: Request):
    request.state.db = get_db()
    response = await call_next(request)
    return response

# Authentication Middleware
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    user = await authenticate_user(request)
    request.state.user = user
    response = await call_next(request)
    return response

# Audit Logging Middleware
app.add_middleware(AuditLoggingMiddleware)

# Exception Handlers
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

# Route Initialization
app.include_router(keys.router)
app.include_router(policies.router)
app.include_router(audit_logs.router)
app.include_router(compliance.router)

# Placeholder for Application Entry Point
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
