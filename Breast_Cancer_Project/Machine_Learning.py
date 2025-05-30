#!/usr/bin/env python3
"""
Machine_Learning.py

Loads cleaned scRNA dataset, preprocesses, and runs Leave-One-Out CV
with a Random Forest pipeline (scaling → variance threshold → univariate
feature selection → classifier). Reports accuracy, per-split results,
misclassified samples, and plots the ROC curve.
"""

import warnings
# Silence every warning emitted by Python or third-party libraries
warnings.filterwarnings("ignore")

import numpy as np
# Silence numpy floating-point warnings (divide/invalid)
np.seterr(divide='ignore', invalid='ignore')

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import LeaveOneOut, cross_val_score, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, roc_curve

def main():
    # 1) Load & preprocess
    df = pd.read_csv("cleaned_data.txt", sep="\t")
    df['tumor_status'] = df['tumor_status'].map({'Normal': 0, 'Tumor': 1})

    X = df.drop(['sample_name', 'tumor_status'], axis=1)
    y = df['tumor_status']

    # drop any feature that is constant across all samples
    X = X.loc[:, X.var(axis=0) > 0]

    # stabilize variance
    X = np.log1p(X)

    # 2) Build pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('var', VarianceThreshold(threshold=0.01)),
        ('select', SelectKBest(f_classif, k=10)),
        ('clf', RandomForestClassifier(n_estimators=50, random_state=42)),
    ])

    # 3) Leave-One-Out CV
    loo = LeaveOneOut()
    scores = cross_val_score(pipeline, X, y, cv=loo, scoring='accuracy', n_jobs=-1)
    print(f"LOO CV accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
    print("Per-split accuracies:", scores)

    # 4) Identify misclassified samples
    preds = cross_val_predict(pipeline, X, y, cv=loo, method='predict')
    mis = pd.DataFrame({
        'sample_name': df['sample_name'],
        'true_label': y,
        'predicted': preds
    })
    mis = mis[mis['true_label'] != mis['predicted']]
    if not mis.empty:
        print("\nMisclassified sample(s):")
        print(mis.to_string(index=False))
    else:
        print("\nNo misclassifications under LOO CV.")

    # 5) Compute LOO AUC
    probas = cross_val_predict(pipeline, X, y, cv=loo, method='predict_proba')[:, 1]
    auc = roc_auc_score(y, probas)
    print(f"\nLOO CV ROC AUC: {auc:.3f}")

    # 6) Plot ROC curve
    fpr, tpr, thresholds = roc_curve(y, probas)
    plt.figure(figsize=(6,6))
    plt.plot(fpr, tpr, lw=2, label=f'ROC curve (AUC = {auc:.3f})')
    plt.plot([0, 1], [0, 1], linestyle='--', lw=1, color='grey', label='Chance')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Leave-One-Out CV ROC Curve')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.tight_layout()
    # either show or save to file:
    plt.show()
    # plt.savefig('roc_curve.png', dpi=150)

if __name__ == "__main__":
    main()






