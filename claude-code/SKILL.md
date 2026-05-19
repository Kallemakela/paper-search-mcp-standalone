---
name: paper-search
description: Search, download, and read academic papers from 20+ sources (arXiv, PubMed, Semantic Scholar, CrossRef, etc). Use when the user asks to find papers, search for research, look up academic literature, download a paper PDF, or extract text from a paper.
---

# Paper Search

Search, download, and read academic papers via the `paper-search` CLI.

## CLI Usage

All commands run via:
```bash
uv run --directory <REPO_PATH> paper-search <command> [args]
```

Replace `<REPO_PATH>` with the absolute path to your clone of this repository.

Commands are generated from the same shared API functions as the MCP server.

### Search across sources
```bash
uv run --directory <REPO_PATH> paper-search search "<query>" --max-results-per-source <n> --sources <sources> --year <year>
```
- `--max-results-per-source`: results per source (default: 5)
- `--sources`: comma-separated sources or "all" (default: all)
- `--year`: year filter for Semantic Scholar (e.g. "2020", "2018-2022")

For speed, prefer targeted sources (`--sources arxiv,semantic,crossref`) over "all" unless broad coverage is needed.

### Search one source
```bash
uv run --directory <REPO_PATH> paper-search search_arxiv "<query>" --max-results 10
```

### Download PDF
```bash
uv run --directory <REPO_PATH> paper-search download_arxiv <paper_id> --save-path ./downloads
```

### Read (extract text)
```bash
uv run --directory <REPO_PATH> paper-search read_arxiv_paper <paper_id> --save-path ./downloads
```

### List sources
```bash
uv run --directory <REPO_PATH> paper-search sources
```

## Output

Search and metadata commands return JSON. Read commands return plain text. Config warnings go to stderr and can be ignored.

## Sources

arxiv, pubmed, biorxiv, medrxiv, google_scholar, iacr, semantic, crossref, openalex, pmc, core, europepmc, dblp, openaire, citeseerx, doaj, base, zenodo, hal, ssrn, unpaywall

Optional (env vars): ieee (`IEEE_API_KEY`), acm (`ACM_API_KEY`)

## Workflow

1. Search with targeted sources to find papers
2. Present results as a table: title, authors, year, source, DOI/URL
3. If the user wants full text, use the matching `read_*` command
4. If the user wants the PDF, use the matching `download_*` command and report the saved path
