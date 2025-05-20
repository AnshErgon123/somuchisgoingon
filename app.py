from fastapi import FastAPI
import uvicorn

# Create the FastAPI app
app = FastAPI()

# Define a sample route
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# This block runs the server if you execute the file directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
