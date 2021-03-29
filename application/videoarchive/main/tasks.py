import os.path
from django.conf import settings
from celery import shared_task
from .models import Video, Thumbnail, EncodedVideo
from .clients import VideoTranscoder
from .utils import generate_filename


@shared_task
def create_thumbnail(
    *, video_id: int, video_path: str, width=640, height=360, format="png"
):
    transcoder = VideoTranscoder()

    partial_path = os.path.join("thumbnails", generate_filename("." + format))

    thumbnail_path = os.path.join(settings.MEDIA_PATH, partial_path)
    transcoder.create_thumbnail(
        file_path=video_path, thumbnail_path=thumbnail_path, width=width, height=height
    )

    thumbnail = Thumbnail.objects.create(
        video_id=video_id,
        format=format,
        path=partial_path,
        width=width,
        height=height,
    )


@shared_task
def create_encoded(
    *, video_id: int, video_path: str, format: str, width=640, height=360
):
    transcoder = VideoTranscoder()

    partial_path = os.path.join(format, generate_filename("." + format))

    output_path = os.path.join(settings.MEDIA_PATH, partial_path)

    transcoder.create_encoded_video(
        input_path=video_path, output_path=output_path, width=width, height=height
    )

    encoded_video = EncodedVideo.objects.create(
        format=format, width=width, height=height, path=partial_path, video_id=video_id
    )
