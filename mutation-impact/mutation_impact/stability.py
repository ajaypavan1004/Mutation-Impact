import pandas as pd


def compute_stability_score(feature_df):
    df = feature_df.copy()

    # Normalize volume impact (large steric shifts matter more if buried)
    df["volume_impact"] = abs(df["volume_delta"]) / 100.0

    # Hydrophobic mismatch magnitude
    df["hydro_impact"] = abs(df["hydrophobicity_delta"]) / 5.0

    # Conservation impact (invert entropy: low entropy = high conservation)
    max_entropy = df["entropy"].max() if df["entropy"].max() > 0 else 1
    df["conservation_score"] = 1 - (df["entropy"] / max_entropy)

    # Core stability heuristic
    df["stability_score"] = (
        2 * df["buried_flag"]
        + df["volume_impact"]
        + df["hydro_impact"]
        + df["conservation_score"]
    )

    # Classification
    df["stability_class"] = pd.cut(
        df["stability_score"],
        bins=[-1, 1.5, 3, 10],
        labels=["Low impact", "Moderate impact", "High impact"]
    )

    return df
