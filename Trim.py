import os
from tkinter import PROJECTING
import ffmpeg


def trim(in_file, out_file, start, end):
    if os.path.exists(out_file):
        os.remove(out_file)

    in_file_probe_result = ffmpeg.probe(in_file)
    in_file_duration = in_file_probe_result.get(
        "format", {}).get("duration", None)
    print(in_file_duration)

    input_stream = ffmpeg.input(in_file)

    pts = "PTS-STARTPTS"
    video = input_stream.trim(start=start, end=end).setpts(pts)
    audio = (input_stream
             .filter_("atrim", start=start, end=end)
             .filter_("asetpts", pts))
    video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
    output = ffmpeg.output(video_and_audio, out_file)
    output.run()

    out_file_probe_result = ffmpeg.probe(out_file)
    out_file_duration = out_file_probe_result.get(
        "format", {}).get("duration", None)
    print(out_file_duration)


# last two numbers are time range
trim("example.mov", "out.mov", 10, 60)
