# RSID Extraction Tool
These Python scripts extracts RSIDs (Reference SNP IDs) for genomic variants using the Ensembl REST API (assuming HG38). It retrieves RSIDs based on chromosome and position, and writes the results to an output CSV file.

# VCF Annotation Extraction
These scripts extracts the relevant column of a VCF annotated with SNPeff (https://pcingola.github.io/SnpEff/snpeff/introduction/) and seperates "gene ID" and associated consequences.

## Features
- Retrieves RSIDs from the Ensembl REST API using GFF3-formatted responses.
- Handles chromosome and position data efficiently, the script currently removes "chr" from the variant_id column.

## Requirements
To install these dependencies, run:
```bash
pip install pandas requests pyreadr 
```
