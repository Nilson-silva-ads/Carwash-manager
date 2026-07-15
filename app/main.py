from fastapi import FastAPI

app = FastAPI( 
    title="CarWash Maanger",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message: CarWash Manager Funcionando"
    }