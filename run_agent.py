#!/usr/bin/env python

from src.agent import Agent
import src.actions as actions

def run():
    a = Agent()
    wkflw = a.workflow

    if a.workflow_step is not None:
        wkflw = {a.workflow_step: a.workflow[a.workflow_step]}

    for act in wkflw:
        if 'prompt' in a.workflow[act]:
            print(f'Building prompt for {act}...')

            prompt = a.build_prompt(a.workflow[act])

            print(f'Running prompt for {act}...')

            a.outputs[act] = a.run_prompt(a.config['models']['language'], prompt)

            if 'output' in a.workflow[act] and bool(a.workflow[act]['output']) is True:
                print(f'Writing output for {act}...')

                with open(f'./workflows/{a.args.workflow}/outputs/{act}.txt', 'w') as fh:
                    fh.write(a.outputs[act])
        
        if 'context' in a.workflow[act]:
            func = getattr(actions, act)
            ctx = {c: a.outputs[c] for c in a.workflow[act]['context']}
            func(**ctx)

    # Create content for GitHub
    # files = {
    #     "summary.txt": summary,
    #     "draft_email.txt": email
    # }

    # post_to_github(
    #     repo="username/repo-name",
    #     token="ghp_your_github_token",
    #     files=files,
    #     commit_message="Add job summary and email draft"
    # )

if __name__ == "__main__":
    run()
