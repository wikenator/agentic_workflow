# Agentic Workflow
Simple agentic workflow implementation that can be customized to perform specific tasks.

## Architecture

### Config Files
Each agentic workflow is defined in a `.yaml` file in the `workflows` folder. To keep things simple, the workflow steps run in series from top to bottom. Prompts can be configured in these files, as well as functions that can utilize the output of previous steps.

### Agent
The agent class is just a simple Python class containing functionality to:
- load configuration files
- build and run prompts
- verify LLM outputs

LLM functionality is handled by the `ollama` library in order to avoid costly API calls or network latency. This project uses the `Llama-3.2-1B-Instruct-GGUF` model.

### Actions
Functions in the actions file are used to support agentic workflows. These functions call out to external programs or services. Steps named in workflow configs should be the same name as a corresponding action function.

## Configurations

Here is a sample agentic workflow config file (`test.yaml`):

```
step1:
  prompt: [write prompt here]
  context_file: [context that the prompt can reference. located under workflows/test/]
  output: [true if output should be saved to workflows/test/outputs/]
step2:
  prompt: [write prompt here]
  context_file: [context for the prompt]
  multishot_prompt: [appended to the prompt with instructions on how to handle multishot examples]
  multishot_file: [context for the multishot prompt]
  output: true
step3:
  context: [use the output from the listed step names in this step]
    - step1
    - step2
```