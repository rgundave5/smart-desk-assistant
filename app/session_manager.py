import os
import time
import csv
import json
import threading
from datetime import datetime
from emotion_activity_tracker import (
    record_clip,
    upload_clip,
    get_video_status,
    get_aggregate_emotions
)

# ========== CONFIG ==========
CLIP_INTERVAL = 30             # seconds between clips
SESSION_DIR = "sessions"       # folder to store session data
OUTPUT_DIR = "clips"           # reused from emotion_activity_tracker
OVERRIDE_THRESHOLD = 0.1

current_session = None
session_emotions = {}
session_start_time = None
# ============================

if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)


class SessionManager:
    def __init__(self):
        self.session_active = False
        self.session_start = None
        self.session_end = None
        self.session_name = None
        self.session_path = None
        self.thread = None
        self.emotion_log = []

    # ---------- SESSION CONTROL ----------
    def start_session(self):
        """Start a new tracking session."""
        if self.session_active:
            print("[WARN] A session is already running.")
            return

        self.session_active = True
        self.session_start = datetime.now()
        self.session_name = f"session_{self.session_start.strftime('%Y%m%d_%H%M%S')}"
        self.session_path = os.path.join(SESSION_DIR, self.session_name)

        try:
            os.makedirs(self.session_path, exist_ok=True)
        except Exception as e:
            print(f"[ERROR] Failed to create session directory: {e}")
            self.session_active = False
            return

        print(f"[INFO] Session started: {self.session_name}")
        self.thread = threading.Thread(target=self._run_session, daemon=True)
        self.thread.start()

    def end_session(self):
        """Stop the current session."""
        if not self.session_active:
            print("[WARN] No active session to stop.")
            return

        print("[INFO] Ending session...")
        self.session_active = False
        self.session_end = datetime.now()

        if self.thread:
            self.thread.join(timeout=10)

        duration = (self.session_end - self.session_start).total_seconds() / 60
        print(f"[INFO] Session ended. Duration: {duration:.2f} minutes.")
        self._save_session_summary(duration)

    # ---------- SESSION LOOP ----------
    def _run_session(self):
        """Continuously record, upload, and log emotions."""
        while self.session_active:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            clip_path = os.path.join(OUTPUT_DIR, f"clip_{timestamp}.avi")

            print(f"[INFO] Recording new clip: {clip_path}")
            try:
                success = record_clip(clip_path)
            except Exception as e:
                print(f"[ERROR] Exception during clip recording: {e}")
                success = False

            if not success or not os.path.exists(clip_path):
                print("[ERROR] Clip recording failed. Skipping to next attempt.")
                time.sleep(CLIP_INTERVAL)
                continue

            # Upload to Imentiv
            try:
                video_id = upload_clip(clip_path)
            except Exception as e:
                print(f"[ERROR] Upload exception: {e}")
                video_id = None

            if not video_id:
                print("[ERROR] Clip upload failed. Retrying next cycle.")
                time.sleep(CLIP_INTERVAL)
                continue

            print("[INFO] Waiting for API processing...")
            emotions = None
            for attempt in range(20):  # up to ~3-5 minutes
                if not self.session_active:
                    print("[INFO] Session manually stopped during processing.")
                    return

                try:
                    status = get_video_status(video_id)
                except Exception as e:
                    print(f"[ERROR] Failed to get status: {e}")
                    status = None

                print(f"[DEBUG] API Status ({attempt+1}/20): {status}")

                if status == "completed":
                    try:
                        emotions = get_aggregate_emotions(video_id)
                    except Exception as e:
                        print(f"[ERROR] Failed to fetch emotions: {e}")
                        emotions = None
                    if emotions:
                        break
                elif status in ["failed", "error"]:
                    print("[ERROR] API failed for this clip.")
                    break

                time.sleep(10)

            if emotions:
                try:
                    self._log_emotions(timestamp, emotions)
                except Exception as e:
                    print(f"[ERROR] Failed to log emotions: {e}")
            else:
                print("[WARN] No emotions returned for this clip.")

            # Wait before next recording
            for _ in range(CLIP_INTERVAL):
                if not self.session_active:
                    print("[INFO] Session stopped mid-wait.")
                    return
                time.sleep(1)

    # ---------- DATA LOGGING ----------
    def _log_emotions(self, timestamp, emotions):
        """Append emotions to session CSV."""
        if not isinstance(emotions, dict):
            print("[ERROR] Invalid emotion data format.")
            return

        record = {"timestamp": timestamp, **emotions}
        self.emotion_log.append(record)
        csv_path = os.path.join(self.session_path, "session_emotions.csv")

        try:
            write_header = not os.path.exists(csv_path)
            with open(csv_path, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=record.keys())
                if write_header:
                    writer.writeheader()
                writer.writerow(record)
        except Exception as e:
            print(f"[ERROR] Could not write to CSV: {e}")
            return

        print(f"[INFO] Logged emotions for {timestamp}")

    # ---------- SUMMARY ----------
    def _save_session_summary(self, duration):
        """Aggregate and save summary stats."""
        if not self.emotion_log:
            print("[WARN] No emotion data collected this session.")
            return

        try:
            emotion_keys = [k for k in self.emotion_log[0].keys() if k != "timestamp"]
            summary = {
                emo: sum(r.get(emo, 0) for r in self.emotion_log) / len(self.emotion_log)
                for emo in emotion_keys
            }
        except Exception as e:
            print(f"[ERROR] Failed to compute averages: {e}")
            return

        dominant = max(summary, key=summary.get)
        if dominant == "neutral":
            for emo, val in summary.items():
                if emo != "neutral" and val > OVERRIDE_THRESHOLD:
                    dominant = emo
                    break

        summary_data = {
            "session_name": self.session_name,
            "start_time": self.session_start.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.session_end.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_minutes": duration,
            "average_emotions": summary,
            "dominant_emotion": dominant
        }

        json_path = os.path.join(self.session_path, "summary.json")
        try:
            with open(json_path, "w") as f:
                json.dump(summary_data, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Could not save summary JSON: {e}")
            return

        print(f"[INFO] Saved session summary to: {json_path}")
        print(f"[INFO] Dominant emotion: {dominant}")


# ---------- CLI USAGE ----------
if __name__ == "__main__":
    manager = SessionManager()

    while True:
        try:
            cmd = input("\nEnter command (start / stop / exit): ").strip().lower()
        except EOFError:
            print("\n[INFO] Input stream closed. Exiting.")
            break

        if cmd == "start":
            manager.start_session()
        elif cmd == "stop":
            manager.end_session()
        elif cmd == "exit":
            if manager.session_active:
                manager.end_session()
            print("[INFO] Exiting program.")
            break
        else:
            print("[WARN] Invalid command. Use start / stop / exit.")
