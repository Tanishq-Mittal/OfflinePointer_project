# OfflinePointer

OfflinePointer is a prototype that uses a local Ollama model to identify a UI control from a text request and return the control's coordinates. It currently uses a bundled TextEdit fixture; it does not control the mouse or click anything.

## Requirements

- Python 3.11 or newer
- [Ollama](https://ollama.com/) installed and running locally
- The default models: `qwen3:1.7b` (picker) and `llama3.2:3b` (escalation)

## Get started

Clone the repository and change into its directory:

```sh
git clone https://github.com/Tanishq-Mittal/OfflinePointer_project.git
cd OfflinePointer_project
```

### Windows (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
ollama pull qwen3:1.7b
ollama pull llama3.2:3b
```

### macOS

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-macos.txt
ollama pull qwen3:1.7b
ollama pull llama3.2:3b
```

Ollama usually runs as a background service. If it is not running, start it in a separate terminal with `ollama serve`.

## Run

With the virtual environment activated and Ollama running:

```sh
python main.py "text ko bold karo"
```

The program reads `controls/fixtures/textedit.json`, asks the local model to select a candidate, verifies the result, and prints the target and coordinates. The first model request may take longer while Ollama loads the model.

Run the test suite with:

```sh
python -m pytest -q
```

## Configuration

The defaults are `OLLAMA_HOST=http://localhost:11434`, `PICKER_MODEL=qwen3:1.7b`, and `ESCALATION_MODEL=llama3.2:3b`. Override these by setting environment variables in your shell. `.env.example` documents the variable names; the application does not automatically load a `.env` file.

## Current limitations

- The command-line flow uses fixture data on both Windows and macOS; it is not yet connected to live UI controls.
- The macOS Accessibility reader is incomplete and has not been validated against real applications.
- No cursor overlay, cursor movement, or clicking is implemented.

See `requirements.txt` for the shared dependencies and `requirements-macos.txt` for the additional macOS dependencies. See [LICENSE](LICENSE) for the project licence.
