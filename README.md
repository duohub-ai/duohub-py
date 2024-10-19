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
    - [Options](#options)
    - [Default Mode - Voice AI Compatible](#default-mode---voice-ai-compatible)
      - [Default Mode Response](#default-mode-response)
    - [Assisted Queries - Voice AI Compatible](#assisted-queries---voice-ai-compatible)
      - [Assisted Mode Results](#assisted-mode-results)
    - [Fact Queries](#fact-queries)
      - [Fact Query Response](#fact-query-response)
    - [Combining Options](#combining-options)
      - [Combining Options Response](#combining-options-response)
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

Basic usage is as follows:

```python
from duohub import Duohub
client = Duohub(api_key="your_api_key")
response = client.query(query="What is the capital of France?", memoryID="your_memory_id")
print(response)
```

Output schema is as follows:  

```json
{
  "payload": "string",
  "facts": [
    {
      "content": "string"
    }
  ],
  "token_count": 0
}
```

Token count is the number of tokens in the graph context. Regardless of your mode, you will get the same token content if you use the same query and memory ID on a graph.

### Options

- `facts`: Whether to return facts in the response. Defaults to `False`.
- `assisted`: Whether to return an answer in the response. Defaults to `False`.
- `query`: The query to search the graph with.
- `memoryID`: The memory ID to isolate your search results to.

### Default Mode - Voice AI Compatible

When you only pass a query and memory ID, you are using default mode. This is the fastest option, and most single sentence queries will get a response in under 50ms. 


```python
from duohub import Duohub

client = Duohub(api_key="your_api_key")

response = client.query(query="What is the capital of France?", memoryID="your_memory_id")

print(response)
```

#### Default Mode Response

Your response (located in `payload`) is a string representation of a subgraph that is relevant to your query returned as the payload. You can pass this to your context window using a system message and user message template. 

### Assisted Queries - Voice AI Compatible

If you pass the `assisted=True` parameter to the client, the API will add reasoning to your query and uses the graph context to returns the answer. Assisted mode will add some latency to your query, though it should still be under 250ms.

Using assisted mode will improve the results of your chatbot as it will eliminate any irrelevant information before being passed to your context window, preventing your LLM from assigning attention to noise in your graph results.

```python
from duohub import Duohub

client = Duohub(api_key="your_api_key")

response = client.query(query="What is the capital of France?", memoryID="your_memory_id", assisted=True)

print(response)
``` 

#### Assisted Mode Results

Assisted mode results will be a JSON object with the following structure:

```json
{
    "payload": "The capital of France is Paris.",
    "facts": [],
    "tokens": 100,
}
```

### Fact Queries 

If you pass `facts=True` to the client, the API will return a list of facts that are relevant to your query. This is useful if you want to pass the results to another model for deeper reasoning.

Because the latency for a fact query is higher than default or assisted mode, we recommend not using these in voice AI or other low-latency applications.

It is more suitable for chatbot workflows or other applications that do not require real-time responses.

```python
from duohub import Duohub

client = Duohub(api_key="your_api_key")

response = client.query(query="What is the capital of France?", memoryID="your_memory_id", facts=True)

print(response)
```

#### Fact Query Response

Your response (located in `facts`) will be a list of facts that are relevant to your query.

```json
{
  "payload": "subgraph_content",
  "facts": [
    {
      "content": "Paris is the capital of France."
    },
    {
      "content": "Paris is a city in France."
    },
    {
      "content": "France is a country in Europe."
    }
  ],
  "token_count": 100
}
```

### Combining Options

You can combine the options to get a more tailored response. For example, you can get facts and a payload:

```python
from duohub import Duohub

client = Duohub(api_key="your_api_key")

response = client.query(query="What is the capital of France?", memoryID="your_memory_id", facts=True, assisted=True)

print(response)
```

#### Combining Options Response

Your response will be a JSON object with the following structure:

```json
{
  "payload": "Paris is the capital of France.",
  "facts": [
    {
      "content": "Paris is the capital of France."
    },
    {
      "content": "Paris is a city in France."
    },
    {
      "content": "France is a country in Europe."
    }
  ],
  "token_count": 100
}
```



## Contributing

We welcome contributions to this client! Please feel free to submit a PR. If you encounter any issues, please open an issue.