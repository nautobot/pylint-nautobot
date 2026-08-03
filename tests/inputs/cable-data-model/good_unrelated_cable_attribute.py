from nautobot.apps.jobs import Job


class CableReportJob(Job):
    """`self.cable` is job state here, not a CableTermination attribute."""

    def run(self, cable):
        self.cable = cable
        self.render_report(cable=cable, path="/tmp/report.txt")

    def render_report(self, cable, path):
        self.logger.info("%s -> %s", cable, path)
