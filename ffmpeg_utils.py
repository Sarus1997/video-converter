import shutil
from pathlib import Path

def check_ffmpeg():
    """ตรวจสอบว่า ffmpeg ถูกติดตั้งใน PATH หรือยัง"""
    if shutil.which("ffmpeg") is None:
        print("❌ ERROR: ไม่พบ ffmpeg ในระบบ กรุณาติดตั้งก่อน (https://ffmpeg.org/download.html)")
        raise FileNotFoundError("ffmpeg not found")

def build_ffmpeg_command(input_path: Path, output_path: Path,
                         crf: int = 20, preset: str = "medium",
                         audio_bitrate: str = "128k", threads: int = 0,
                         overwrite: bool = True):
    """สร้างคำสั่ง ffmpeg สำหรับแปลงไฟล์ HEVC → H.264"""
    cmd = ["ffmpeg"]
    cmd.append("-y" if overwrite else "-n")
    cmd += [
        "-hide_banner",
        "-loglevel", "info",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-preset", preset,
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-level", "4.0",
        "-movflags", "+faststart",
        "-c:a", "aac",
        "-b:a", audio_bitrate,
        "-ac", "2"
    ]
    if threads > 0:
        cmd += ["-threads", str(threads)]
    cmd.append(str(output_path))
    return cmd
