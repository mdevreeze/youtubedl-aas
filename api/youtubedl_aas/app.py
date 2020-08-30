from __future__ import unicode_literals
import os
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import logging
import random
import time
import string
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from youtube_dl import YoutubeDL, DownloadError
from youtubedl_aas.models import Progress, Video
from youtubedl_aas.storage.redis_storage import get_status, set_status
from youtubedl_aas.storage.blob_storage import store_delete_file
from youtubedl_aas.gif_processing import convert_to_gif, optimize_gif

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.warning("App started")

dir_path = os.path.dirname(os.path.realpath(__file__))
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    properties_start = {"rid": idem, "path": request.url, "method": request.method}
    logger.info("Request started", extra=properties_start)
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    properties_end = {
        "rid": idem,
        "completed_in": formatted_process_time,
        "status_code": response.status_code,
    }
    logger.info("Request completed", extra=properties_end)

    return response


@app.get("/{progress_uuid}/status")
def retrieve_status(progress_uuid: UUID):
    """Get video download/conversion progress"""

    progress = get_status(progress_uuid)
    return {
        "status": progress.status,
        "filename": progress.filename,
        "progress": progress.current,
        "progress_total": progress.total,
        "gif_url": progress.gif_url,
        "mp4_url": progress.mp4_url,
    }


@app.get("/")
async def get(request: Request):
    return {"Hello": "World"}


@app.post("/")
async def post(video: Video, background_tasks: BackgroundTasks, req: Request):
    """Download video endpoint"""

    progress_uuid = uuid4()
    progress = Progress(
        uuid=progress_uuid, status="downloading", last_update=datetime.utcnow()
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

        if status == "finished":
            progress.status = "converting"
            # start converting to gif
            progress.gif_filename = convert_to_gif(
                progress.uuid, progress.filename, update_converting_progress
            )
            if video.optimize:
                # status gif optimization
                optimize_gif(progress.gif_filename)
            progress.status = "finished"
            blob_filename = progress.uuid.hex + ".mp4"
            blob_gif_filename = progress.uuid.hex + ".gif"
            progress.mp4_url = store_delete_file(progress.filename, blob_filename)
            progress.gif_url = store_delete_file(
                progress.gif_filename, blob_gif_filename
            )
            # save finished status
            update_progress()
        else:
            progress.status = data["status"]

        if status == "error":
            # save error status
            logger.error("Progress status is in error")
            update_progress()

    ydl_opts = {
        "progress_hooks": [progress_hook],
        "outtmpl": dir_path + "/output/%(title)s.%(ext)s",
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            background_tasks.add_task(ydl.download, [video.url])
            return {"status": "downloading", "id": progress_uuid}
        except DownloadError as download_err:
            progress.status = "error"
            set_status(progress)  # save error status
            logger.exception(download_err)
            raise HTTPException(
                status_code=500,
                detail="Youtube-dl download error",
                headers={"X-Error": str(download_err)},
            )
        except Exception as exception:
            progress.status = "error"
            set_status(progress)  # save error status
            logger.exception(exception)
            raise HTTPException(
                status_code=500,
                detail="Unknown error",
                headers={"X-Error": str(exception)},
            )
