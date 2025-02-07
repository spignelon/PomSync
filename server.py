from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading
import json
import os

app = Flask(__name__)
CORS(app)  # ✅ Allow frontend access

# File to store session data
SESSION_FILE = "pomodoro_session.json"

# Default Pomodoro state
DEFAULT_SESSION = {
    "active": False,
    "start_time": None,
    "work_duration": 0,
    "break_duration": 0,
    "phase": "work"  # Can be "work" or "break"
}


def load_session():
    """Loads the Pomodoro session from a file."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return DEFAULT_SESSION
    return DEFAULT_SESSION


def save_session(session):
    """Saves the Pomodoro session to a file."""
    with open(SESSION_FILE, "w") as file:
        json.dump(session, file)


def update_session():
    """Continuously updates the Pomodoro session to switch phases when time expires."""
    while True:
        session = load_session()

        if session["active"]:
            elapsed_time = time.time() - session["start_time"]
            phase_duration = session["work_duration"] if session["phase"] == "work" else session["break_duration"]

            if elapsed_time >= phase_duration:
                session["phase"] = "break" if session["phase"] == "work" else "work"
                session["start_time"] = time.time()  # Reset timer for new phase
                save_session(session)

        time.sleep(1)  # ✅ Sync every second


@app.route("/start", methods=["POST"])
def start_session():
    """Starts a Pomodoro session and saves it to the file."""
    data = request.json
    mode = data.get("mode", "25-5")

    if mode == "25-5":
        work_time, break_time = 25 * 60, 5 * 60
    elif mode == "50-10":
        work_time, break_time = 50 * 60, 10 * 60
    else:
        return jsonify({"error": "Invalid mode"}), 400

    session = {
        "active": True,
        "start_time": time.time(),
        "work_duration": work_time,
        "break_duration": break_time,
        "phase": "work"
    }
    save_session(session)

    return jsonify({"message": "Session started", "mode": mode})


@app.route("/status", methods=["GET"])
def get_status():
    """Returns the current Pomodoro session state."""
    session = load_session()

    if not session["active"]:
        return jsonify({"active": False, "message": "No active session"})

    elapsed_time = time.time() - session["start_time"]
    phase_duration = session["work_duration"] if session["phase"] == "work" else session["break_duration"]
    remaining_time = max(0, phase_duration - elapsed_time)

    return jsonify({
        "phase": session["phase"],
        "remaining_time": int(remaining_time),
        "active": session["active"]
    })


@app.route("/reset", methods=["POST"])
def reset_session():
    """Resets the Pomodoro session."""
    save_session(DEFAULT_SESSION)
    return jsonify({"message": "Session reset"})


if __name__ == "__main__":
    thread = threading.Thread(target=update_session, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

