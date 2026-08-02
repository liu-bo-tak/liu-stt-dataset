# QA Knowledge Base Dataset

This repository contains a collected dataset of materials for QA engineers, as well as the tool (ETL pipeline) used for its automated population.

## Dataset Structure

This branch implements the **"by-topic"** approach. Data from various sources is combined and sorted into domain categories based on standards (e.g., ISTQB).
*A planned alternative branch will implement the **"by-source"** approach, where the structure will mirror the original hierarchy of the websites or authors.*

Current structure (by-topic branch):
- `data/`
  - `sdlc/`
  - `api_testing/`
  - `automation_tools/`
  - ...and other domain categories.

## Collection Tool (`tools/pipeline.py`)

A custom ETL script is used for automated collection, operating in three stages:
1. **Discover:** URL collection (`raw_discovery.jsonl`).
2. **Classify:** LLM analysis (Gemini API) via `google-genai` and `pydantic`. The Structured Outputs (`Enum`) mechanism is used to strictly map articles to existing thematic categories. A sliding window algorithm prevents API blocking (limit of 5 requests/min).
3. **Download:** Asynchronous downloading (`httpx`), cleaning HTML from ads/navigation (`BeautifulSoup4`), and saving in Markdown (`markdownify`).

### Dependencies and Usage
The classification stage requires an environment variable:
`export GEMINI_API_KEY="your_key"`

Run the pipeline:
```bash
python tools/pipeline.py -h
```

## Next Steps
- Add support for parsing PDF (PyMuPDF) and DOCX (python-docx). All new data will be organically integrated into the existing thematic categories.
