#!/home/hatch/workspace/tools/whisper_venv/bin/python
"""H3YU QC: timestamped ASR of a generated song (Whisper base, zh).
Usage: qc_asr.py <song.mp3> [segments_out.txt]
Acceptance (SKILL.md step 7): every section sung in order, outro complete,
last vocal ends within ~10s of file end, no single-line loop, no long vocal gaps.
"""
import sys, os
import whisper

def main():
    mp3 = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(mp3)[0] + "_segments.txt"
    m = whisper.load_model("base")
    r = m.transcribe(mp3, language="zh", verbose=False)
    lines = [f"{s['start']:7.1f}-{s['end']:7.1f}  {s['text'].strip()}" for s in r["segments"]]
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if lines:
        print("LAST_VOCAL_END:", r["segments"][-1]["end"])

if __name__ == "__main__":
    main()
