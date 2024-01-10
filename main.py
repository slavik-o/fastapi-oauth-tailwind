import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

# .env
load_dotenv()

# OAuth
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

# App
app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Views
views = Jinja2Templates(directory="views")

# Middleware
@app.middleware("http")
async def auth_required(request: Request, call_next):
    if not request.url.path.startswith("/auth") and not request.url.path.startswith("/static"):
        if "user" not in request.session:
            return RedirectResponse("/auth")

    return await call_next(request)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("COOKIE_SECRET"))

# Routes
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return views.TemplateResponse(request=request, name="index.html")

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)

    return RedirectResponse(request.url_for("index"))

@app.get("/auth", response_class=HTMLResponse)
def login(request: Request):
    return views.TemplateResponse(request=request, name="login.html")

@app.get("/auth/{provider}")
async def auth(provider: str, request: Request):
    redirect_uri = request.url_for("auth_callback", provider=provider)

    return await getattr(oauth, provider).authorize_redirect(request, redirect_uri)

@app.get("/auth/{provider}/callback")
async def auth_callback(provider: str, request: Request, response: Response):
    token = await getattr(oauth, provider).authorize_access_token(request)

    request.session["user"] = dict(token.get("userinfo"))

    return RedirectResponse(request.url_for("index"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT")))
