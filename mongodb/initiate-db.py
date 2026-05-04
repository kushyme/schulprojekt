import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path


CONTAINER_NAME = "flashcard-mongodb"
IMAGE_NAME = "flashcard-mongodb:local"
VOLUME_NAME = "flashcard-mongodb-data"
HOST = "127.0.0.1"
HOST_PORT = 27017
CONTAINER_PORT = 27017


def run_command(command):
    try:
        return subprocess.run(command, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        details = e.stderr.strip() or e.stdout.strip()
        if details:
            raise RuntimeError(f"{' '.join(command)} failed: {details}") from e
        raise


def docker_exists():
    return shutil.which("docker") is not None


def docker_image_exists():
    result = subprocess.run(
        ["docker", "image", "inspect", IMAGE_NAME],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def docker_container_exists():
    result = subprocess.run(
        ["docker", "container", "inspect", CONTAINER_NAME],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def port_is_open(host=HOST, port=HOST_PORT, timeout_seconds=1):
    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return True
    except OSError:
        return False


def wait_for_mongodb(host=HOST, port=HOST_PORT, timeout_seconds=30, interval_seconds=0.5):
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        if port_is_open(host, port):
            return

        time.sleep(interval_seconds)

    raise TimeoutError(f"MongoDB did not become reachable at {host}:{port}")


def build_docker_image():
    dockerfile = Path(__file__).with_name("Dockerfile")
    context_dir = dockerfile.parent

    print(f"Building Docker image {IMAGE_NAME} from {dockerfile}")
    run_command(["docker", "build", "-t", IMAGE_NAME, "-f", str(dockerfile), str(context_dir)])


def start_docker_container():
    if not docker_exists():
        raise RuntimeError("Docker is not installed or not available on PATH.")

    if docker_container_exists():
        print(f"Starting existing MongoDB container {CONTAINER_NAME}")
        run_command(["docker", "start", CONTAINER_NAME])
        return

    if not docker_image_exists():
        build_docker_image()

    print(f"Creating MongoDB container {CONTAINER_NAME}")
    run_command(
        [
            "docker",
            "run",
            "-d",
            "--name",
            CONTAINER_NAME,
            "--restart",
            "unless-stopped",
            "-p",
            f"{HOST}:{HOST_PORT}:{CONTAINER_PORT}",
            "-v",
            f"{VOLUME_NAME}:/data/db",
            IMAGE_NAME,
        ]
    )


def ensure_mongodb_container_running():
    if port_is_open():
        print(f"MongoDB is already reachable at mongodb://localhost:{HOST_PORT}/")
        return

    print("MongoDB is not reachable. Starting local Docker container.")
    start_docker_container()
    wait_for_mongodb()
    print(f"MongoDB is running at mongodb://localhost:{HOST_PORT}/")


def main():
    try:
        ensure_mongodb_container_running()
    except (RuntimeError, TimeoutError, subprocess.CalledProcessError) as e:
        print("Could not start MongoDB Docker container.", e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
