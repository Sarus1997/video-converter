import subprocess
from pathlib import Path
from ffmpeg_utils import build_ffmpeg_command

def run_command(cmd):
    """รันคำสั่ง ffmpeg และแสดงผล"""
    print("▶️ Running:\n", " ".join(cmd))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    try:
        for line in process.stdout:
            print(line, end="")
    except KeyboardInterrupt:
        print("\n⛔ ถูกยกเลิกโดยผู้ใช้")
        process.terminate()
        process.wait()
        raise
    return process.wait()

def convert_one(input_path: Path, output_path: Path, **kwargs):
    """แปลงไฟล์เดี่ยว"""
    if not input_path.exists():
        print(f"❌ ERROR: ไม่พบไฟล์ {input_path}")
        return 2
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_ffmpeg_command(input_path, output_path, **kwargs)
    rc = run_command(cmd)
    if rc == 0:
        print(f"✅ แปลงเสร็จเรียบร้อย: {output_path}")
    else:
        print(f"⚠️ ffmpeg error code {rc}")
    return rc

def batch_convert(folder: Path, ext_list=None, **kwargs):
    """แปลงทุกไฟล์ในโฟลเดอร์"""
    if ext_list is None:
        ext_list = [".mkv", ".mp4", ".mov", ".ts", ".hevc", ".265", ".h265"]
    files = sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in ext_list])
    if not files:
        print("⚠️ ไม่พบไฟล์วิดีโอในโฟลเดอร์นี้")
        return
    for inp in files:
        out = inp.with_suffix(".mp4")
        if out.exists():
            print(f"⏩ ข้าม (ไฟล์นี้มีอยู่แล้ว): {out.name}")
            continue
        print(f"\n🎞️ กำลังแปลง {inp.name} → {out.name}")
        rc = convert_one(inp, out, **kwargs)
        if rc != 0:
            print("❌ หยุดการแปลงเนื่องจากเกิดข้อผิดพลาด")
            break
