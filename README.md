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