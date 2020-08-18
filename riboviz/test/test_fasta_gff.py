"""
:py:mod:`riboviz.test_fasta_gff` tests.
"""
import os
import tempfile
import pytest
import pandas as pd
from riboviz import fasta_gff
from riboviz.test import data


TEST_FASTA_FILE = os.path.join(os.path.dirname(data.__file__),
                               "test_fasta_gff_data.fasta")
""" Test FASTA file in :py:mod:`riboviz.test.data`. """
TEST_GFF_FILE = os.path.join(os.path.dirname(data.__file__),
                             "test_fasta_gff_data.gff")
""" Test GFF file in :py:mod:`riboviz.test.data`. """


@pytest.fixture(scope="function")
def tmp_file():
    """
    Create a temporary file.

    :return: path to temporary file
    :rtype: str or unicode
    """
    _, tmp_file = tempfile.mkstemp(prefix="tmp")
    yield tmp_file
    if os.path.exists(tmp_file):
        os.remove(tmp_file)


@pytest.mark.parametrize("seq_codons", [
    ("", []),
    ("A", ["A"]),
    ("GA", ["GA"]),
    ("GAT", ["GAT"]),
    ("GATT", ["GAT", "T"]),
    ("ATGAAATAA", ["ATG", "AAA", "TAA"]),
    ("ATGGGGCCCTAG", ["ATG", "GGG", "CCC", "TAG"])])
def test_sequence_to_codons(seq_codons):
    """
    Test :py:func:`riboviz.fasta_gff.sequence_to_codons`
    with values vaid sequences.

    :param seq_codons: sequence and expected codons
    :type seq_codons: tuple(str or unicode, list(str or unicode))
    """
    sequence, codons = seq_codons
    assert fasta_gff.sequence_to_codons(sequence) == codons,\
        "Unexpected codons"


def check_seqs_cds_codons_df(seqs_cds_codons, df):
    """
    Check contents of DataFrame output by
    :py:func:`riboviz.fasta_gff.seqs_cds_codons_to_df` contain the
    given codons for the given genes.

    :param seqs_cds_codons: Dictionary keyed by genes and with values
    that are lists of codons
    :type seqs_cds_codons: dict
    :param df: Pandas DataFrame
    :rtype: pandas.core.frame.DataFrame
    """
    num_rows, num_columns = df.shape
    assert num_columns == 3, "Unexpected number of columns"
    for column in [fasta_gff.GENE, fasta_gff.POS, fasta_gff.CODON]:
        assert column in list(df.columns),\
            "Missing column {}".format(column)
    total_codon_length = sum([len(codons)
                              for codons in seqs_cds_codons.values()])
    assert num_rows == total_codon_length, \
        "Unexpected number of rows"
    for seqid, cds_codons in seqs_cds_codons.items():
        seq_df = df.loc[df[fasta_gff.GENE] == seqid]
        assert not seq_df.empty, "Missing row for {}".format(seqid)
        num_rows, _ = seq_df.shape
        assert num_rows == len(cds_codons), \
            "Unexpected number of rows for {}".format(seqid)
        for pos, cds_codon in zip(seq_df[fasta_gff.POS],
                                  seq_df[fasta_gff.CODON]):
            # POS is 1-indexed.
            assert cds_codons[pos - 1] == cds_codon


def test_seqs_cds_codons_to_df_empty():
    """
    Test :py:func:`riboviz.fasta_gff.seqs_cds_codons_to_df`
    with no values produces an empty data frame.
    """
    df = fasta_gff.seqs_cds_codons_to_df({})
    check_seqs_cds_codons_df({}, df)


def test_seqs_cds_codons_to_df():
    """
    Test :py:func:`riboviz.fasta_gff.seqs_cds_codons_to_df`
    with values produces a data frame with the expected columns,
    rows and values.
    """
    seqs_cds_codons = {
        "G1": fasta_gff.sequence_to_codons("ATGAAATAA"),
        "G2": fasta_gff.sequence_to_codons("ATGGGGCCCTAG")
    }
    df = fasta_gff.seqs_cds_codons_to_df(seqs_cds_codons)
    check_seqs_cds_codons_df(seqs_cds_codons, df)


def test_extract_cds_codons_empty_fasta(tmp_file):
    """
    Test :py:func:`riboviz.fasta_gff.extract_cds_codons` with an empty
    FASTA file and a GFF file (:py:const:`TEST_GFF_FILE`). A
    header-only TSV file is expected as output.

    :param tmp_file: Temporary file
    :type tmp_file: str or unicode
    """
    # Use tmp_file as both empty FASTA input file and TSV output
    # file
    fasta_gff.extract_cds_codons(tmp_file, TEST_GFF_FILE, tmp_file)
    df = pd.read_csv(tmp_file, delimiter="\t", comment="#")
    check_seqs_cds_codons_df({}, df)


def test_extract_cds_codons(tmp_file):
    """
    Test :py:func:`riboviz.fasta_gff.extract_cds_codons` with a
    FASTA file (:py:const:`TEST_FASTA_FILE`) and a GFF file
    (:py:const:`TEST_GFF_FILE`) and validate the TSV file output.

    :param tmp_file: Temporary file
    :type tmp_file: str or unicode
    """
    fasta_gff.extract_cds_codons(TEST_FASTA_FILE, TEST_GFF_FILE, tmp_file)
    df = pd.read_csv(tmp_file, delimiter="\t", comment="#")
    # Expected codons based on data in test_fasta_gff_data.fasta and
    # test_fasta_gff_data.gff.
    seqs_cds_codons = {
        "YAL001C_mRNA": ["ATG", "GCC", "CAC", "TGT", "TAA"],
        "YAL002C_mRNA": ["ATG", "GTA", "TCA", "GGA", "TAG"],
        "YAL004CSingleCDS_mRNA": ["ATG", "AGA", "TGA"],
        "YAL005CMultiCDS_mRNA": ["ATG", "AGA", "TGA", "ATG", "GAT",
                                 "TAC", "TAG"]
    }
    check_seqs_cds_codons_df(seqs_cds_codons, df)
