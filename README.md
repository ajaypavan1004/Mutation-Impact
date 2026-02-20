# Mutation Impact  
**Structure & Conservation-Aware Mutation Feature Extraction**

Mutation Impact is a command-line tool for analysing protein mutations in structural and evolutionary context.

It generates:

- Structure-derived features (secondary structure, solvent accessibility, burial)
- Conservation metrics from multiple sequence alignment
- Physicochemical mutation descriptors
- A baseline structural stability risk index
- An ML-ready mutation feature matrix

Designed for:

- Wet lab scientists who want quick structural insight into mutations  
- Computational researchers who need structured mutation features for downstream modeling  

---

## 🔬 What This Tool Does

Given:

- A protein FASTA sequence  
- A mutation list (`position, wt, mut`)  
- A structure file (`.pdb` or `.cif`)  
- A homolog FASTA file  

The tool produces:

### 1️⃣ Human-Readable Mutation Analysis  
`final_mutation_analysis.csv`

Includes:

- Secondary structure  
- Relative solvent accessibility  
- Buried flag  
- Conservation score  
- Physicochemical change metrics  
- Stability risk index (baseline heuristic)  
- Stability classification  

---

### 2️⃣ ML-Ready Feature Matrix  
`mutation_feature_matrix.csv`

Includes:

- Numeric structural features  
- Conservation metrics  
- Chemistry deltas  

Does **not** include heuristic stability scoring.

This file is suitable for training regression or classification models.

---

## 📂 Project Structure

```
mutation-impact/
│
├── main.py
├── environment.yml
├── mutation_impact/
│   ├── features.py
│   ├── structure.py
│   ├── conservation.py
│   ├── chemistry.py
│   └── ...
│
├── example/
│   ├── tp53.fasta
│   ├── tp53_homologs.fasta
│   ├── 2OCJ.cif
│   ├── tp53_mutations.csv
│   └── results/
│
└── README.md
```

---

## 🚀 Installation (Conda)

Create environment:

```bash
conda env create -f environment.yml
conda activate mutation-impact
```

Dependencies include:

- Python  
- Biopython  
- MAFFT  
- DSSP (mkdssp)  
- NumPy  
- Pandas  

---

## ▶️ Usage

```bash
python main.py \
  --fasta example/tp53.fasta \
  --mutations example/tp53_mutations.csv \
  --structure example/2OCJ.cif \
  --chain A \
  --homologs example/tp53_homologs.fasta \
  --output example/results
```

Output directory:

```
example/results/
├── mutation_feature_matrix.csv
└── final_mutation_analysis.csv
```

---

## 🧠 Stability Risk Index

The stability risk index integrates:

- Residue burial  
- Conservation  
- Volume change  
- Hydrophobicity change  

It is a **baseline heuristic**, not a trained ΔΔG predictor.

For rigorous thermodynamic predictions, dedicated energy-based tools or experimental measurements are recommended.

---

## 🤖 Using for Machine Learning

The file `mutation_feature_matrix.csv` can be used directly as input to ML models.

Example workflow:

1. Generate mutation features  
2. Merge with experimental labels (e.g., ΔΔG, pathogenicity)  
3. Train regression or classification models  

Example (scikit-learn):

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("mutation_feature_matrix.csv")

X = df.drop(columns=["experimental_ddg"])
y = df["experimental_ddg"]

model = RandomForestRegressor()
model.fit(X, y)
```

Feature extraction is deterministic and reproducible.

---

## 🧪 Example Validation

Validated on hotspot mutations in the TP53 DNA-binding domain.

Structural destabilizing mutations are identified as high structural risk, while DNA-contact mutations are differentiated appropriately.

---

## 📄 License

MIT License
