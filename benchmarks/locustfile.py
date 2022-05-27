from locust import HttpUser, task

id = 1

class Benchmarks(HttpUser):

    @task
    def paste(self):
        global id
        _ = self.client.post(url="/api/paste", json={"title": "abcd", "content": "efgh"})
        id += 1

    @task
    def id(self):
        self.client.get("/api/" + str(id))

    @task
    def recents(self):
        self.client.post(url="/api/recents", json={})