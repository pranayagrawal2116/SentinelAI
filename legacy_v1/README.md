# Hybrid Feature Selection and Ensemble Machine Learning for Multi-Class IoT Intrusion Detection

This project implements an intelligent Machine Learning pipeline for detecting and classifying cyberattacks in IoT network traffic (e.g., CICIoT2023 dataset). 

The project is entirely coded in Python and divided into **3 distinct Machine Learning modules**, designed specifically for a 3-person student group presentation.

## Installation & Setup

1. Make sure you have Python 3.8+ installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main pipeline:
   ```bash
   python main.py
   ```
   *Note: The code uses a synthetic dataset generator that perfectly mimics the shape and properties of the CICIoT2023 dataset so you can run and present the code immediately without needing to download and process a 30GB+ CSV file. To use a real dataset, modify `use_synthetic=False` in `main.py`.*

---

## Mini-Project Presentation Guide (For 3 Students)

This project has been explicitly designed so that each student can take ownership of a critical, complex part of the Machine Learning pipeline. There is no "frontend/backend" here; this is a pure Data Science / ML Engineering project.

### 👩‍💻 Student 1: Module 1 - Data Engineering & Preprocessing
**File:** `src/module1_preprocessing.py`

**Your Presentation Focus:**
1. **The Dataset (CICIoT2023):** Explain that IoT environments generate massive amounts of network traffic, making it hard to identify attacks like DDoS, Reconnaissance, or Brute Force.
2. **Data Cleaning & Encoding:** Explain how you loaded the data, handled missing/duplicate values, and used `LabelEncoder` to convert attack categories into numerical targets.
3. **Preventing Data Leakage:** Highlight that you performed the Train-Test Split *before* scaling and resampling to ensure the model doesn't "cheat" by seeing test data during training.
4. **Addressing Class Imbalance:** Cyberattack data is notoriously imbalanced (lots of benign traffic, few attacks). Explain your use of **SMOTE (Synthetic Minority Over-sampling Technique)** to synthetically balance the training data, allowing the models to learn rare attacks without being biased.

### 🧑‍💻 Student 2: Module 2 - Hybrid Feature Selection
**File:** `src/module2_feature_selection.py`

**Your Presentation Focus:**
1. **The Dimensionality Problem:** Explain that IoT datasets have dozens or hundreds of features, many of which are redundant or noisy, which slows down models and reduces accuracy.
2. **The Hybrid Approach:** You didn't just rely on one method. You combined three complementary feature selection strategies:
   * **Filter Method (ANOVA/SelectKBest):** Evaluated statistical relevance between each feature and the target.
   * **Wrapper Method (Recursive Feature Elimination):** Iteratively trained a Decision Tree, dropping the weakest features.
   * **Embedded Method (Random Forest Importance):** Used the internal node-impurity splits of a Random Forest to rank features.
3. **The Consensus Voting System:** Explain your algorithm that tallies "votes" from all three methods. A feature was only selected for the final dataset if it was identified as important by at least 2 out of the 3 methods. This guarantees a highly robust subset of network features.

### 👨‍💻 Student 3: Module 3 - Model Training, Ensemble Learning & Evaluation
**File:** `src/module3_modeling_evaluation.py`

**Your Presentation Focus:**
1. **The Base Models:** Explain that you trained several state-of-the-art algorithms: Random Forest, XGBoost, LightGBM, and an SVM (Support Vector Machine) as a baseline.
2. **The Ensemble Architecture:** Explain the concept of **Ensemble Learning (Soft Voting)**. Instead of relying on a single model, you combined RF, XGBoost, and LightGBM. The models average out their probability predictions, meaning the ensemble leverages the strengths of all three to make a more accurate and robust final decision.
3. **Experimental Results:** Present the final output (printed in the terminal). Compare "Experiment 1" (using all features) vs "Experiment 2" (using the features selected by Student 2).
4. **Evaluation Metrics:** Discuss why you used F1-score and Precision/Recall alongside Accuracy. Show how the Hybrid Feature Selection reduced training time significantly while maintaining (or even improving) the F1-score and Accuracy.
