# Insurance-Risk-Analysis

## 📖 Project Overview
AlphaCare Insurance Solutions (ACIS) is focused on utilizing data analytics to optimize marketing strategies and identify "low-risk" targets for car insurance in South Africa. 

This project involves building a robust data engineering and analytics pipeline to analyze historical insurance claim data (Feb 2014 - Aug 2015). The goal is to provide actionable insights that allow for reduced premiums for low-risk clients and targeted marketing strategies.

---

## 📂 Project Structure
The project adheres to Object-Oriented Programming (OOP) principles and is structured as a modular Python package.

```text
AlphaCare_Analytics/
├── data/                
│   ├── raw/             # Original dataset (Not synced to Git)
│   └── processed/       # Cleaned/Transformed data
├── notebooks/           # Jupyter Notebooks for EDA & Prototyping
├── src/                 # Source code for the analysis package
│   ├── __init__.py
│   ├── loader.py        # Data Ingestion Logic
│   └── analysis.py      # Statistical Analysis & Visualization
├── .gitignore           # Git ignore rules
├── README.md            # Project Documentation
└── requirements.txt     # Python Dependencies
```
## Setup and Installation
Follow these steps to set up the development environment.
1. Prerequisites
Python 3.8 or higher
Git
2. Clone the Repository
code
```Bash
git clone https://github.com/binia01/Insurance-Risk-Analysis.git
cd Insurance-Risk-Analysis
```
3. Create a Virtual Environment
- It is recommended to use a virtual environment to manage dependencies.
- Using venv:
code
```Bash
# Create environment
python -m venv .venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate
```
4. Install Dependencies
code
```Bash
pip install -r requirements.txt
```

## DVC Setup (Data Version Control)

Add the following instructions to manage large data and model artifacts with DVC.

### Prerequisites
- DVC (pip or apt/brew)
- Remote storage (S3, GCS, Google Drive, SSH, Azure, etc.)
- Credentials configured for chosen remote (AWS CLI, gcloud, SSH keys, etc.)

### Install DVC
```bash
pip install dvc
```

### Initialize DVC in repo
```bash
# run once at project root
dvc init
git add .dvc .dvcignore
git commit -m "chore: initialize dvc"
```

### Configure a remote storage
Pick one and set it as default (-d).

- S3 example:
```bash
dvc remote add -d storage s3://my-bucket/path/to/project
# prefer using AWS credentials via env/AWS config
dvc remote modify storage region us-east-1
```

- Google Drive (requires setting up dvc with gdrive support):
```bash
dvc remote add -d storage gdrive://<folder-id>
# follow dvc prompts to authorize
```

- SSH example:
```bash
dvc remote add -d storage ssh://user@host:/path/to/storage
# ensure ssh keys and permissions are set
```

### Track raw data / large files
Do not commit raw large files to Git. Use dvc to track them instead.

```bash
# add a dataset (example)
dvc add data/raw/claims.csv

# this creates data/raw/claims.csv.dvc and moves the large file under .dvc/cache
git add data/raw/claims.csv.dvc
git commit -m "feat: track raw claims dataset with dvc"
```

### Push and pull data from remote
```bash
# upload local tracked files to remote
dvc push


