from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import json
from pathlib import Path

app = FastAPI()

# Directory where JSON files are stored
DATA_DIR = Path("./assets/data/")

# JSON file names
JSON_FILES = ["users.json", "reviews.json", "authors.json", "books.json"]


def read_json(file_name):
    file_path = DATA_DIR / file_name
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "File not found"}


@app.get("/", response_class=HTMLResponse)
def home():
    links = "".join([f'<li><a href="/{file}">{file}</a></li>' for file in JSON_FILES])
    html_content = f"""
    <html>
        <head><title>JSON File Server</title></head>
        <body>
            <h1>Available JSON Files</h1>
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
