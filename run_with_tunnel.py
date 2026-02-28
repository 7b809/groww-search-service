import subprocess
import time
import re
import shutil
import sys
import socket
import platform
import os


# ==========================================================
# Detect Free Port Automatically
# ==========================================================
def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


# ==========================================================
# Detect OS and Set cloudflared Binary
# ==========================================================
def get_cloudflared_binary():
    system = platform.system().lower()

    if system == "windows":
        return "cloudflared.exe"
    else:
        return "./cloudflared"


# ==========================================================
# Install cloudflared if missing
# ==========================================================
def install_cloudflared():
    system = platform.system().lower()

    if system == "windows":
        binary_name = "cloudflared.exe"
        download_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    else:
        binary_name = "cloudflared"
        download_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"

    if not os.path.exists(binary_name):
        print("⏳ Installing cloudflared...\n")

        subprocess.run(
            ["curl", "-L", download_url, "-o", binary_name],
            check=True
        )

        if system != "windows":
            subprocess.run(["chmod", "+x", binary_name], check=True)

        print("✅ cloudflared installed.\n")
    else:
        print("✅ cloudflared already installed.\n")


# ==========================================================
# Start FastAPI on Dynamic Port
# ==========================================================
def start_fastapi(port):
    print(f"🚀 Starting FastAPI on port {port}...\n")

    uvicorn_cmd = [
        "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", str(port)
    ]

    return subprocess.Popen(uvicorn_cmd)


# ==========================================================
# Start Cloudflare Tunnel
# ==========================================================
def start_tunnel(port):
    print("🌍 Starting Cloudflare Tunnel...\n")

    binary = get_cloudflared_binary()

    tunnel_proc = subprocess.Popen(
        [binary, "tunnel", "--url", f"http://localhost:{port}"],
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

                print("\n🔌 WebSocket Base URL:")
                print(public_url.replace("https", "wss") + "/ws/option")

                print("\n📌 Example WebSocket:")
                print(public_url.replace("https", "wss") + "/ws/option/NIFTY2630225400CE")

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

    port = get_free_port()

    fastapi_proc = start_fastapi(port)

    # wait briefly to allow server startup
    time.sleep(3)

    tunnel_proc = start_tunnel(port)

    try:
        tunnel_proc.wait()
    except KeyboardInterrupt:
        shutdown(fastapi_proc, tunnel_proc)