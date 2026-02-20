import pandas as pd


def build_feature_matrix(mutations_df, structure_df, conservation_df):
    # Merge structure + conservation on position
    position_features = structure_df.merge(
        conservation_df,
        on="position",
        how="inner"
    )

    # Merge with mutations
    feature_matrix = mutations_df.merge(
        position_features,
        on="position",
        how="left"
    )

    return feature_matrix
