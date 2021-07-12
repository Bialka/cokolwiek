import json
import subprocess


def get_file_info(file_path):
    proc = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", file_path],
                          stdout=subprocess.PIPE)
    file_info = proc.stdout.decode("utf-8")
    data = json.loads(file_info)
    return data["format"]