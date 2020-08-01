"""Integration tests on Docker container"""
import requests
import time

# timeout variable can be omitted, if you use specific value in the while condition



def test_status():
    """Test retrieve of status"""
    response = requests.post("http://localhost:8000",
                             json={
                                 "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
                                 "optimize": False
                             })
    assert response.status_code == 200
    body = response.json()
    print(body)

    timeout = 5  #seconds 

    timeout_start = time.time()

    while time.time() < timeout_start + timeout:
        status_response = requests.get("http://localhost:8000/" + body["id"] + "/status")
        print(status_response.text)
        assert status_response.status_code == 200
        status_body = status_response.json()
        if not status_body["downloading"]:
            break

    status_body = status_response.json()
    print(status_body)
    assert status_body.status == "downloading"
