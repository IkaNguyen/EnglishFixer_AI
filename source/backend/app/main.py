from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import writing

app = FastAPI(title="Fixer AI API")

# --- Cấu hình CORS ---
origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Cho phép tất cả methods (GET, POST, v.v.)
    allow_headers=["*"], # Cho phép tất cả headers
)

# --- Thêm router ---
app.include_router(writing.router, prefix="/api/v1", tags=["writing"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Writing Tutor API"}