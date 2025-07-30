from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

# DB
from src.db.session import engine
from src.db.base_class import Base


# Routers
from src.routers import event as eventRoutes
from starlette.middleware.base import BaseHTTPMiddleware



def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    class SecurityHeadersMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            response = await call_next(request)
            # Add headers to every response
            response.headers.update({
                "X-Frame-Options": "DENY",
                "X-XSS-Protection": "1; mode=block",
                "X-Content-Type-Options": "nosniff",
            })
            return response

    # add origins
    origins = [

    ]
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.PROJECT_VERSION, docs_url="/docs", redoc_url=None)

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(
        CORSMiddleware,

        # allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    create_tables()
    return app


app = start_application()

app.include_router(eventRoutes.router)


@app.get("/")
async def root():
    print('Main Application  ------------------------------')

    return {"msg": 'Main App'}
