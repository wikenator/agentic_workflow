#!/usr/bin/env python

import ollama
import subprocess

def push_to_github(*args, **kwargs):
    subprocess.call(['git', 'add', f"workflows/{kwargs['workflow']}/outputs/*"])
    subprocess.call(['git', 'commit', '-m', f"adding outputs from {kwargs['workflow']} workflow"])
    subprocess.call(['git', 'push', 'origin'])