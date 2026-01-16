
import obspython as obs
import socket
import struct
import threading
import os
import time

HOST = "127.0.0.1"
PORT = 8477

sock = None
thread = None
running = True

VIDEO_DIRECTORY = "/home/adrien/Videos"


def rename_most_recent_file(map_name: str):
    try:
        files = [
            os.path.join(VIDEO_DIRECTORY, f)
            for f in os.listdir(VIDEO_DIRECTORY)
            if os.path.isfile(os.path.join(VIDEO_DIRECTORY, f))
        ]

        if not files:
            print("[OBS] No files found in video directory")
            return

        most_recent = max(files, key=os.path.getmtime)

        directory, old_name = os.path.split(most_recent)
        ext = os.path.splitext(old_name)[1]
        new_path = os.path.join(directory, map_name + ext)

        os.rename(most_recent, new_path)
        print(f"[OBS] Saved recording as: {new_path}")

    except Exception as e:
        print(f"[OBS] Rename failed: {e}")


def recv_exact(conn, size):
    data = b""
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Socket closed")
        data += chunk
    return data


def stop_and_rename(map_name: str):
    if obs.obs_frontend_recording_active():
        obs.obs_frontend_recording_stop()

        # Wait until OBS finishes writing the file
        time.sleep(0.5)

        rename_most_recent_file(map_name)


def socket_loop():
    global sock, running

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("[OBS] Connected to controller")

    while running:
        try:
            msg = struct.unpack("i", recv_exact(sock, 4))[0]

            if msg == 0:  # Stop recording
                size = struct.unpack("i", recv_exact(sock, 4))[0]
                map_name = recv_exact(sock, size).decode("utf-8")
                time.sleep(2)
                print(f"[OBS] Stop recording → {map_name}")
                stop_and_rename(map_name)

            elif msg == 1:  # Begin recording
                print("[OBS] Start recording")
                if obs.obs_frontend_recording_active():
                    obs.obs_frontend_recording_stop()
                    time.sleep(0.1)
                obs.obs_frontend_recording_start()

        except Exception as e:
            print("[OBS] Socket error:", e)
            break


def script_load(settings):
    global thread
    thread = threading.Thread(target=socket_loop, daemon=True)
    thread.start()


def script_unload():
    global running, sock
    running = False
    if sock:
        sock.close()
