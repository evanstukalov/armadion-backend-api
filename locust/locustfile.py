from locust import task, HttpUser

class Actions(HttpUser):
    @task(1)
    def doors_popular(self):
        self.client.get('/doors/popular/')

    @task(2)
    def doors(self):
        self.client.get('/doors/')

    @task(3)
    def doors_filter(self):
        self.client.get('/doors/filter')