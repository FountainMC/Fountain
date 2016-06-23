import os
import shutil
from sys import stderr
from os import path
from urllib.request import urlretrieve
import re
from subprocess import run, PIPE


minecraft_version="1.9.4"
jdiff_jar=path.join("work", "JDiff.jar")
mappings_path=path.join("mappings", "obf2mcp-" + minecraft_version + ".srg")

def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def setup():
    if not path.exists("work"): os.mkdir("work")
    if not path.exists("mappings"): os.mkdir("mappings")

    if not path.exists(mappings_path):
        print("Downloading mappings for", minecraft_version, "to", mappings_path)
        urlretrieve("https://raw.githubusercontent.com/Techcable/MinecraftMappings/master/" + minecraft_version + "/obf2mcp.srg", mappings_path)
        print("Done downloading mappings")

    if not path.exists(jdiff_jar):
        print("Downloading JDiff jar")
        urlretrieve('https://github.com/Techcable/JDiff/releases/download/v1.0.1/JDiff.jar', jdiff_jar)
        print("Done downloading JDiff")

    if not shutil.which("java"):
        eprint("Java not found")
        exit(1)

    java_version = None
    try:
        java_version = int(run(["java", "-version"], stderr=PIPE, universal_newlines=True).stderr.splitlines(False)[0].split(' ')[2].replace('"', '').split('.')[1])
    except:
        eprint("Unable to detect java version")
        exit(1)
    if java_version < 8:
        eprint("Unsupported java version detected", java_version)
        exit(1)

def runJDiff(*args):
    run(["java", "-XX:+UseG1GC", "-jar", jdiff_jar] + list(args), check=True)
