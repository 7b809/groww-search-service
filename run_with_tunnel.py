import subprocess
import threading
import time
import re
import shutil
import signal
import sys

UVICORN_CMD = [
    "uvicorn",
    "app.main:app",
    "--host", "0.0.0.0",
    "--port", "8000"
]

CLOUDFLARED_BINARY = "./cloudflared"
LOCAL_PORT = 8000


# ==========================================================
# Install cloudflared if missing
# ==========================================================
def install_cloudflared():
    if not shutil.which("cloudflared") and not shutil.which("./cloudflared"):
        print("⏳ Installing cloudflared...\n")
        subprocess.run([
            "curl", "-L",
            "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe",
            "-o", "cloudflared.exe"
        ], check=True)
        print("✅ cloudflared installed.\n")
    else:
        print("✅ cloudflared already installed.\n")


# ==========================================================
# Start FastAPI
# ==========================================================
def start_fastapi():
    print("🚀 Starting FastAPI...\n")
    return subprocess.Popen(UVICORN_CMD)


# ==========================================================
# Start Cloudflare Tunnel
# ==========================================================
def start_tunnel():
    print("🌍 Starting Cloudflare Tunnel...\n")

    tunnel_proc = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://localhost:{LOCAL_PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    public_url = None

    for line in tunnel_proc.stdout:
        print("[Cloudflare]", line.strip())

        if "trycloudflare.com" in line and not public_url:
            match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", line)
            if match:
                public_url = match.group(0)
                print("\n✅ Public URL Ready:")
                print(public_url)
                print("\n🔌 WebSocket URL:")
                print(public_url.replace("https", "wss") + "/ws/option/YOUR_SYMBOL")
                print("\n")

    return tunnel_proc


# ==========================================================
# Graceful Shutdown
# ==========================================================
def shutdown(fastapi_proc, tunnel_proc):
    print("\n🛑 Shutting down...")

    if fastapi_proc:
        fastapi_proc.terminate()

    if tunnel_proc:
        tunnel_proc.terminate()

    sys.exit(0)


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    install_cloudflared()

    fastapi_proc = start_fastapi()

    # Wait 2 seconds to ensure server starts
    time.sleep(2)

    tunnel_proc = start_tunnel()

    try:
        tunnel_proc.wait()
    except KeyboardInterrupt:
        shutdown(fastapi_proc, tunnel_proc)