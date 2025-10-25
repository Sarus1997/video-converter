import sys
from pathlib import Path
import argparse
from ffmpeg_utils import check_ffmpeg
from converter import convert_one, batch_convert

def parse_args():
    parser = argparse.ArgumentParser(description="แปลง HEVC (H.265) → MP4 (H.264 + AAC)")
    parser.add_argument("input", help="ไฟล์ต้นฉบับ หรือ โฟลเดอร์ (เมื่อใช้ --batch)")
    parser.add_argument("output", nargs="?", help="ชื่อไฟล์ปลายทาง (เว้นว่างไว้ถ้าใช้ --batch)")
    parser.add_argument("--crf", type=int, default=20, help="คุณภาพ (18–23 ดี, 0=lossless)")
    parser.add_argument("--preset", default="medium", help="ความเร็ว (ultrafast..veryslow)")
    parser.add_argument("--audio-bitrate", default="128k", help="บิตเรตเสียง (เช่น 128k, 192k)")
    parser.add_argument("--threads", type=int, default=0, help="จำนวน threads (0=อัตโนมัติ)")
    parser.add_argument("--batch", action="store_true", help="แปลงทุกไฟล์ในโฟลเดอร์")
    parser.add_argument("--no-overwrite", action="store_true", help="ไม่เขียนทับไฟล์ที่มีอยู่แล้ว")
    return parser.parse_args()

def main():
    args = parse_args()
    check_ffmpeg()
    inp = Path(args.input)
    kwargs = {
        "crf": args.crf,
        "preset": args.preset,
        "audio_bitrate": args.audio_bitrate,
        "threads": args.threads,
        "overwrite": not args.no_overwrite,
    }

    if args.batch:
        if not inp.is_dir():
            print("❌ ต้องระบุเป็นโฟลเดอร์เมื่อใช้ --batch")
            sys.exit(2)
        batch_convert(inp, **kwargs)
        return

    if not inp.exists():
        print(f"❌ ไม่พบไฟล์: {inp}")
        sys.exit(2)

    out = Path(args.output) if args.output else inp.with_suffix(".mp4")
    rc = convert_one(inp, out, **kwargs)
    sys.exit(rc)

if __name__ == "__main__":
    main()
