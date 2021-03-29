import ffmpeg
import os
import os.path


class FilestorageClient:
    def __init__(self, base_path):
        self.base_path = base_path

    def copy_file(self, file_object, path: str):
        path = os.path.join(self.base_path, path)

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        with open(path, "wb+") as destination:
            for chunk in file_object.chunks():
                destination.write(chunk)

            return path


class VideoTranscoder:
    def get_video_info(self, file_path: str):
        probe = ffmpeg.probe(file_path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )
        width = int(video_stream["width"])
        height = int(video_stream["height"])
        duration = float(video_stream["duration"])

        return {"width": width, "height": height, "duration": duration}

    def create_thumbnail(
        self, *, file_path: str, thumbnail_path: str, width: int, height: int
    ):
        if not os.path.exists(os.path.dirname(thumbnail_path)):
            os.makedirs(os.path.dirname(thumbnail_path))

        info = self.get_video_info(file_path)
        size = f"{width}x{height}"

        thumbnail_position = int(info["duration"] / 2)

        (
            ffmpeg.input(file_path, ss=str(thumbnail_position))
            .output(thumbnail_path, vframes=1, s=size)
            .run()
        )

    def create_encoded_video(
        self, *, input_path: str, output_path: str, width: int, height: int
    ):
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        size = f"{width}x{height}"

        (ffmpeg.input(input_path).output(output_path, s=size).run())
