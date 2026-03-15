

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from src.infra.adapters.outbound.dynamo_adapter import DynamoAdapter
from src.application.use_cases.shorten_url import UseCaseShortenUrl
from mangum import Mangum



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://app.elihat.com", "https://short.elihat.com" ], # Agrega el local y tu futuro dominio
    allow_credentials=True,
    allow_methods=["*"], # Permite POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)


class UrlRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API!"}

@app.post("/convert_url")
def create_short_url(request: UrlRequest) -> dict:
    db_repo = DynamoAdapter()
    use_case = UseCaseShortenUrl(db_repo)
    
    new_url = use_case.execute(request.url)
    return {"original_url": request.url, "short_url": new_url.aliases}
    

@app.get("/{alias}")
def get_original_url(alias: str):
    db_repo = DynamoAdapter()
    original_url = db_repo.get_url_by_alias(alias)

    if original_url is None:
        raise HTTPException(status_code=404, detail="URL alias not found")
    
    url_destino = original_url.url_link

    if not url_destino.startswith(("http://", "https://")):
        url_destino = "https://" + url_destino
    
    return RedirectResponse(url=url_destino, status_code=307)
    
handler = Mangum(app, lifespan="off")

