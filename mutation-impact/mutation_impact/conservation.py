import subprocess
import math
from collections import Counter
from Bio import SeqIO
import pandas as pd
import os


def run_mafft(input_fasta, output_fasta):
    command = ["mafft", "--auto", input_fasta]

    with open(output_fasta, "w") as outfile:
        subprocess.run(command, stdout=outfile, check=True)


def calculate_entropy(column):
    counts = Counter(column)
    total = sum(counts.values())

    entropy = 0.0
    for aa, count in counts.items():
        if aa == "-":
            continue
        p = count / total
        entropy -= p * math.log2(p)
        #lol just used Shannon entropy formula here
    return entropy


def extract_conservation_features(fasta_path, homologs_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    combined_fasta = os.path.join(output_dir, "combined.fasta")
    aligned_fasta = os.path.join(output_dir, "aligned.fasta")

    # Combine target + homologs
    with open(combined_fasta, "w") as outfile:
        for record in SeqIO.parse(fasta_path, "fasta"):
            SeqIO.write(record, outfile, "fasta")
        for record in SeqIO.parse(homologs_path, "fasta"):
            SeqIO.write(record, outfile, "fasta")

    # Run MAFFT
    run_mafft(combined_fasta, aligned_fasta)

    # Read alignment
    alignment = list(SeqIO.parse(aligned_fasta, "fasta"))

    target_seq = alignment[0].seq

    features = []
    fasta_index = 0

    for i in range(len(target_seq)):
        if target_seq[i] == "-":
            continue

        column = [record.seq[i] for record in alignment]
        entropy = calculate_entropy(column)

        fasta_index += 1

        features.append({
            "position": fasta_index,
            "entropy": entropy
        })

    return pd.DataFrame(features)
