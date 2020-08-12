from __future__ import unicode_literals
import os
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from youtube_dl import YoutubeDL, DownloadError
from api.models import Video, Progress
from api.storage.redis_storage import get_status, set_status
from api.processing.gif import convert_to_gif, optimize_gif

dir_path = os.path.dirname(os.path.realpath(__file__))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=dir_path + "/views")


@app.get("/{progress_uuid}/status")
def retrieve_status(progress_uuid: UUID):
    """Get video download/conversion progress"""

    progress = get_status(progress_uuid)
    return {
        "status": progress.status,
        "filename": progress.filename,
        "gif_filename": progress.gif_filename
    }


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request
    })


@app.post("/")
async def post(video: Video, background_tasks: BackgroundTasks):
    """Download video endpoint"""

    progress_uuid = uuid4()
    progress = Progress(
        uuid=progress_uuid,
        status="downloading",
        last_update=datetime.utcnow()
    )

    def update_progress():
        """ Update Redis with new progress """

        if progress.last_update < datetime.utcnow() + timedelta(seconds=2):
            progress.last_update = datetime.utcnow()
            set_status(progress)

    # save downloading status
    update_progress()

    def update_converting_progress(current: int, total: int):
        """ Update status with the converting progress """

        progress.status = "converting"
        progress.current = current
        progress.total = total
        update_progress()

    def progress_hook(data):
        """ Update youtube-dl progress hook """

        progress.filename = data["filename"]
        status = data["status"]

        if status == 'finished':
            progress.status = "converting"
            # start converting to gif
            progress.gif_filename = convert_to_gif(
                progress.uuid, progress.filename, update_converting_progress)
            if video.optimize:
                # status gif optimization
                optimize_gif(progress.gif_filename)
            progress.status = 'finished'
            # save finished status
            update_progress()
        else:
            progress.status = data["status"]

        if status == 'error':
            # save error status
            update_progress()

    ydl_opts = {
        'progress_hooks': [progress_hook],
        'outtmpl': dir_path + '/output/%(title)s.%(ext)s'
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            background_tasks.add_task(ydl.download, [video.url])
            return {"status": "downloading", "id": progress_uuid}
        except DownloadError as download_err:
            progress.status = 'error'
            set_status(progress)  # save error status
            raise HTTPException(
                status_code=500,
                detail="Youtube-dl download error",
                headers={"X-Error": str(download_err)}
            )
        except Exception as exception:
            progress.status = 'error'
            set_status(progress)  # save error status
            raise HTTPException(
                status_code=500,
                detail="Unknown error",
                headers={"X-Error": str(exception)}
            )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
