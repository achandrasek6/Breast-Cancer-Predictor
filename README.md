# breast-tumor-predictor
_ML model that predicts tumor presence in scRNA seq breast tissue samples._

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

├── GEO Accession viewer_files # full file contents required to upload original study webpage

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
   *(install with R gui)*
   
         install.packages("tidyverse")

3. **Python dependecies**
   *(must install in same directory as project)*
   
   *bash*
   
       python3 -m venv venv
       source venv/bin/activate
       pip install numpy pandas scikit-learn matplotlib

---

## Usage
# Preprocess the raw counts (R)
   1. Edit data_cleaning.R to point to your output directory for cleaned_data.txt.
   2. Run R in gui (preferably rStudio) with tidyverse installed.
   3. Choose `GSE267505_RawCountFile_rsemgenes.txt` raw data file when prompted.

*Additional info:* 
- `cleaned_data.txt` already exists in this directory 
- User will need to either:
   - Overwrite this file
   - Rename this file
   - Skip running R script all together and begin with next step
# Run ML script (python/shell)
  **To run in unix shell:**
  
   1. Change directory to project directory.
   2. Execute `python3 Machine_Learning.py`
      
  *Additional info:* 
- Script may alternatively be run directly from a python gui.
- If user prefers to save output image instead of viewing interactive graph, final line of section 6 in the python script should be activated *(currently commented out)*, and the penultimate line should be commented out *(currently active)*.

---

## Outputs
**Console**
- LOO-CV accuracy and standard deviation
- Per-split accuracies
- Misclassified sample(s)
- ROC AUC

**Plot**
- ROC curve graphic (shown interactively or saved as as roc.png)

---

## Notes
- No additional configuration files are required.








   
