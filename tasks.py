<<<<<<< HEAD
"""Tasks for use with Invoke.

Copyright (c) 2023, Network to Code, LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os

from invoke.collection import Collection
from invoke.tasks import task as invoke_task
=======
"""Tasks for use with Invoke."""

import os
import re
from pathlib import Path

from invoke import Collection, Exit
from invoke import task as invoke_task
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.

<<<<<<< HEAD
    Examples
    --------
=======
    Examples:
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg

    val = str(arg).lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
<<<<<<< HEAD
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truthy value: `{arg}`")
=======
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"Invalid truthy value: `{arg}`")
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)


# Use pyinvoke configuration for default values, see http://docs.pyinvoke.org/en/stable/concepts/configuration.html
# Variables may be overwritten in invoke.yml or by the environment variables INVOKE_PYLINT_NAUTOBOT_xxx
namespace = Collection("pylint_nautobot")
namespace.configure(
    {
        "pylint_nautobot": {
<<<<<<< HEAD
            "nautobot_ver": "2.3.1",
            "project_name": "pylint-nautobot",
            "python_ver": "3.11",
            "local": False,
            "compose_dir": os.path.join(os.path.dirname(__file__), "development"),
            "compose_files": [
                "docker-compose.base.yml",
                "docker-compose.dev.yml",
            ],
            "compose_http_timeout": "86400",
=======
            "project_name": "pylint_nautobot",
            "python_ver": "3.10",
            "local": is_truthy(os.getenv("INVOKE_PYLINT_NAUTOBOT_LOCAL", "false")),
            "image_name": "pylint_nautobot",
            "image_ver": os.getenv("INVOKE_PYLINT_NAUTOBOT_IMAGE_VER", "latest"),
            "pwd": Path(__file__).parent,
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)
        }
    }
)


<<<<<<< HEAD
=======
# pylint: disable=keyword-arg-before-vararg
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)
def task(function=None, *args, **kwargs):
    """Task decorator to override the default Invoke task decorator and add each task to the invoke namespace."""

    def task_wrapper(function=None):
        """Wrapper around invoke.task to add the task to the namespace as well."""
        if args or kwargs:
            task_func = invoke_task(*args, **kwargs)(function)
        else:
            task_func = invoke_task(function)
        namespace.add_task(task_func)
        return task_func

    if function:
        # The decorator was called with no arguments
        return task_wrapper(function)
    # The decorator was called with arguments
    return task_wrapper


<<<<<<< HEAD
def docker_compose(context, command, **kwargs):
    """Helper function for running a specific docker compose command with all appropriate parameters and environment.

    Args:
    ----
        context (obj): Used to run specific commands
        command (str): Command string to append to the "docker compose ..." command, such as "build", "up", etc.
        **kwargs: Passed through to the context.run() call.
    """
    build_env = {
        # Note: 'docker compose logs' will stop following after 60 seconds by default,
        # so we are overriding that by setting this environment variable.
        "COMPOSE_HTTP_TIMEOUT": context.pylint_nautobot.compose_http_timeout,
        "NAUTOBOT_VER": context.pylint_nautobot.nautobot_ver,
        "PYTHON_VER": context.pylint_nautobot.python_ver,
        **kwargs.pop("env", {}),
    }
    compose_command_tokens = [
        "docker compose",
        f"--project-name {context.pylint_nautobot.project_name}",
        f'--project-directory "{context.pylint_nautobot.compose_dir}"',
    ]

    for compose_file in context.pylint_nautobot.compose_files:
        compose_file_path = os.path.join(context.pylint_nautobot.compose_dir, compose_file)
        compose_command_tokens.append(f' -f "{compose_file_path}"')

    compose_command_tokens.append(command)

    # If `service` was passed as a kwarg, add it to the end.
    service = kwargs.pop("service", None)
    if service is not None:
        compose_command_tokens.append(service)

    print(f'Running docker compose command "{command}"')
    compose_command = " ".join(compose_command_tokens)

    return context.run(compose_command, env=build_env, **kwargs)


def run_command(context, command, **kwargs):
    """Wrapper to run a command locally or inside the nautobot container."""
    if is_truthy(context.pylint_nautobot.local):
        context.run(command, **kwargs)
    else:
        # Check if nautobot is running, no need to start another nautobot container to run a command
        docker_compose_status = "ps --services --filter status=running"
        results = docker_compose(context, docker_compose_status, hide="out")
        if "nautobot" in results.stdout:
            compose_command = f"exec nautobot {command}"
        else:
            compose_command = f"run --rm --entrypoint '{command}' nautobot"

        pty = kwargs.pop("pty", True)

        docker_compose(context, compose_command, pty=pty, **kwargs)
=======
def run_command(context, exec_cmd, port=None, rm=True):
    """Wrapper to run the invoke task commands.

    Args:
        context ([invoke.task]): Invoke task object.
        exec_cmd ([str]): Command to run.
        port (int): Used to serve local docs.
        rm (bool): Whether to remove the container after running the command.

    Returns:
        result (obj): Contains Invoke result from running task.
    """
    if is_truthy(context.pylint_nautobot.local):
        print(f"LOCAL - Running command {exec_cmd}")
        result = context.run(exec_cmd, pty=True)
    else:
        print(
            f"DOCKER - Running command: {exec_cmd} container: {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver}"
        )
        if port:
            result = context.run(
                f"docker run -it {'--rm' if rm else ''} -p {port} -v {context.pylint_nautobot.pwd}:/local {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver} sh -c '{exec_cmd}'",
                pty=True,
            )
        else:
            result = context.run(
                f"docker run -it {'--rm' if rm else ''} -v {context.pylint_nautobot.pwd}:/local {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver} sh -c '{exec_cmd}'",
                pty=True,
            )

    return result
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)


# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------
@task(
    help={
<<<<<<< HEAD
        "force_rm": "Always remove intermediate containers",
        "cache": "Whether to use Docker's cache when building the image (defaults to enabled)",
        "pull": "Always attempt to pull a newer version of the base image",
    }
)
def build(context, force_rm=False, cache=True, pull=False):
    """Build Nautobot docker image."""
    command = "build"
=======
        "cache": "Whether to use Docker's cache when building images (default enabled)",
        "force_rm": "Always remove intermediate images",
        "hide": "Suppress output from Docker",
    }
)
def build(context, cache=True, force_rm=False, hide=False):
    """Build a Docker image."""
    print(f"Building image {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver}")
    command = f"docker build --tag {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver} --build-arg PYTHON_VER={context.pylint_nautobot.python_ver} -f Dockerfile ."
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"
<<<<<<< HEAD
    if pull:
        command += " --pull"

    print(f"Building Nautobot with Python {context.pylint_nautobot.python_ver}...")
    docker_compose(context, command)
=======

    result = context.run(command, hide=hide)
    if result.exited != 0:
        print(
            f"Failed to build image {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver}\nError: {result.stderr}"
        )
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)


@task
def generate_packages(context):
    """Generate all Python packages inside docker and copy the file locally under dist/."""
    command = "poetry build"
    run_command(context, command)


@task(
    help={
        "check": (
            "If enabled, check for outdated dependencies in the poetry.lock file, "
            "instead of generating a new one. (default: disabled)"
        )
    }
)
def lock(context, check=False):
<<<<<<< HEAD
    """Generate poetry.lock inside the Nautobot container."""
    run_command(context, f"poetry {'check' if check else 'lock --no-update'}")


# ------------------------------------------------------------------------------
# START / STOP / DEBUG
# ------------------------------------------------------------------------------
@task(help={"service": "If specified, only affect this service."})
def debug(context, service=""):
    """Start specified or all services and its dependencies in debug mode."""
    print(f"Starting {service} in debug mode...")
    docker_compose(context, "up", service=service)


@task(help={"service": "If specified, only affect this service."})
def start(context, service=""):
    """Start specified or all services and its dependencies in detached mode."""
    print("Starting Nautobot in detached mode...")
    docker_compose(context, "up --detach", service=service)


@task(help={"service": "If specified, only affect this service."})
def restart(context, service=""):
    """Gracefully restart specified or all services."""
    print("Restarting Nautobot...")
    docker_compose(context, "restart", service=service)


@task(help={"service": "If specified, only affect this service."})
def stop(context, service=""):
    """Stop specified or all services, if service is not specified, remove all containers."""
    print("Stopping Nautobot...")
    docker_compose(context, "stop" if service else "down --remove-orphans", service=service)


@task(aliases=("down",))
def destroy(context):
    """Destroy all containers and volumes."""
    print("Destroying Nautobot...")
    docker_compose(context, "down --remove-orphans")


@task
def export(context):
    """Export docker compose configuration to `compose.yaml` file.

    Useful to:

    - Debug docker compose configuration.
    - Allow using `docker compose` command directly without invoke.
    """
    docker_compose(context, "convert > compose.yaml")


@task(name="ps", help={"all": "Show all, including stopped containers"})
def ps_task(context, all=False):
    """List containers."""
    docker_compose(context, f"ps {'--all' if all else ''}")


@task
def vscode(context):
    """Launch Visual Studio Code with the appropriate Environment variables to run in a container."""
    command = "code nautobot.code-workspace"

    context.run(command)
=======
    """Generate poetry.lock inside the library container."""
    run_command(context, f"poetry {'check' if check else 'lock --no-update'}")


@task
def clean(context):
    """Remove the project specific image."""
    print(
        f"Attempting to forcefully remove image {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver}"
    )
    context.run(f"docker rmi {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver} --force")
    print(f"Successfully removed image {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver}")


@task
def rebuild(context):
    """Clean the Docker image and then rebuild without using cache."""
    clean(context)
    build(context, cache=False)


@task
def coverage(context):
    """Run the coverage report against pytest."""
    exec_cmd = "coverage run --source=pylint_nautobot -m pytest"
    run_command(context, exec_cmd)
    run_command(context, "coverage report")
    run_command(context, "coverage html")
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)


@task(
    help={
<<<<<<< HEAD
        "service": "If specified, only display logs for this service (default: all)",
        "follow": "Flag to follow logs (default: False)",
        "tail": "Tail N number of lines (default: all)",
    }
)
def logs(context, service="", follow=False, tail=0):
    """View the logs of a docker compose service."""
    command = "logs "

    if follow:
        command += "--follow "
    if tail:
        command += f"--tail={tail} "

    docker_compose(context, command, service=service)


# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
@task(help={"file": "Python file to execute"})
def nbshell(context, file=""):
    """Launch an interactive nbshell session."""
    command = [
        "nautobot-server",
        "nbshell",
        f"< '{file}'" if file else "",
    ]
    run_command(context, " ".join(command), pty=not bool(file))


@task
def shell_plus(context):
    """Launch an interactive shell_plus session."""
    command = "nautobot-server shell_plus"
    run_command(context, command)


@task
def cli(context):
    """Launch a bash shell inside the Nautobot container."""
    run_command(context, "bash")


@task(
    help={
        "service": "Docker compose service name to run command in (default: nautobot).",
        "command": "Command to run (default: bash).",
        "file": "File to run command with (default: empty)",
    },
)
def exec(context, service="nautobot", command="bash", file=""):
    """Launch a command inside the running container (defaults to bash shell inside nautobot container)."""
    command = [
        "exec",
        "--",
        service,
        command,
        f"< '{file}'" if file else "",
    ]
    docker_compose(context, " ".join(command), pty=not bool(file))


# ------------------------------------------------------------------------------
# DOCS
# ------------------------------------------------------------------------------
@task
def docs(context):
    """Build and serve docs locally for development."""
    command = "mkdocs serve -v"

    if is_truthy(context.pylint_nautobot.local):
        print(">>> Serving Documentation at http://localhost:8001")
        run_command(context, command)
    else:
        start(context, service="docs")


@task
def build_and_check_docs(context):
    """Build documentation to be available within Nautobot."""
    command = "mkdocs build --no-directory-urls --strict"
    run_command(context, command)


@task(name="help")
def help_task(context):
    """Print the help of available tasks."""
    import tasks  # pylint: disable=all  # noqa: PLC0415

    root = Collection.from_module(tasks)
    for task_name in sorted(root.task_names):
        print(50 * "-")
        print(f"invoke {task_name} --help")
        context.run(f"invoke {task_name} --help")


@task(
    help={
        "version": "Version of Nautobot Dev Example App to generate the release notes for.",
        "date": "Date of the release (default: today).",
        "keep": "Keep existing release notes files. Useful for testing. (default: False).",
    }
)
def generate_release_notes(context, version="", date="", keep=False):
    """Generate Release Notes using Towncrier."""
    command = "poetry run towncrier build"
    if not version:
        version = context.run("poetry version --short", hide=True).stdout.strip()
    command += f" --version {version}"
    if date:
        command += f" --date {date}"
    command += " --keep" if keep else " --yes"

    # TODO: Commented out until this project moves to multiple release notes files
    # version_major_minor = ".".join(version.split(".")[:2])
    # context.run(f"poetry run python development/bin/ensure_release_notes.py --version {version_major_minor}")

    # Due to issues with git repo ownership in the containers, this must always run locally.
    print(f"Running command {command}")
    context.run(command)


# ------------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------------
@task
def hadolint(context):
    """Check Dockerfile for hadolint compliance and other style issues."""
    command = "hadolint development/Dockerfile"
    run_command(context, command)


@task
def pylint(context):
    """Run pylint code analysis."""
    command = 'pylint --init-hook "import nautobot; nautobot.setup()" --rcfile pyproject.toml pylint_nautobot'
    run_command(context, command)
=======
        "pattern": "Only run tests which match the given substring. Can be used multiple times.",
        "label": "Module path to run (e.g., tests/unit/test_foo.py). Can be used multiple times.",
    },
    iterable=["pattern", "label"],
)
def pytest(context, pattern=None, label=None):
    """Run pytest test cases."""
    exec_cmd = "pytest -vv --doctest-modules pylint_nautobot/ && coverage run --source=pylint_nautobot -m pytest && coverage report"
    run_command(context, exec_cmd)

    doc_test_cmd = "pytest -vv --doctest-modules pylint_nautobot/"
    pytest_cmd = "coverage run --source=pylint_nautobot -m pytest"
    if pattern:
        pytest_cmd += "".join([f" -k {_pattern}" for _pattern in pattern])
    if label:
        pytest_cmd += "".join([f" {_label}" for _label in label])
    coverage_cmd = "coverage report"
    exec_cmd = " && ".join([doc_test_cmd, pytest_cmd, coverage_cmd])
    run_command(context, exec_cmd)
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)


@task(aliases=("a",))
def autoformat(context):
    """Run code autoformatting."""
    ruff(context, action=["format"], fix=True)


@task(
    help={
<<<<<<< HEAD
        "action": "Available values are `['lint', 'format']`. Can be used multiple times. (default: `['lint']`)",
        "fix": "Automatically fix selected actions. May not be able to fix all issues found. (default: False)",
        "output_format": "See https://docs.astral.sh/ruff/settings/#output-format for details. (default: `full`)",
    },
    iterable=["action"],
)
def ruff(context, action=None, fix=False, output_format="full"):
    """Run ruff to perform code formatting and/or linting."""
    if not action:
        action = ["lint"]

    if "format" in action:
        command = "ruff format"
        if not fix:
            command += " --check"
        command += " ."
        run_command(context, command)

    if "lint" in action:
        command = "ruff check"
        if fix:
            command += " --fix"
        command += f" --output-format {output_format} ."
        run_command(context, command)
=======
        "action": "Available values are `['lint', 'format']`. Can be used multiple times. (default: `['lint', 'format']`)",
        "target": "File or directory to inspect, repeatable (default: all files in the project will be inspected)",
        "fix": "Automatically fix selected actions. May not be able to fix all issues found. (default: False)",
        "output_format": "See https://docs.astral.sh/ruff/settings/#output-format for details. (default: `concise`)",
    },
    iterable=["action", "target"],
)
def ruff(context, action=None, target=None, fix=False, output_format="concise"):
    """Run ruff to perform code formatting and/or linting."""
    if not action:
        action = ["lint", "format"]
    if not target:
        target = ["."]

    exit_code = 0

    if "format" in action:
        command = "ruff format "
        if not fix:
            command += "--check "
        command += " ".join(target)
        if not run_command(context, command):
            exit_code = 1

    if "lint" in action:
        command = "ruff check "
        if fix:
            command += "--fix "
        command += f"--output-format {output_format} "
        command += " ".join(target)
        if not run_command(context, command):
            exit_code = 1

    if exit_code != 0:
        raise Exit(code=exit_code)


@task
def pylint(context):
    """Run pylint for the specified name and Python version.

    Args:
        context (obj): Used to run specific commands
    """
    exec_cmd = 'find . -name "*.py" | grep -vE "tests/unit" | xargs pylint'
    run_command(context, exec_cmd)
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)


@task
def yamllint(context):
    """Run yamllint to validate formatting adheres to NTC defined YAML standards.

    Args:
<<<<<<< HEAD
    ----
        context (obj): Used to run specific commands
    """
    command = "yamllint . --format standard"
    run_command(context, command)
=======
        context (obj): Used to run specific commands
    """
    exec_cmd = "yamllint ."
    run_command(context, exec_cmd)


@task
def cli(context):
    """Enter the image to perform troubleshooting or dev work.

    Args:
        context (obj): Used to run specific commands
    """
    dev = f"docker run -it -v {context.pylint_nautobot.pwd}:/local {context.pylint_nautobot.image_name}:{context.pylint_nautobot.image_ver} /bin/bash"
    context.run(f"{dev}", pty=True)
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)


@task(
    help={
        "lint-only": "Only run linters; unit tests will be excluded. (default: False)",
    }
)
def tests(context, lint_only=False):
<<<<<<< HEAD
    """Run all tests for this app."""
    # If we are not running locally, start the docker containers so we don't have to for each test
    if not is_truthy(context.pylint_nautobot.local):
        print("Starting Docker Containers...")
        start(context)
=======
    """Run all tests for the specified name and Python version.

    Args:
        context (obj): Used to run specific commands
        lint_only (bool): If True, only run linters and skip unit tests.
    """
    # If we are not running locally, start the docker containers so we don't have to for each test
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)
    # Sorted loosely from fastest to slowest
    print("Running ruff...")
    ruff(context)
    print("Running yamllint...")
    yamllint(context)
    print("Running poetry check...")
    lock(context, check=True)
    print("Running pylint...")
    pylint(context)
    print("Running mkdocs...")
    build_and_check_docs(context)
    if not lint_only:
        print("Running unit tests...")
        pytest(context)
    print("All tests have passed!")


@task
<<<<<<< HEAD
def pytest(context, verbose=False, names=""):
    """Run pytest test cases."""
    command = [
        "pytest",
        "-vvv" if verbose else "",
        names if names else "",
    ]

    run_command(context, " ".join(command))
=======
def build_and_check_docs(context):
    """Build documentation and test the configuration."""
    command = "mkdocs build --no-directory-urls --strict"
    run_command(context, command)

    # Check for the existence of a release notes file for the current version if it's not a prerelease.
    version = context.run("poetry version --short", hide=True)
    match = re.match(r"^(\d+)\.(\d+)\.\d+$", version.stdout.strip())
    if match:
        major = match.group(1)
        minor = match.group(2)
        release_notes_file = Path(__file__).parent / "docs" / "admin" / "release_notes" / f"version_{major}.{minor}.md"
        if not release_notes_file.exists():
            print(f"Release notes file `version_{major}.{minor}.md` does not exist.")
            raise Exit(code=1)


@task
def docs(context):
    """Build and serve docs locally for development."""
    exec_cmd = "mkdocs serve -v"
    run_command(context, exec_cmd, port="8001:8001")


@task(
    help={
        "version": "Version of pylint_nautobot to generate the release notes for.",
        "date": "Date of the release (default: today).",
    }
)
def generate_release_notes(context, version="", date=""):
    """Generate Release Notes using Towncrier."""
    if not version:
        version = context.run("poetry version --short", hide=True).stdout.strip()

    version_major_minor = ".".join(version.split(".")[:2])
    context.run(f"poetry run python bin/ensure_release_notes.py --version {version_major_minor}")

    command = f"poetry run towncrier build --version {version} --yes"
    if date:
        command += f" --date {date}"
    # Due to issues with git repo ownership in the containers, this must always run locally.
    context.run(command)
>>>>>>> 20e684d (Cookie initially baked targeting develop by NetworkToCode Cookie Drift Manager Tool)
