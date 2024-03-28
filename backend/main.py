from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/api/graph")
async def read_item():
    return [
        {
            "source": "Microsoft",
            "target": "Amazon",
            "type": "licensing",
        },
        {
            "source": "Microsoft",
            "target": "HTC",
            "type": "licensing",
        },
        {
            "source": "Samsung",
            "target": "Apple",
            "type": "suit",
        },
        {
            "source": "Motorola",
            "target": "Apple",
            "type": "suit",
        },
    ]

# app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="static")
