from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# Simple session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="trade-general-secret"
)

templates = Jinja2Templates(directory="templates")

# TEMP users (you control this)
USERS = {
    "akhil": "akhil123"
}

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None}
    )

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if USERS.get(username) != password:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid username or password"
            }
        )

    request.session["user"] = username
    return RedirectResponse("/dashboard", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user
        }
    )

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)
