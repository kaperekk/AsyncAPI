from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from API_handler import get_wiki_pages

app = FastAPI()


@app.get("/random_wikipedia_pages/{N}", response_class=HTMLResponse)
async def get_random_wikipedia_pages(N: int):
    html_content = await get_wiki_pages(N=N)

    return html_content
