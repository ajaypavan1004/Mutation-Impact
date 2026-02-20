import pandas as pd


# Basic physicochemical properties
CHARGE = {
    "D": -1, "E": -1,
    "K": +1, "R": +1,
    "H": +0.5  # approximate partial positive
}

HYDROPHOBICITY = {
    "A": 1.8, "C": 2.5, "D": -3.5, "E": -3.5,
    "F": 2.8, "G": -0.4, "H": -3.2, "I": 4.5,
    "K": -3.9, "L": 3.8, "M": 1.9, "N": -3.5,
    "P": -1.6, "Q": -3.5, "R": -4.5, "S": -0.8,
    "T": -0.7, "V": 4.2, "W": -0.9, "Y": -1.3
}
#i pulled the values from kyte-doolittle scale
VOLUME = {
    "A": 88.6, "C": 108.5, "D": 111.1, "E": 138.4,
    "F": 189.9, "G": 60.1, "H": 153.2, "I": 166.7,
    "K": 168.6, "L": 166.7, "M": 162.9, "N": 114.1,
    "P": 112.7, "Q": 143.8, "R": 173.4, "S": 89.0,
    "T": 116.1, "V": 140.0, "W": 227.8, "Y": 193.6
}

POLAR = {"D", "E", "K", "R", "H", "N", "Q", "S", "T", "Y"}


def compute_mutation_features(mutations_df):
    rows = []

    for _, row in mutations_df.iterrows():
        wt = row["wt"]
        mut = row["mut"]

        wt_charge = CHARGE.get(wt, 0)
        mut_charge = CHARGE.get(mut, 0)

        charge_change = mut_charge - wt_charge

        hydro_delta = HYDROPHOBICITY[mut] - HYDROPHOBICITY[wt]
        volume_delta = VOLUME[mut] - VOLUME[wt]

        polarity_change = int((wt in POLAR) != (mut in POLAR))

        rows.append({
            "position": row["position"],
            "wt": wt,
            "mut": mut,
            "charge_change": charge_change,
            "hydrophobicity_delta": hydro_delta,
            "volume_delta": volume_delta,
            "polarity_change_flag": polarity_change
        })

    return pd.DataFrame(rows)
