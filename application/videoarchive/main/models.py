from django.db import models


class Video(models.Model):
    title = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    raw_path = models.TextField(null=False)


class VideoFormatChoices(models.TextChoices):
    webm = "webm"
    mp4 = "mp4"


class EncodedVideo(models.Model):
    format = models.TextField(choices=VideoFormatChoices.choices, null=False)
    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    path = models.TextField(null=False)
    video = models.ForeignKey(Video, null=False, on_delete=models.CASCADE)


class ThumbnailFormatChoices(models.TextChoices):
    jpg = "jpg"
    png = "png"


class Thumbnail(models.Model):
    format = models.TextField(choices=ThumbnailFormatChoices.choices, null=False)
    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    path = models.TextField(null=False)
    video = models.ForeignKey(Video, null=False, on_delete=models.CASCADE)
