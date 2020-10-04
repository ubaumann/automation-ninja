import subprocess

result = {"success": [], "failed": [], "uploaded": [], "upload_faild": []}

build_commands = ["docker", "build", ".", "--no-cache", "--tag", "ubaumann/automation-ninja:latest"]
try:
    r = subprocess.run(build_commands, check=True)
except subprocess.CalledProcessError as e:
    result["failed"].append("latest")
else:
    result["success"].append("latest")

builds = {
    "ansible": {"install": "pip install -q ansible", "tag": "ansible"},
    "nornir": {"install": "pip install -q nornir", "tag": "nornir"},
    "nornir_dev": {
        "install": "git clone https://github.com/nornir-automation/nornir.git && cd nornir && git checkout 3.0.0 && $HOME/.poetry/bin/poetry install --no-interaction --no-ansi",
        "tag": "nornir_dev3.0.0",
    },
    "netmiko": {"install": "pip install -q netmiko", "tag": "netmiko"},
    "netmiko_dev": {
        "install": "git clone https://github.com/ktbyers/netmiko.git && cd netmiko  && pip install -e .",
        "tag": "netmiko_dev",
    },
    "napalm": {"install": "pip install -q napalm", "tag": "napalm"},
    "napalm_dev": {
        "install": "git clone https://github.com/napalm-automation/napalm.git && cd napalm  && pip install -e .",
        "tag": "napalm_dev",
    },
}

for build in builds.values():
    dockerfile = f"""
    FROM ubaumann/automation-ninja:latest

    LABEL maintainer="Urs Baumann <docker@m.ubaumann.ch>"

    RUN {build["install"]}

    CMD [ "/bin/bash" ]
    """

    build_commands = [
        "docker",
        "build",
        "--no-cache",
        "--tag",
        f"ubaumann/automation-ninja:{build['tag']}",
        "-",
    ]
    try:
        r = subprocess.run(build_commands, input=dockerfile, text=True, check=True)
    except subprocess.CalledProcessError as e:
        result["failed"].append(build["tag"])
    else:
        result["success"].append(build["tag"])

print(result)

for tag in result["success"]:
    build_commands = ["docker", "push", f"ubaumann/automation-ninja:{tag}"]
    try:
        r = subprocess.run(build_commands, check=True)
    except subprocess.CalledProcessError as e:
        result["uploaded"].append(tag)
    else:
        result["uploaded"].append(tag)
