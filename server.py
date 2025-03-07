import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse


DATA_DIR = Path("./assets/data/")
JSON_FILES = ["users.json", "authors.json", "books.json", "reviews.json"]

app = FastAPI()


def read_json(file_name: str) -> dict:
    file_path = DATA_DIR / file_name
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "File not found"}


@app.get("/", response_class=HTMLResponse)
def index():
    links = "".join([f'<li><a href="/{file}">{file}</a></li>' for file in JSON_FILES])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <title>IE API</title>
      </head>
      <body>
        <h1>IE API (Spring 04)</h1>
        <h2>Endpoints:</h2>
        <ul>{links}</ul>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/{file_name}")
def get_json(file_name: str):
    if file_name not in JSON_FILES:
        return JSONResponse(
            content={"error": "Invalid file requested"}, status_code=404
        )
    data = read_json(file_name)
    return JSONResponse(content=data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
