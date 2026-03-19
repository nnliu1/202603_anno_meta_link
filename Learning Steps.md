# Learning Steps

## Preliminaries

- There are two possibilities to follow the hands on exercises:
  - https://mybinder.org, oder
  - git clone

### 1- My binder
1- go to https://mybinder.org paste the GitHub repository name [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/nnliu1/202603_anno_meta_link/HEAD)

2- binder installs the requirements.txt and the participant can directly start using the jupyter

### 2- Cloning
0- clone the project from `git@github.com:nnliu1/202603_anno_meta_link.git`

1- if uv is installed use uv to make a virtual environment:
```bash
uv venv
```
2- use uv to install the needed libraries
```bash
uv pip install -r requirements.txt
```
3- if uv is not installed, use `venv` and `pip` to create a virtual environment and install the requirements.

### Why uv
#### Performance Comparison

For a typical research stack (e.g., `fastapi`, `numpy`, `pandas`, `owlready2`, `torch`), `uv` will usually resolve and install the `requirements.txt` in a fraction of the time:

|**Task**|**pip (standard)**|**uv (cached)**|
|---|---|---|
|**Resolution**|~5–15 seconds|**< 0.1 seconds**|
|**Installation**|~30–60 seconds|**~1–2 seconds**|

#### For macOS and Linux

Open your terminal and run:

Bash

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### For Windows

Run the following in PowerShell:

PowerShell

```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Initial Configuration

Once installed, you should verify the installation by checking the version:

Bash

```
uv --version
```

#### Updating `uv`

One of the advantages of the standalone installation is the built-in self-update mechanism:

Bash

```Bash
uv self update
```

---

#### Quick Start for Research Workflows

Here is the "cheat sheet" for using `uv` effectively:

| **Task**                         | **Command**                                         |
| -------------------------------- | --------------------------------------------------- |
| **Create a virtual environment** | `uv venv`                                           |
| **Activate environment**         | `source .venv/bin/activate`                         |
| **Install a package**            | `uv pip install <package_name>`                     |
| **Sync from requirements.txt**   | `uv pip sync requirements.txt`                      |
| **Compile a lockfile**           | `uv pip compile pyproject.toml -o requirements.txt` |
