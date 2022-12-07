
import uvicorn
import appeal 
uvicorn.run("appeal:app", host="localhost", port=5000, log_level="info")