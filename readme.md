# QnA-LLM: Document Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Chainlit](https://img.shields.io/badge/Chainlit-Framework-orange.svg)](https://chainlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready document question-answering system built with Chainlit and LangChain, supporting both cloud-based and offline LLM inference.

## Features

- **Document Q&A**: Upload PDFs and text files for intelligent querying
- **Multi-Modal Support**: Cloud (OpenAI) and offline (local models) inference
- **Research Assistant**: ArXiv paper search and analysis
- **Vector Search**: ChromaDB integration for semantic document retrieval
- **Interactive UI**: Web-based chat interface with file upload

## Quick Start

### Prerequisites
- Python 3.9 or higher
- OpenAI API key (for cloud features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShyamSanjeyS/QNA-LLM.git
   cd QnA-LLM
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**
   ```bash
   # Create config.yml
   echo "openai:\n  api-key: your-api-key-here" > config.yml
   ```

4. **Run the application**
   ```bash
   # Basic chat interface
   chainlit run main.py -w
   
   # Document Q&A (requires model download)
   chainlit run document_qa.py -w
   
   # Research assistant
   chainlit run internet_browsing_arxiv_chainlit.py -w
   ```

## Applications

| Application | Description | Requirements |
|-------------|-------------|--------------|
| `main.py` | Basic OpenAI chat interface | OpenAI API key |
| `document_qa.py` | PDF/document analysis (offline) | Local model file |
| `langchain_integration.py` | LangChain-powered chat | OpenAI API key |
| `internet_browsing_arxiv_chainlit.py` | ArXiv research assistant | OpenAI API key |

## Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Chainlit UI   │────│  LangChain   │────│  Vector Store   │
└─────────────────┘    └──────────────┘    └─────────────────┘
         │                       │                    │
         │                       │                    │
    ┌─────────┐            ┌───────────┐        ┌──────────┐
    │ OpenAI  │            │ Local LLM │        │ ChromaDB │
    │   API   │            │  (.gguf)  │        │          │
    └─────────┘            └───────────┘        └──────────┘
```

## Configuration

### Environment Setup
```yaml
# config.yml
openai:
  api-key: sk-your-actual-api-key
```

### Local Model Setup (Optional)
For offline document processing:
1. Create `models/` directory
2. Download a compatible `.gguf` model (e.g., Mistral-7B)
3. Update model path in `document_qa.py`

## Usage Examples

### Document Analysis
```python
# Upload PDF → Ask questions → Get contextual answers
"What are the main findings in this research paper?"
"Summarize the methodology section"
```

### Research Assistant
```python
# Search ArXiv → Get latest research insights
"What is RLHF for Large Language Models?"
"Latest developments in transformer architectures"
```

## API Reference

### Core Components
- **Document Loader**: PDF, TXT file processing
- **Text Splitter**: Chunking for optimal retrieval
- **Embeddings**: Sentence transformers for semantic search
- **Vector Store**: ChromaDB for similarity matching
- **LLM Chain**: Question-answering pipeline

## Development

### Project Structure
```
QnA-LLM/
├── main.py                    # Basic chat interface
├── document_qa.py             # Document Q&A system
├── langchain_integration.py   # LangChain implementation
├── internet_browsing_*.py     # Research tools
├── config.yml                 # Configuration
├── requirements.txt           # Dependencies
├── models/                    # Local model storage
└── README.md                  # Documentation
```

### Testing
```bash
# Run component tests
python chroma_db_basics.py

# Check project health
python check.py  # Use the provided checker script
```

## Deployment

### Local Development
```bash
chainlit run [app].py -w --port 8000
```

### Production Considerations
- Use environment variables for API keys
- Implement rate limiting for API calls
- Add error logging and monitoring
- Configure reverse proxy for HTTPS

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Create Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Chainlit](https://chainlit.io) - Conversational AI framework
- [LangChain](https://langchain.com) - LLM application development
- [ChromaDB](https://trychroma.com) - Vector database
- [OpenAI](https://openai.com) - Language model API

---

**Built with ❤️ for intelligent document processing**