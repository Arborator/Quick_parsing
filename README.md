# ArboratorGrew Quick parsing interface

This website provides an interactive interface for syntactic parsing. It uses [BertForDeprel](https://github.com/kirianguiller/BertForDeprel), similar to UDPipe. It allows users to input text or files and analyze their linguistic structure using various trained parsing models.

## Architecture

```
Quick_parsing (this repo)  ──HTTP──▶  arborator-parser (backend)  ──▶  BertForDeprel
   - text tokenization                 - model management on disk
   - file upload UI                    - Celery task queue (train / parse)
   - proxies requests to backend       - writes CoNLL-U, invokes BertForDeprel
```

- **Quick_parsing** (this repo) is the user-facing Flask frontend. It tokenizes plain text into CoNLL-U format (using spaCy or a custom tokenizer), handles file uploads, and proxies all parsing/training requests via HTTP to the backend. It does not modify CoNLL-U content — it passes it through and returns the backend's response.
- **[arborator-parser](https://github.com/Arborator/arborator-parser)** is the Flask + Celery backend. It manages model files on disk, runs BertForDeprel training and inference as Celery tasks, and returns parsed CoNLL-U. All model logic (including the gloss swap for gloss-based parsing) lives there.

### Gloss parser models

The backend supports gloss-based parsing models (project names starting with `gloss_`). When such a model is selected, the backend automatically swaps `Gloss=` values from the MISC column into the FORM column before parsing, and restores the original forms afterward. This happens entirely in [arborator-parser](https://github.com/Arborator/arborator-parser) — no changes are needed in Quick_parsing.

