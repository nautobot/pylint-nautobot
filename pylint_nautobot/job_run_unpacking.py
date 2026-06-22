"""Check for unpacking operators in Job run methods."""

from astroid.nodes import ClassDef, FunctionDef
from pylint.checkers import BaseChecker

from .utils import find_ancestor

# Job base class. Astroid resolves the public `nautobot.apps.jobs.Job` re-export to its
# definition module, `nautobot.extras.jobs.Job`.
_JOB_BASE_CLASSES = ("nautobot.extras.jobs.Job",)


class NautobotJobRunUnpackingChecker(BaseChecker):
    """Discourage `*args`/`**kwargs` in a Job's `run` method."""

    version_specifier = ">=2,<4"

    name = "nautobot-job-run-unpacking"
    msgs = {
        "E4294": (
            "Job `run` method uses an unpacking operator (`%s`). Declare all job options as explicit keyword arguments.",
            "nb-job-run-unpacking",
            "In Nautobot v2+, all job options are explicit keyword arguments on `run`. "
            "Using `*args`/`**kwargs` causes inconsistencies because the UI sends all form "
            "fields while API/ORM calls only send provided fields.",
        )
    }

    def visit_functiondef(self, node: FunctionDef):
        """Visit function/method definitions, looking for a Job's `run` method."""
        if node.name != "run":
            return

        parent = node.parent
        if not isinstance(parent, ClassDef):
            return
        if not find_ancestor(parent, _JOB_BASE_CLASSES):
            return

        # `*args` and `**kwargs` are reported separately so the message names the operator.
        if node.args.vararg:
            self.add_message("nb-job-run-unpacking", node=node, args=(f"*{node.args.vararg}",))
        if node.args.kwarg:
            self.add_message("nb-job-run-unpacking", node=node, args=(f"**{node.args.kwarg}",))
