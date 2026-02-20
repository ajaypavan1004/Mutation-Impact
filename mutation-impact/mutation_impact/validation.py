VALID_AA = set("ACDEFGHIKLMNPQRSTVWY")


def validate_mutations(sequence, df):
    seq_len = len(sequence)

    validated_rows = []

    for _, row in df.iterrows():
        pos = int(row["position"])
        wt = str(row["wt"]).upper()
        mut = str(row["mut"]).upper()

        if pos < 1 or pos > seq_len:
            raise ValueError(f"Position {pos} out of range.")

        if wt not in VALID_AA or mut not in VALID_AA:
            raise ValueError(f"Invalid amino acid at position {pos}.")

        if sequence[pos - 1] != wt:
            raise ValueError(
                f"WT mismatch at position {pos}: "
                f"Expected {sequence[pos - 1]}, got {wt}"
            )

        if wt == mut:
            raise ValueError(f"WT and MUT are identical at position {pos}.")

        validated_rows.append({
            "position": pos,
            "wt": wt,
            "mut": mut
        })

    import pandas as pd
    return pd.DataFrame(validated_rows)
