import cv2
import time
import os
import requests
import glob
from statistics import mean

# ========== CONFIG ==========
CLIP_DURATION = 5             # record 5-second clips
SESSION_DURATION = 60       # total session time (2 min)
BREAK_DURATION = 10           # seconds between clips
OUTPUT_DIR = "clips"
MAX_CAM_INDEX = 3
API_KEY = "H3XeEJEsPwcBY5gQB1Nhq92MsHelQz_vhtdzQlvSUgPuS0gmyATYAu_oVwSfUSeiUxM"
OVERRIDE_THRESHOLD = 0.1
# ============================

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def find_working_camera(max_index=MAX_CAM_INDEX):
    """Find a valid camera index."""
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        ret, _ = cap.read()
        cap.release()
        if ret:
            print(f"[INFO] Using camera index {i}")
            return i
    print("[ERROR] No working camera found!")
    return None


def record_clip(filename=None, duration=CLIP_DURATION):
    """Record a video clip for given duration."""
    cam_index = find_working_camera()
    if cam_index is None:
        return None

    if filename is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(OUTPUT_DIR, f"clip_{timestamp}.avi")

    cap = cv2.VideoCapture(cam_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 20)

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    print(f"[INFO] Recording for {duration} seconds...")
    start_time = time.time()
    frames_written = 0

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame read failed.")
            continue
        out.write(frame)
        frames_written += 1

    cap.release()
    out.release()
    print(f"[INFO] Clip saved: {filename} ({frames_written} frames written)")
    return filename if frames_written > 0 else None


def upload_clip(filename):
    """Upload the clip to Imentiv API."""
    if not os.path.exists(filename):
        print(f"[ERROR] File not found: {filename}")
        return None

    url = "https://api.imentiv.ai/v1/videos"
    headers = {
        "X-API-Key": API_KEY,
        "accept": "application/json",
        "Referer": "https://imentiv.ai"
    }

    try:
        with open(filename, "rb") as f:
            files = {
                "video_file": (os.path.basename(filename), f, "video/avi"),
                "title": (None, os.path.basename(filename)),
                "description": (None, "Smart Desk Assistant session clip"),
                "generate_audio_summary": (None, "false"),
            }
            response = requests.post(url, headers=headers, files=files)
            print(f"[DEBUG] Upload response: {response.text}")

        if response.status_code in [200, 201, 202]:
            data = response.json()
            video_id = data.get("id") or data.get("video_id")
            print(f"[INFO] Uploaded video ID: {video_id}")
            return video_id
        else:
            print(f"[ERROR] Upload failed ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Upload error: {e}")
        return None


def get_video_status(video_id):
    """Check if video is processed yet."""
    url = f"https://api.imentiv.ai/v1/videos/{video_id}"
    headers = {"X-API-Key": API_KEY, "accept": "application/json"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()

        if res.status_code != 200:
            print(f"[ERROR] Failed to get video status ({res.status_code}): {res.text}")
            return None

        return data.get("status")
    except Exception as e:
        print(f"[ERROR] Status check error: {e}")
        return None


def get_aggregate_emotions(video_id):
    """Fetch aggregated emotion data."""
    url = f"https://api.imentiv.ai/v1/videos/{video_id}/emotions/aggregate"
    headers = {"X-API-Key": API_KEY, "accept": "application/json"}

    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            print(f"[ERROR] Emotion fetch failed ({res.status_code}): {res.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Emotion API error: {e}")
        return None


def analyze_session(all_emotions):
    """Compute overall emotion averages and productivity."""
    if not all_emotions:
        print("[WARN] No emotion data recorded.")
        return

    # Gather all emotion types
    keys = set().union(*[emo.keys() for emo in all_emotions])
    avg_emotions = {k: mean([emo.get(k, 0) for emo in all_emotions]) for k in keys}

    dominant = max(avg_emotions, key=avg_emotions.get)
    print("\n===== SESSION SUMMARY =====")
    for k, v in avg_emotions.items():
        print(f"{k.capitalize():<10}: {v:.3f}")
    print(f"\n[INFO] Dominant Emotion: {dominant.capitalize()}")

    # Productivity mapping
    if dominant in ["happy", "surprise"]:
        state = "happy/focused/motivated"
    elif dominant in ["neutral"]:
        state = "neutral/focused"
    elif dominant in ["sad", "disgust", "fear"]:
        state = "fatigued/stressed"
    elif dominant in ["angry"]:
        state = "angry/frustrated/stressed"
    else:
        state = "unknown"

    print(f"[INFO] Productivity State: {state}")
    print("=============================")


if __name__ == "__main__":
    print("\n=== SMART DESK ASSISTANT ===")
    choice = input("Start 2-minute emotion tracking session? (yes/no): ").strip().lower()

    if choice not in ["yes", "y"]:
        print("[INFO] Session cancelled.")
        exit()

    print("[INFO] Starting 2-minute session...")
    start_time = time.time()
    all_emotions = []

    while time.time() - start_time < SESSION_DURATION:
        # Record clip
        clip_path = record_clip()
        if not clip_path:
            continue

        # Upload
        video_id = upload_clip(clip_path)
        if not video_id:
            continue

        # Wait for processing
        for _ in range(10):
            status = get_video_status(video_id)
            if status == "completed":
                break
            elif status in ["failed", "error"]:
                print("[ERROR] Video failed on server.")
                break
            time.sleep(10)

        # Fetch emotion data
        emotions = get_aggregate_emotions(video_id)
        if emotions:
            all_emotions.append(emotions)
            print(f"[INFO] Emotions: {emotions}")

        # Wait before next clip
        if time.time() - start_time < SESSION_DURATION:
            print(f"[INFO] Taking {BREAK_DURATION}s break before next clip...\n")
            time.sleep(BREAK_DURATION)

    analyze_session(all_emotions)
    print("\n✅ Session complete! All emotion data processed.")
