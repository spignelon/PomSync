# PomSync: Sync Pomodoro Timer

A Flask-based synchronized Pomodoro timer that allows multiple users to join the same timer session and stay in sync. The frontend is built with HTML, CSS, and JavaScript, while the backend handles session management and timing.

## Features
- **Synchronized Timer:** All users connected see the same timer.
- **Two Modes:** 25-5 minute and 50-10 minute Pomodoro sessions.
- **Audio Alerts:** Start and end sounds for each phase.
- **Reset Option:** Allows resetting the session.
- **Simple Deployment:** Deploy on **Render.com** or a **Debian VPS**.

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Server:** Gunicorn (for production deployment)

## Setup & Installation

### Local Development

1. **Clone the Repository**
   ```bash
   git clone https://github.com/spignelon/PomSync.git
   cd PomSync
   ```
2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Flask Server**
   ```bash
   python server.py
   ```
5. **Access the App**
   Open a browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Deploying on Render.com

1. **Push Your Code to GitHub**
2. **Go to [Render Dashboard](https://dashboard.render.com/)**
3. **Create a New Web Service**
4. **Use These Settings:**
   - **Runtime:** Python
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     gunicorn -b 0.0.0.0:$PORT server:app
     ```
5. **Deploy & Get Your Public URL**

## Deploying on Debian VPS

1. **SSH into Your Server**
   ```bash
   ssh user@your-server-ip
   ```
2. **Install Required Packages**
   ```bash
   sudo apt update && sudo apt install python3 python3-venv python3-pip nginx
   ```
3. **Clone the Repo & Set Up Virtual Env**
   ```bash
   git clone https://github.com/spignelon/PomSync.git
   cd PomSync
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Run Gunicorn Server**
   ```bash
   gunicorn -b 0.0.0.0:5000 server:app
   ```
5. **Set Up Nginx Reverse Proxy (Optional)**
   ```bash
   sudo nano /etc/nginx/sites-available/pomodoro
   ```
   Add the following:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   Then enable it:
   ```bash
   sudo ln -s /etc/nginx/sites-available/pomodoro /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```
6. **Access via Browser**
   ```
   http://yourdomain.com
   ```

## API Endpoints
| Method | Endpoint     | Description                 |
|--------|-------------|-----------------------------|
| POST   | `/start`    | Starts a new Pomodoro session |
| POST   | `/reset`    | Resets the session         |
| GET    | `/status`   | Gets the current session status |

## Contributing
Feel free to open issues or submit pull requests to improve this project!

## License
This project is licensed under the GPL-2.0 license.

