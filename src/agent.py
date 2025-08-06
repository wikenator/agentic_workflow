#!/usr/bin/env python
# encoding: utf-8

import os, sys
from collections import defaultdict
import argparse
import ollama
import yaml
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

class Agent():
    def __init__(self):
        self.workflow_step = None
        self.outputs = defaultdict(dict)
        self.config = self._load_config("config.yaml")
        self.args = self._parse_args()

        if self.args.workflow is None:
            sys.exit('No workflow provided.')

        try:
            self.workflow = self._load_workflow()

        except Exception as e:
            raise('Workflow file not found.')
        
        if self.args.step_name is not None:
            if self.args.step_name not in self.workflow:
                raise('Workflow step not found')
            
            self.workflow_step = self.args.step_name

    def _load_config(self, config_path):
        '''
        Load configuration.
        :param config_path: Local path to configuration YAML.
        '''

        fh = open(config_path, 'r')

        return yaml.load(fh, Loader=Loader)
    
    def _load_workflow(self):
        fh = open(f'./workflows/{self.args.workflow}.yaml', 'r')

        return yaml.load(fh, Loader=Loader)
    
    def _parse_args(self):
        cmd_line_parser = argparse.ArgumentParser(description='Run simple agentic workflows.')
        cmd_line_parser.add_argument('-w', '--workflow', action='store', default=None, type=str, help='Name of workflow to run.')
        cmd_line_parser.add_argument('-s', '--step_name', action='store', default=None, type=str, help='Name of step within workflow to run.')
        args = cmd_line_parser.parse_args()

        return args
    
    def build_prompt(self, action):
        prompt = ''

        if 'prompt' in action:
            prompt += action['prompt']

            if 'context_file' in action:
                with open(f"./workflows/{self.args.workflow}/{action['context_file']}", 'r') as fh:
                    prompt += fh.read()

                prompt += '\n\n'

        if 'multishot_prompt' in action:
            prompt += action['multishot_prompt']

            if 'multishot_file' in action:
                with open(f"./workflows/{self.args.workflow}/{action['multishot_file']}", 'r') as fh:
                    prompt += fh.read()

        return prompt

    def run_prompt(self, model, prompt, verify_prompt=None):
        try:
            response = ollama.generate(
                model=model,
                prompt=prompt if verify_prompt is None else verify_prompt,
            )

        except Exception as e:
            raise(e)

        return_val = response['response']

        verification = self.verify_response(model, prompt, return_val)

        if verification.startswith('no'):
            print('Verification failed, trying again.')

            verify_prompt = f"Given this output: {return_val}\n\nand this error message: {verification}\n\nrun this again: {prompt}"
            return_val = self.run_prompt(model, prompt, verify_prompt)

        return return_val

    def verify_response(self, model, prompt, response):
        response = ollama.generate(
            model=model,
            prompt=f"Given the prompt: {prompt}\n\nWas the output appropriate and relevant? Output: {response}\n\nAnswer yes or no only."
        )

        return response['response'].lower()
    