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
    - [Additional Methods](#additional-methods)
      - [Adding Files](#adding-files)
      - [Creating a Memory](#creating-a-memory)
      - [Managing Files in Memory](#managing-files-in-memory)
      - [Starting Ingestion](#starting-ingestion)
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
  "payload": [
    {
      "content": "string",
      "score": 1
    }
  ],
  "facts": [
    {
      "content": "string"
    }
  ],
  "sources": [
    {
      "id": "string",
      "name": "string", 
      "url": "string",
      "score": 1
    }
  ]
}
```

### Options

- `facts`: Whether to return facts in the response. Defaults to `False`.
- `assisted`: Whether to return an answer in the response. Defaults to `False`.
- `query`: The query to search the graph with.
- `memoryID`: The memory ID to isolate your search results to.
- `top_k`: Number of top memories to return. Defaults to 5.

### Default Mode - Voice AI Compatible

When you only pass a query and memory ID, you are using default mode. This is the fastest option, and most single sentence queries will get a response in under 50ms. 


```python
from duohub import Duohub

client = Duohub(api_key="your_api_key")

response = client.query(query="What is the capital of France?", memoryID="your_memory_id")

print(response)
```

#### Default Mode Response

Your response (located in `payload[0].content`) is a string representation of a subgraph that is relevant to your query returned as the payload. You can pass this to your context window using a system message and user message template. 

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
    "payload": [
        {
            "content": "The capital of France is Paris.",
            "score": 1
        }
    ],
    "facts": [],
    "sources": []
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

Your response will include both payload and facts:

```json
{
  "payload": [
    {
      "content": "Paris is the capital of France.",
      "score": 1
    }
  ],
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
  "sources": [
    {
      "id": "123",
      "name": "Wikipedia",
      "url": "https://wikipedia.org/wiki/Paris",
      "score": 1
    }
  ]
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
  "payload": [
    {
      "content": "Paris is the capital of France.",
      "score": 1
    }
  ],
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
  "sources": [
    {
      "id": "123",
      "name": "Wikipedia",
      "url": "https://wikipedia.org/wiki/Paris",
      "score": 1
    }
  ]
}
```

### Additional Methods

#### Adding Files

You can add files to Duohub using either local files or external URIs:

```python
# Add a local file
response = client.add_file(file_path="path/to/your/file.txt")

# Add an external website or sitemap
response = client.add_file(
    external_uri="https://example.com",
    file_type="website"  # Options: 'website', 'sitemap', or 'website_bulk'
)
```

#### Creating a Memory

Create a new memory (graph or vector storage):

```python
response = client.create_memory(
    name="My Memory",
    memory_type="graph",  # or "vector"
    description="Optional description",
    ontology="culture",  # Required for graph type. Options: culture, essays, support_requests
    chunk_size=250,  # Only for vector type
    chunk_overlap=10,  # Only for vector type (1-50)
    webhook_url="https://your-webhook.com",  # Optional
    acceleration=False  # Optional
)
```

#### Managing Files in Memory

Add files to an existing memory:

```python
response = client.add_files_to_memory(
    memory_id="your_memory_id",
    files=["file_id_1", "file_id_2"]
)
```

Remove a file from memory:

```python
response = client.delete_file_from_memory(
    memory_id="your_memory_id",
    file_id="file_id_to_remove"
)
```

#### Starting Ingestion

After adding files, start the ingestion process:

```python
response = client.start_ingestion(
    memory_id="your_memory_id"
)
```

Note: The file management endpoints can only be used with memories created on or after 17-Dec-2024.

## Contributing

We welcome contributions to this client! Please feel free to submit a PR. If you encounter any issues, please open an issue.