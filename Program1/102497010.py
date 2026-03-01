import sys
import os
import yt_dlp
from pydub import AudioSegment


# ---------------------------
# FUNCTION: Download Videos (Only if needed)
# ---------------------------
def download_videos(singer, num_videos):
    print("Checking existing files...")

    os.makedirs("downloads", exist_ok=True)

    existing_files = [
        f for f in os.listdir("downloads")
        if f.endswith(('.webm', '.m4a', '.mp4', '.mp3'))
    ]

    # If already enough files, skip downloading
    if len(existing_files) >= num_videos:
        print(f"{len(existing_files)} files already exist. Skipping download.")
        return

    print("Downloading videos from YouTube...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'ignoreerrors': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Avoid long mixes and albums
            ydl.download([f"ytsearch{num_videos}:{singer} official audio -live -mix -full album"])
    except Exception as e:
        print("Error downloading videos:", e)
        sys.exit(1)


# ---------------------------
# FUNCTION: Convert & Trim
# ---------------------------
def process_audios(duration, num_videos):
    print("Processing audio files...")

    trimmed_clips = []

    files = [
        f for f in os.listdir("downloads")
        if f.endswith(('.webm', '.m4a', '.mp4', '.mp3'))
    ]

    if not files:
        print("No audio files found.")
        sys.exit(1)

    count = 0

    for file in files:
        if count >= num_videos:
            break

        file_path = os.path.join("downloads", file)

        # Skip very large files (e.g., > 50 MB)
        if os.path.getsize(file_path) > 50 * 1024 * 1024:
            print(f"Skipping large file: {file}")
            continue

        try:
            audio = AudioSegment.from_file(file_path)
            trimmed = audio[:duration * 1000]
            trimmed_clips.append(trimmed)
            count += 1
        except Exception as e:
            print(f"Skipping {file} due to error:", e)

    return trimmed_clips

# ---------------------------
# FUNCTION: Merge Audios
# ---------------------------
def merge_audios(clips, output_file):
    print("Merging audio clips...")

    if not clips:
        print("No valid audio clips to merge.")
        sys.exit(1)

    final_audio = clips[0]

    for clip in clips[1:]:
        final_audio += clip

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", output_file)

    final_audio.export(output_path, format="mp3")

    print("Mashup created successfully!")
    print("Saved at:", output_path)


# ---------------------------
# MAIN FUNCTION
# ---------------------------
def main():

    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    if num_videos <= 10:
        print("NumberOfVideos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("AudioDuration must be greater than 20 seconds.")
        sys.exit(1)

    if not output_file.endswith(".mp3"):
        print("Output file must be in .mp3 format.")
        sys.exit(1)

    download_videos(singer, num_videos)
    clips = process_audios(duration, num_videos)
    merge_audios(clips, output_file)


if __name__ == "__main__":
    main()