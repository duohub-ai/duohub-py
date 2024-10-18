# duohub GraphRAG python client

![PyPI version](https://img.shields.io/pypi/v/duohub.svg)

This is a python client for the Duohub API. 

Duohub is a blazing fast graph RAG service designed for voice AI and other low-latency applications. It is used to retrieve memory from your knowledege graph in under 50ms.

You will need an API key to use the client. You can get one by signing up on the [Duohub app](https://app.duohub.ai). For more information, visit our website: [duohub.ai](https://duohub.ai).

## Table of Contents

- [duohub GraphRAG python client](#duohub-graphrag-python-client)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Default Mode - Voice AI Compatible](#default-mode---voice-ai-compatible)
      - [VoiceAI Mode Results](#voiceai-mode-results)
    - [Assisted Mode](#assisted-mode)
      - [Assisted Mode Results](#assisted-mode-results)
  - [Contributing](#contributing)

## Installation

```bash
pip install duohub
```

or 

```bash
poetry add duohub
```

## Usage

### Default Mode - Voice AI Compatible

```python
from duohub import Duohub

duohub = Duohub(api_key="your_api_key")

result = duohub.query(query="What is the capital of France?", memoryID="your_memory_id")

print(result)
```

#### VoiceAI Mode Results

In voice AI mode, you will get a string representation of a subgraph that is relevant to your query. You can pass this to your chat bot using a system message and user message template. 

### Assisted Mode

Assisted mode adds reasoning to your query and returns the answer as well as 3 facts instead of a subgraph. 

This adds some latency to your query, so it is not recommended for real-time applications, but can offer an exceptional experience to text-based AI applications or agentic workflows.

```python
from duohub import Duohub

duohub = Duohub(api_key="your_api_key")

result = duohub.query(query="What is the capital of France?", memoryID="your_memory_id", assisted=True)

print(result)
``` 

#### Assisted Mode Results

Assisted mode results will be a JSON object with the following structure:

```json
{
    "payload": "The capital of France is Paris.",
    "facts": [
        {
            "content": "Paris is the capital of France.",
        },
        {
            "content": "Paris is a city in France.",
        },
         {
            "content": "France is a country in Europe.",
        },
    ],
    "tokens": 100,
}
```

## Contributing

We welcome contributions to this client! Please feel free to submit a PR. If you encounter any issues, please open an issue.