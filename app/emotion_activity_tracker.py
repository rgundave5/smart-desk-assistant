import cv2
import time
import os
import requests
import glob

# ========== CONFIG ==========
CLIP_DURATION = 5          # seconds per clip
OUTPUT_DIR = "clips"       # folder to save clips
MAX_CAM_INDEX = 3          # will try indices 0..2
API_KEY = "H3XeEJEsPwcBY5gQB1Nhq92MsHelQz_vhtdzQlvSUgPuS0gmyATYAu_oVwSfUSeiUxM"   # Replace with your real key
OVERRIDE_THRESHOLD = 0.1
# ============================

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def find_working_camera(max_index=MAX_CAM_INDEX):
    """Tries multiple camera indices until one works"""
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        ret, _ = cap.read()
        cap.release()
        if ret:
            print(f"[INFO] Using camera index {i}")
            return i
    print("[ERROR] No working camera found!")
    return None

def record_clip(filename, duration=CLIP_DURATION):
    cam_index = find_working_camera()
    if cam_index is None:
        return False

    cap = cv2.VideoCapture(cam_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 20)

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # stable codec for macOS
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = time.time()
    frames_written = 0
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("[WARN] Skipping invalid frame...")
            continue
        out.write(frame)
        frames_written += 1

    cap.release()
    out.release()
    print(f"[INFO] Clip saved: {filename} ({frames_written} frames written)")
    return frames_written > 0

# ======= RECORD CLIP =======
timestamp = time.strftime("%Y%m%d_%H%M%S")
clip_path = os.path.join(OUTPUT_DIR, f"clip_{timestamp}.avi")
success = record_clip(clip_path)

if not success:
    print("[ERROR] Clip recording failed. Exiting.")
    exit()

# ======= USE MOST RECENT CLIP =======
latest_clip = max(glob.glob(f"{OUTPUT_DIR}/*.avi"), key=os.path.getctime)
print(f"[INFO] Using latest clip: {latest_clip}")

# ======= UPLOAD TO IMENTIV =======
def upload_clip(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] File not found: {filename}")
        return None
    url = f"https://api.imentiv.ai/v1/videos"
    headers = {
        "X-API-Key": API_KEY,
        "Referer": "https://imentiv.ai",
        "accept": "application/json"
    }
    try:
        with open(filename, 'rb') as f:
            files = {
               #'video_file': f,
               "video_file": (os.path.basename(filename), f, "video/avi"),
                'title': (None, os.path.basename(filename)),  
                'description': (None, "Auto-uploaded test clip from Smart Desk Assistant"),
                'generate_audio_summary': (None, 'false')
            }
            response = requests.post(url, headers=headers, files=files)
            print(f"[DEBUG] Raw API response: {response.text}")

        if response.status_code == (200, 201):
            data = response.json()
            video_id = data.get("video_id") or data.get("video_id")
            print(f"[INFO] Uploaded video. ID: {video_id}, status: {data.get('status')}")
            return video_id
        elif response.status_code == 202 or "processing" in response.text:
            data = response.json()
            video_id = data.get("id")
            print(f"[INFO] Video accepted for processing. ID: {video_id}")
            return video_id
        else:
            print(f"[ERROR] Upload failed: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception during upload: {e}")
        return None

video_id = upload_clip(latest_clip)

# ======= FETCH EMOTIONS =======
def get_aggregate_emotions(video_id):
    if not video_id:
        print("[WARN] No video ID provided.")
        return None
    url = f"https://api.imentiv.ai/v1/videos/{video_id}/emotions/aggregate"
    headers = {
        "X-API-Key": API_KEY,
        "accept": "application/json"
    }
    try:
        res = requests.get(url, headers=headers)
        print(f"[DEBUG] Emotion API response ({res.status_code}): {res.text}")
        if res.status_code == 200:
            data = res.json()
            return data
        else:
            if "'annotated_video_mp4'" in res.text:
                print("[WARN] Annotated video not generated — skipping.")
                return None
            print(f"[ERROR] Failed to get emotions: {res.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception during emotion fetch: {e}")
        return None

# ======= CHECK PROCESSING STATUS =======
def get_video_status(video_id):
    url = f"https://api.imentiv.ai/v1/videos/{video_id}"
    headers = {"X-API-Key": API_KEY, "accept": "application/json"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        return data.get("status")
    else:
        print(f"[ERROR] Failed to get video status: {res.text}")
        return None

# ======= WAIT UNTIL READY =======
if video_id:
    print("[INFO] Waiting for video to finish processing...")
    for attempt in range(20):  # ~5 minutes total
        status = get_video_status(video_id)
        print(f"[DEBUG] Status check {attempt+1}: {status}")
        if status == "completed":
            emotions = get_aggregate_emotions(video_id)
            if emotions:
                break
        elif status in ["failed", "error"]:
            print("[ERROR] Video processing failed on server.")
            break
        time.sleep(15)
else:
    print("[WARN] No video ID — skipping emotion check.")

# ======= SAFE PRODUCTIVITY MAPPING =======
if emotions:
    dominant = max(emotions, key=emotions.get).lower()
    dominant_value = emotions[dominant]
    print(f"[INFO] Dominant emotion: {dominant}")

    if dominant == "neutral":
        for emo, val in emotions.items():
            if emo != "neutral" and val > OVERRIDE_THRESHOLD:
                dominant = emo
                dominant_value = val
                break  # take the first significant non-neutral emotion

    if dominant in ["happy", "surprised"]:
        state = "happy/focused/motivated"
    elif dominant in ["neutral"]:
        state = "neutral/focused"
    elif dominant in ["tired"]:
        state = "tired/drained"
    elif dominant in ["sad", "disgust", "fear"]:
        state = "fatigued/stressed"
    elif dominant in ["angry", "frustrated"]:
        state = "angry/frustrated/stressed"
    else:
        state = "unknown"
    print(f"[INFO] Productivity state: {state}")
else:
    print("[WARN] Emotions not available. Skipping productivity mapping.")

def get_video_status(video_id):
    url = f"https://api.imentiv.ai/v1/videos/{video_id}"
    headers = {"X-API-Key": API_KEY, "accept": "application/json"}
    res = requests.get(url, headers=headers)
    print("[DEBUG]", res.text)