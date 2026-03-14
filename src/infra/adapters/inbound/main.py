

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from src.infra.adapters.outbound.sql_adapter import SQLAdapter
from src.application.use_cases.shorten_url import UseCaseShortenUrl

app = FastAPI()

class UrlRequest(BaseModel):
    url: str

@app.post("/convert_url")
def create_short_url(request: UrlRequest) -> dict:
    db_repo = SQLAdapter()
    use_case = UseCaseShortenUrl(db_repo)
    
    new_url = use_case.execute(request.url)
    return {"original_url": request.url, "short_url": new_url.aliases}
    

@app.get("/{alias}")
def get_original_url(alias: str) -> dict:
    db_repo = SQLAdapter()
    original_url = db_repo.get_url_by_alias(alias)
    if original_url is None:
        raise HTTPException(status_code=404, detail="URL alias not found")
    return RedirectResponse(url=original_url.url_link, status_code=307)
    

