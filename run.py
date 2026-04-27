import uvicorn
import sys
import os

if sys.platform == "win32":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8004, reload=False)
