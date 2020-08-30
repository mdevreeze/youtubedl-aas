import os
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
dir_path = os.path.dirname(os.path.realpath(__file__))


def test_read_main():
    response = client.post("/", json={"url": "not a valid url"})
    assert response.status_code == 422


def test_download():
    mp4file = dir_path + "/output/" + "Me at the zoo.mp4"
    giffile = dir_path + "/output/" + "Me at the zoo.gif"
    if os._exists(mp4file):
        os.remove(mp4file)
    if os._exists(giffile):
        os.remove(giffile)

    response = client.post(
        "/",
        json={"url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "optimize": False},
    )
    assert response.status_code == 200
    status = client.get("/" + response.json()["id"] + "/status")

    assert status.status_code == 200
    assert status.json()["status"] == "finished"
    assert os.path.exists(dir_path + "/output/" + "Me at the zoo.mp4")
    assert os.path.exists(dir_path + "/output/" + "Me at the zoo.gif")
