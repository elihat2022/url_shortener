from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.adapters.outbound.sql_adapter import SqlAdapter
from src.domain.services import UrlShortenerService


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://app.elihat.com", "https://short.elihat.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UrlRequest(BaseModel):
    url: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API!"}


@app.post("/convert_url")
def create_short_url(request: UrlRequest) -> dict:
    db_repo = SqlAdapter()
    service = UrlShortenerService(db_repo)
    new_url = service.execute(request.url)
    return {"original_url": request.url, "short_url": new_url.aliases}


@app.get("/{alias}")
def redirect_to_url(alias: str):
    db_repo = SqlAdapter()
    original_url = db_repo.get_url_by_alias(alias)

    if original_url is None:
        raise HTTPException(status_code=404, detail="URL alias not found")

    url_destino = original_url.url_link
    if not url_destino.startswith(("http://", "https://")):
        url_destino = "https://" + url_destino

    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="refresh" content="0;url={url_destino}">
            <title>Redirecting...</title>
        </head>
        <body>
            <p>Redirecting to: <a href="{url_destino}" target="_blank">{url_destino}</a></p>
            <p><small>Opening in new tab...</small></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
