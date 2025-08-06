#!/usr/bin/env python

import ollama
import subprocess

def push_to_github(*args, **kwargs):
    subprocess.call(['git', 'add', 'workflows/test/outputs/*'])