from nautobot.apps.jobs import Job


class MyJob(Job):
    # This test also verifies we don't get a false negative when using `*` to enforce arguments are passed as keyword-only.
    def run(self, *, device, location=None):
        pass
