import time
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # self.client.post("/login", json={"username":"ellen_key", "password":"education"})
        pass

    def on_stop(self):
        # self.client.post("/logout")
        pass

    @task
    def posts_find_all(self):
        self.client.get("/posts/find")

    @task(5)
    def posts_find_by_id(self):
        for item_id in range(10):
            self.client.get(f"/posts/find/{item_id}", name="/posts/find/:id")
            time.sleep(1)
