"""
Workflow file name constants.
"""

ADAPTER_TRIM_FQ = "trim.fq"
""" Adapter trimmed reads file name. """
NON_RRNA_FQ = "nonrRNA.fq"
""" Non-rRNA reads file name. """
RRNA_MAP_SAM = "rRNA_map.sam"
""" rRNA-mapped reads file name. """
ORF_MAP_SAM = "orf_map.sam"
""" ORF-mapped reads file name. """
ORF_MAP_CLEAN_SAM = "orf_map_clean.sam"
""" ORF-mapped reads with mismatched nts trimmed file name. """
ORF_MAP_CLEAN_BAM = "orf_map_clean.bam"
""" ORF-mapped reads with mismatched nts trimmed file name (Nextflow only). """
TRIM_5P_MISMATCH_TSV = "trim_5p_mismatch.tsv"
""" Trim 5' mismatches summary file name. """
UNALIGNED_FQ = "unaligned.fq"
""" Unaligned reads file name. """
UMI_EXTRACT_FQ = "extract_trim.fq"
""" Adapter trimmed reads with UMIs extracted file name. """
PRE_DEDUP_BAM = "pre_dedup.bam"
""" Pre-deduplication file name. """
DEDUP_BAM = "dedup.bam"
""" Deduplicated reads file name (Nextflow only). """
PRE_DEDUP_GROUPS_TSV = "pre_dedup_groups.tsv"
""" Pre-deduplication UMI groups file name. """
POST_DEDUP_GROUPS_TSV = "post_dedup_groups.tsv"
""" Post-deduplication UMI groups file name. """
DEDUP_STATS_PREFIX = "dedup_stats"
""" UMI deduplication statistics file name prefix. """
DEDUP_STATS_FORMAT = DEDUP_STATS_PREFIX + "_{}"
""" UMI deduplication statistics file name format. """
DEPLEX_DIR_FORMAT = "{}_deplex"
""" Demultiplexed data directory name format. """
ADAPTER_TRIM_FQ_FORMAT = "{}_trim.fq"
""" Adapter trimmed multiplexed reads file name format."""
UMI_EXTRACT_FQ_FORMAT = "{}_extract_trim.fq"
""" Adapter trimmed multiplexed reads with UMIs extracted file name format. """
MINUS_BEDGRAPH = "minus.bedgraph"
""" Reads from minus strand bedgraph file name."""
PLUS_BEDGRAPH = "plus.bedgraph"
""" Reads from plus strand bedgraph file name."""
READ_COUNTS_FILE = "read_counts.tsv"
""" Read counts file name. """
DEFAULT_CMD_FILE = "run_riboviz_vignette.sh"
""" Default bash commands file name. """
