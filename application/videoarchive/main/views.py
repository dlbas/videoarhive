import os.path
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.template import loader
from django.conf import settings
from django.core.paginator import Paginator

from .models import Video, Thumbnail, EncodedVideo
from .clients import FilestorageClient
from .utils import generate_filename, validate_file
from .tasks import create_thumbnail, create_encoded
from .exceptions import BaseCustomException


def index(request: HttpRequest):
    context = {"videos": []}

    videos = Video.objects.all().order_by("-created")

    for video in videos:
        thumbnails = Thumbnail.objects.filter(
            video=video, width=settings.ENCODING_WIDTH, height=settings.ENCODING_HEIGHT
        )
        encoded_videos = EncodedVideo.objects.filter(
            video=video, width=settings.ENCODING_WIDTH, height=settings.ENCODING_HEIGHT
        )

        webm = encoded_videos.filter(format="webm")
        mp4 = encoded_videos.filter(format="mp4")

        context_element = {"title": video.title, "thumbnails": thumbnails}

        if encoded_videos.count() > 0:
            context_element["encoded_videos"] = {"mp4": mp4, "webm": webm}

        context["videos"].append(context_element)

    context["nginx_base_url"] = settings.NGINX_BASE_URL.rstrip("/")

    paginator = Paginator(context["videos"], 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context["videos"] = page_obj

    template = loader.get_template("index.html")
    return HttpResponse(template.render(context, request))


def post(request: HttpRequest):
    template = loader.get_template("post_video.html")
    return HttpResponse(template.render({}, request))


def posted(request: HttpRequest):
    data = request.POST
    files = request.FILES

    if not data.get("title"):
        return HttpResponseBadRequest("expected title")

    if not files:
        return HttpResponseBadRequest("expected files")

    if len(files) > 1:
        return HttpResponseBadRequest("exactly one file is expected")

    file = files["file"]
    try:
        validate_file(file)
    except BaseCustomException as e:
        return HttpResponseBadRequest(str(e))

    filestorage_client = FilestorageClient(settings.MEDIA_PATH)
    copied_path = filestorage_client.copy_file(
        file, os.path.join("raw", generate_filename())
    )

    video = Video.objects.create(raw_path=copied_path, title=data["title"])

    create_thumbnail.delay(
        video_id=video.id,
        video_path=video.raw_path,
        format=settings.THUMBNAIL_FORMAT,
        width=settings.ENCODING_WIDTH,
        height=settings.ENCODING_HEIGHT,
    )

    for format in settings.ENCODING_FORMATS:
        create_encoded.delay(
            video_id=video.id,
            video_path=video.raw_path,
            format=format,
            width=settings.ENCODING_WIDTH,
            height=settings.ENCODING_HEIGHT,
        )

    template = loader.get_template("video_posted.html")
    return HttpResponse(template.render({}, request))
