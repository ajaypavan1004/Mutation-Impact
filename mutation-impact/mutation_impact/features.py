from mutation_impact.structure import extract_structure_features
from mutation_impact.conservation import extract_conservation_features
from mutation_impact.mutation_features import compute_mutation_features
from mutation_impact.validation import validate_mutations
from mutation_impact.stability import compute_stability_score


def generate_feature_matrix(
    fasta_path,
    sequence,
    mutations,
    structure_path,
    chain,
    homologs_path,
    output_dir
):
    # Validate mutations
    validated = validate_mutations(sequence, mutations)

    # Structure features
    structure_features = extract_structure_features(structure_path,chain,sequence)

    # Conservation features
    conservation_features = extract_conservation_features(fasta_path,homologs_path,output_dir)

    # Chemistry features
    mutation_features = compute_mutation_features(validated)

    # Merge base features
    feature_matrix = validated.merge(
        structure_features,
        on="position",
        how="left"
    ).merge(
        conservation_features,
        on="position",
        how="left"
    ).merge(
        mutation_features,
        on=["position", "wt", "mut"],
        how="left"
    )

    # Stability scoring
    feature_matrix = compute_stability_score(feature_matrix)

    return feature_matrix
