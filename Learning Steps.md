# Learning Steps

## A- Preliminaries

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

## B- Target of the Workshop
1- Publish a distribution of two datasets:
- Measured active power photovoltaic on the top roof of IAI, after aggregation
- The content of this training material for future reference.

2- Define a Workflow for future publications, where our understanding of the FAIR-principles is implemented.

*Discuss and elaborate those targets to define an action list*

| **Task**                                            | **Responsable** |
|-----------------------------------------------------|-----------------|
| Which different type of data can be generated       | All             |
| Describe the plan phase of an experiment            | Anis            |
| Decide which tool should be used for the plan phase | Nan             |
| etc.                                                | All             |



## C- Visualise the Workflow
- mermaid is a modern language to describe graphs within mark-down files.
- here is an example of a generic workflow
- another way to represent workflows, more professional is BPMN (try https://bpmn.io and https://www.omg.org/spec/BPMN/2.0/)

```mermaid
---
config:
  layout: elk
  theme: base
  themeVariables:
    primaryColor: "#778899"
    edgeLabelBackground: "#ffffff"
---
flowchart TD
    Start(( )) --> Plan[Plan data collection & publication<br/><i>Tools, Guidelines, Schemas, Platforms, etc.</i>]
    
    Plan --> Collect[Collect raw data<br/><i>Through research operations</i>]
    
    Collect --> Clean[Initial Data Cleansing/Preprocessing<br/><i>Generate the scaffold, i.e. RO-Crate</i>]

    %% Parallel Annotation Setup
    Clean --> Split1{ }
    Split1 --> Task[Assign Annotation Tasks]
    Split1 --> Env[Setup Annotation Environment]
    
    Task --> Join1{ }
    Env --> Join1
    
    Join1 --> Annotate[Annotate Data<br/><i>Human or Semi-Automated</i>]
    
    Annotate --> QA[Quality Assurance - QA]
    
    QA --> Doc[Generate Data Documentation<br/><i>Metadata, README</i>]

    %% Sensitivity Logic
    Doc --> Sensitive{Data Sensitive?}
    
    Sensitive -- Yes --> Anon[Anonymize / De-identify Data]
    Anon --> Restrict[Select Restricted Access Repository]
    
    Sensitive -- No --> Public[Select Public Repository]
    
    Restrict --> Submit[Submit Dataset to Repository]
    Public --> Submit

    %% Parallel Repository Actions
    Submit --> Fork1{ }
    Fork1 --> Review[Repository performs<br/>Curation & Review]
    Fork1 --> DOI[Acquire Persistent<br/>Identifier - DOI]
    
    Review --> Join2{ }
    DOI --> Join2
    
    Join2 --> Final[Final Publication of<br/>Dataset & Metadata]
    Final --> Stop((( )))

    %% Styling for Research Paper Aesthetic
    style Plan fill:#f9f9f9,stroke:#778899,stroke-width:2px
    style Clean fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Final fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style Sensitive fill:#ececff,stroke:#9370db