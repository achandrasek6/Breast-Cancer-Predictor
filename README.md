# breast-tumor-predictor
_ML model that predicts tumor presence in scRNA seq breast tissue samples_

This repository contains two analysis scripts for a small breast cancer study:

1. **R Script** (`data_preprocessing.R`)  
   - Imports raw gene-count data.  
   - Cleans and reshapes the table so that each row is a sample and each column a gene.  
   - Annotates each sample as “Normal” or “Tumor.”  
   - Writes out `cleaned_data.txt` for modeling.

2. **Python Script** (`Machine_Learning.py`)  
   - Reads the cleaned count table.  
   - Applies log-plus-one transformation, feature scaling, variance filtering, and ANOVA-based feature selection.  
   - Trains and evaluates a Random Forest under Leave-One-Out CV.  
   - Reports accuracy, misclassified samples, and ROC AUC.  
   - Generates and displays (or saves) an ROC curve.

---

## Repository Structure

├── GEO Accession viewer.html # link to original study
├── GEO Accession viewer_files # full file contents from the study
├── GSE267505_RawCountFile_rsemgenes.txt # scRNA protein dataset used in inital study
├── data_cleaning.R # R script for data cleaning/prep
├── .Rhistory # R history file
├── cleaned_data.txt # Output of the R script (input for Python)
├── Machine_Learning.py # Python modeling & evaluation
└── README.md # This file

---

## Prerequisites

- **R (≥ 4.0)** with:
  - tidyverse

- **Python 3.8+** with:
  - numpy  
  - pandas  
  - scikit-learn  
  - matplotlib  

---

## Installation

1. **R dependencies**
   # install within R gui
   install.packages("tidyverse")

2. **Python dependecies**
   # bash shell script **must install in same directory as project**
   python3 -m venv venv
   source venv/bin/activate
   pip install numpy pandas scikit-learn matplotlib

---

## Usage
  # Preprocess the raw counts (R)
    Edit data_cleaning.R to point to your output directory for cleaned_data.txt.
  **Run R in gui (preferably rStudio) with tidyverse installed.**
    Choose GSE267505_RawCountFile_rsemgenes.txt raw data file when prompted.
  **cleaned_data.txt already exists in this directory; you will need to overwrite/rename this file or skip running R script all together and start with next step**
# Run ML script
  **To run in unix shell:**
    Change directory to project directory.
    Execute python3 Machine_Learning.py
  **May alternatively be run directly from a python gui***

## Outputs
**Console**
    1. LOO-CV accuracy and standard deviation
    2. Per-split accuracies
    3. Misclassified sample(s)
    4. ROC AUC
**Plot**
    1. ROC curve graphic (shown interactively)

---

## Notes
    1. No additional configuration files are required.








   
