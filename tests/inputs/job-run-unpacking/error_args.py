from nautobot.apps.jobs import Job


class MyJob(Job):
    def run(self, *args):
        pass
