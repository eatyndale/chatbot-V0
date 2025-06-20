from fastapi import FastAPI
from app.router import auth, assessment, chat, eft, progress, crisis
from app.database import engine, Base

# This will create all tables, including the new chat-related ones
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EFT Chatbot API",
    description="Backend services for the EFT (Emotional Freedom Techniques) chatbot.",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api")
app.include_router(assessment.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(eft.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(crisis.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the EFT Chatbot API"}
