import os
import pandas as pd
from Bio import SeqIO


def load_fasta(fasta_path):
    records = list(SeqIO.parse(fasta_path, "fasta"))

    if len(records) != 1:
        raise ValueError("FASTA must contain exactly one sequence.")

    return str(records[0].seq).upper()


def load_mutations(mutation_path):
    df = pd.read_csv(mutation_path)

    required_cols = {"position", "wt", "mut"}
    if not required_cols.issubset(df.columns):
        raise ValueError("Mutation CSV must contain columns: position, wt, mut")

    return df


def write_validated(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "validated_mutations.csv")
    df.to_csv(output_path, index=False)
