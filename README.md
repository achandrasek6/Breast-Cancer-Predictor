# Breast-Cancer-Predictor

*ML pipeline that predicts tumor presence in scRNA-seq breast tissue samples (tumor vs. adjacent normal).*

![Accuracy 0.889](https://img.shields.io/badge/Accuracy-0.889-blue) ![ROC AUC 0.775](https://img.shields.io/badge/ROC%20AUC-0.775-blue) ![CV LOO-CV](https://img.shields.io/badge/CV-LOO--CV-green) ![Languages](https://img.shields.io/badge/Languages-R%20%7C%20Python-orange)

## Results at a glance

* **What I built:** a small-cohort, reproducible pipeline that cleans RNA-seq counts (R), then trains and evaluates a **Random Forest** classifier with **strict Leave-One-Out CV (LOO-CV)** in Python.
* **Dataset:** 9 paired tumor/adjacent normal samples from GEO **GSE267505** (subset selected for quality/metadata completeness).
* **Held-out performance (LOO-CV):** **Accuracy = 0.889**, **ROC AUC = 0.775**; **1 misclassified** sample across 9 folds (details in report).
* **Compact features:** within each fold, univariate **ANOVA F-test selects the top 10 genes** after log-transform, scaling, and low-variance filtering—keeps the model simple and interpretable.

> **Why it matters:** Small clinical cohorts are common. This repo shows how to get **credible estimates** from limited data with rigorous cross-validation and fold-internal feature selection (no leakage), while keeping a **parsimonious gene panel** that’s easier to inspect and validate biologically.

---

## Repository structure

```
Breast-Cancer-Predictor/
├── Breast_Cancer_Project/
│   ├── GEO Accession viewer.html                # reference page for the original study
│   ├── GEO Accession viewer_files/              # page assets
│   ├── GSE267505_RawCountFile_rsemgenes.txt     # raw counts (subset used in this study)
│   ├── data_cleaning.R                          # R: import → reshape → annotate → export
│   ├── cleaned_data.txt                         # output from R; input to Python
│   └── Machine_Learning.py                      # Python: pipeline + LOO-CV + ROC plot
└── README.md
```

---

## How it works (pipeline)

**R (preprocessing)**

1. Import raw RSEM counts → clean column/sample names
2. Transpose to **samples × genes**
3. Join sample labels (**Normal/Tumor**)
4. Simplify gene labels; integrity checks
5. Write `cleaned_data.txt` (TSV)

**Python (modeling)**

1. Load `cleaned_data.txt`; map labels to {0,1}
2. **log1p** transform → **StandardScaler**
3. **VarianceThreshold** to drop near-constant genes
4. **SelectKBest(ANOVA F-test, k=10)** *inside each fold*
5. **RandomForestClassifier(n\_estimators=50)**
6. **LOO-CV**: per-fold predictions, accuracy, **ROC AUC**, misclassified IDs; **ROC plot** saved/shown

*All steps are encapsulated in a scikit-learn `Pipeline` so the held-out sample only sees transforms fit on the training fold.*

---

## Quickstart

### 1) Set up environments

**R (≥ 4.0)**

```r
install.packages("tidyverse")
```

**Python (3.8+)**

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy pandas scikit-learn matplotlib
```

### 2) Preprocess counts (R)

* Open `Breast_Cancer_Project/data_cleaning.R`
* Point it at `GSE267505_RawCountFile_rsemgenes.txt`
* Run; it writes `Breast_Cancer_Project/cleaned_data.txt`

> Tip: A `cleaned_data.txt` is already included; you can **overwrite**, **rename**, or **skip** the R step and continue with Python.

### 3) Train & evaluate (Python)

```bash
cd Breast_Cancer_Project
python3 Machine_Learning.py
```

* Console prints **LOO-CV accuracy**, per-fold outcomes, misclassified IDs, and **ROC AUC**.
* A **ROC curve** is displayed; flip the “save” line in the script to output `roc.png`.

---

## Reproducible results (what to expect)

* LOO-CV on the 9-pair subset: **Accuracy ≈ 0.889**, **AUC ≈ 0.775**, with **one** misclassification.
* The ROC curve shows performance substantially better than random (AUC 0.5) while highlighting typical trade-offs in sensitivity/specificity at small N.
* A handful of genes repeatedly appear among the **top-10** fold-selected features—useful candidates for biological follow-up.

<img width="875" height="875" alt="image" src="https://github.com/user-attachments/assets/0e0fa288-ca5b-4acd-ab39-04a062c28eec" />


---

## Notes & gotchas

* **No leakage:** Feature selection and scaling are fit **inside** each training fold; the held-out sample is unseen until prediction.
* **Warnings about zero variance** can be ignored—those genes are filtered out before selection.
* **LOO-CV** can have high-variance metrics with tiny cohorts; for publication-grade claims, use a larger independent validation set.

---

## Extend the project

* **Try more features:** set `k` in `SelectKBest` to 20–50 and compare stability/accuracy.
* **Tune the forest:** vary trees (e.g., 50–200), depth, and `max_features` with nested CV.
* **Alternative models:** logistic regression with elastic-net, gradient boosting, or SVM.
* **Biology:** run GSEA on frequently selected genes to connect to pathways.
* **Packaging:** wrap the Python pipeline in a CLI (`argparse`) and emit a JSON report.

---

## References / Acknowledgments

* scikit-learn, NumPy, pandas, Matplotlib for Python; tidyverse for R.

---

### Changelog

* **v1.0:** Initial release with R preprocessing + Python LOO-CV pipeline; ROC plot; report-aligned results.
