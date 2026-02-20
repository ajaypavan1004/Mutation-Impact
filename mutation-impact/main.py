import os
import argparse

from mutation_impact.io_utils import load_fasta, load_mutations
from mutation_impact.features import generate_feature_matrix


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Mutation Impact: Structure & Conservation-Aware Feature Extraction"
    )

    parser.add_argument(
        "--fasta",
        required=True,
        help="Path to protein FASTA file"
    )

    parser.add_argument(
        "--mutations",
        required=True,
        help="CSV file containing mutations (position, wt, mut)"
    )

    parser.add_argument(
        "--structure",
        required=True,
        help="Path to structure file (.pdb or .cif)"
    )

    parser.add_argument(
        "--chain",
        required=True,
        help="Chain ID (e.g., A)"
    )

    parser.add_argument(
        "--homologs",
        required=True,
        help="FASTA file of homologous sequences for conservation analysis"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output directory"
    )

    return parser.parse_args()


def validate_inputs(args):
    if not os.path.exists(args.fasta):
        raise FileNotFoundError(f"FASTA file not found: {args.fasta}")

    if not os.path.exists(args.mutations):
        raise FileNotFoundError(f"Mutation file not found: {args.mutations}")

    if not os.path.exists(args.structure):
        raise FileNotFoundError(f"Structure file not found: {args.structure}")

    if not os.path.exists(args.homologs):
        raise FileNotFoundError(f"Homolog FASTA file not found: {args.homologs}")

    os.makedirs(args.output, exist_ok=True)


def main():
    args = parse_arguments()
    validate_inputs(args)

    print("Loading sequence...")
    sequence = load_fasta(args.fasta)

    print("Loading mutations...")
    mutations = load_mutations(args.mutations)

    print("Generating mutation feature matrix...")
    feature_matrix = generate_feature_matrix(
        fasta_path=args.fasta,
        sequence=sequence,
        mutations=mutations,
        structure_path=args.structure,
        chain=args.chain,
        homologs_path=args.homologs,
        output_dir=args.output
    )

    output_path = os.path.join(args.output, "final_mutation_analysis.csv")

    feature_matrix.to_csv(output_path, index=False)

    print(f"Full mutation analysis results saved to: {output_path}")


    ml_feature_matrix = feature_matrix.copy()
    # Remove heuristic columns if present
    ml_feature_matrix = feature_matrix.copy()
    for col in ["stability_risk_index", "stability_class"]:
        if col in ml_feature_matrix.columns:
            ml_feature_matrix = ml_feature_matrix.drop(columns=[col])

    ml_output_path = os.path.join(args.output, "mutation_feature_matrix.csv")
    ml_feature_matrix.to_csv(ml_output_path, index=False)

    print(f"Feature matrix for ML training is saved to: {ml_output_path}")





if __name__ == "__main__":
    main()
