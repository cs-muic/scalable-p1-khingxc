from locust import HttpUser, task

class Benchmarks(HttpUser):

    @task
    def paste(self):
        _ = self.client.post(url="/api/paste", json={"title": "abcd", "content": "efgh"})

    # @task
    # def id(self):
    #     self.client.get("/api/paste")

    @task
    def recents(self):
        self.client.post(url="/api/recents", json={})