from Bio.PDB import PDBParser, MMCIFParser, DSSP
from Bio import pairwise2
from Bio.Seq import Seq
import pandas as pd
from Bio.Data.IUPACData import protein_letters_3to1


def extract_chain_sequence(chain):
    sequence = ""
    residue_ids = []

    for residue in chain:
        if residue.id[0] != " ":
            continue  # skip heteroatoms

        resname = residue.resname.capitalize()
        if resname not in protein_letters_3to1:
            continue  # skip non-standard residues

        aa = protein_letters_3to1[resname]

        sequence += aa
        residue_ids.append(residue.id)

    return sequence, residue_ids



def build_pdb_to_fasta_mapping(pdb_seq, fasta_seq, residue_ids):
    alignment = pairwise2.align.globalxx(pdb_seq, fasta_seq)[0]

    pdb_aligned = alignment.seqA
    fasta_aligned = alignment.seqB

    mapping = {}
    pdb_index = 0
    fasta_index = 0

    for i in range(len(pdb_aligned)):
        pdb_char = pdb_aligned[i]
        fasta_char = fasta_aligned[i]

        if pdb_char != "-":
            current_residue_id = residue_ids[pdb_index]

        if pdb_char != "-" and fasta_char != "-":
            mapping[current_residue_id] = fasta_index + 1

        if pdb_char != "-":
            pdb_index += 1

        if fasta_char != "-":
            fasta_index += 1

    return mapping


def extract_structure_features(pdb_path, chain_id, fasta_sequence):
    if pdb_path.endswith(".cif"):
        parser = MMCIFParser(QUIET=True)
    else:
        parser = PDBParser(QUIET=True)

    structure = parser.get_structure("protein", pdb_path)
    model = structure[0]

    if chain_id not in model:
        raise ValueError(f"Chain {chain_id} not found in structure.")

    chain = model[chain_id]

    # Extract PDB chain sequence
    pdb_seq, residue_ids = extract_chain_sequence(chain)

    # Build mapping
    mapping = build_pdb_to_fasta_mapping(
        pdb_seq,
        fasta_sequence,
        residue_ids
    )

    # Run DSSP
    dssp = DSSP(model, pdb_path)

    features = []

    for residue in chain:
        if residue.id[0] != " ":
            continue

        if residue.id not in mapping:
            continue

        fasta_position = mapping[residue.id]

        dssp_key = (chain_id, residue.id)
        if dssp_key not in dssp:
            continue

        dssp_data = dssp[dssp_key]

        secondary_structure = dssp_data[2]
        relative_sasa = dssp_data[3]
        buried_flag = 1 if relative_sasa < 0.2 else 0

        features.append({
            "position": fasta_position,
            "secondary_structure": secondary_structure,
            "relative_sasa": relative_sasa,
            "buried_flag": buried_flag
        })

    return pd.DataFrame(features)
