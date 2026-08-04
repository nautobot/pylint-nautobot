from nautobot.apps.jobs import Job


class CableReportJob(Job):
    """`self` infers to a Job, which is not a CableTermination, so its `cable` attribute is unrelated."""

    def run(self, cable):
        self.cable = cable
        self.render_report(cable=cable, path="/tmp/report.txt")

    def render_report(self, cable, path):
        self.logger.info("%s -> %s", cable, path)


def set_non_cable_values(record):
    """A value that is provably not a Cable means the attribute is near-certainly unrelated."""
    record.cable = "Cat6"
    record.cable = 5


class CableTestCase:
    """`cls` infers to the class object rather than an instance, and this class is not a CableTermination."""

    @classmethod
    def setUpTestData(cls, cable):
        cls.cable = cable
