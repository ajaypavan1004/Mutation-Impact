import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Mutation Impact Framework"
    )

    parser.add_argument("--fasta", required=True, help="Protein FASTA file")
    parser.add_argument("--mutations", required=True, help="Mutation CSV file")
    parser.add_argument("--structure", required=True, help="Protein structure PDB file")
    parser.add_argument("--chain", required=True, help="Target chain ID")
    parser.add_argument("--homologs", required=True, help="Homolog FASTA file")
    parser.add_argument("--output", required=True, help="Output directory")

    return parser.parse_args()
