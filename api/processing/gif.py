import os
from moviepy.editor import VideoFileClip
from proglog import ProgressBarLogger
from pygifsicle import optimize


class ConvertProgressLogger(ProgressBarLogger):

    """Updates progress of mp4 to gif conversion"""

    def __init__(self, update_progress):
        self.progress_uuid = None
        self.update_progress = update_progress
        super().__init__()

    def set_progress_uuid(self, uuid):

        """ Set progress uuid to use for updating later """

        self.progress_uuid = uuid

    def callback(self, **msg):
        # pylint: disable=unused-argument
        dic = self.state["bars"]
        if len(dic.keys()) <= 0:
            return
        v = list(dic.values()).pop()

        total = v.get("total")
        index = v.get("index")
        self.update_progress(index, total)


def convert_to_gif(uuid, video_filename, update_progress):

    """ Convert video to gif """

    gif_name = os.path.splitext(video_filename)[0] + ".gif"
    clip = VideoFileClip(video_filename)
    #pylint: disable=no-member
    clip.subclip(0, 5)

    if clip.w > 480:
        clip.resize(width=480)
    elif clip.h > 480:
        clip.resize(height=480)

    clip.resize(0.3)
    logger = ConvertProgressLogger(update_progress)
    logger.set_progress_uuid(uuid)
    clip.write_gif(gif_name, fps=15, logger=logger)
    return gif_name


def optimize_gif(gif_filename):

    """ Optimize gif to greatly reduce file size """

    optimize(gif_filename)
