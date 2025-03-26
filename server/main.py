from fastapi import FastAPI
from ipo_listener import check_for_new_ipos, initialize_tracker

app = FastAPI()

@app.get("/check-ipos")
def check_ipos():
    updated = check_for_new_ipos(limit=10)
    return {"status": "done", "updated": updated}


@app.post("/init-tracker")
def init_tracker():
    count = initialize_tracker()
    return {"message": f"Initialized with {count} IPOs."}
