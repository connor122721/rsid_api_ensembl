# Connor Murray
# Extract RSID for each SNP using rest.ensembl
# Created: 12.10.2024

# Load packages
import os
import requests
import pandas as pd
import pyreadr as pr

# Working directory
os.chdir("/standard/vol185/cphg_Manichaikul/users/csm6hg")

# Query function
def get_rsid_from_gff3(chrom, pos):
    """
    Query the Ensembl API to get RSID for a given chromosome and position.
    """
    url = f"https://rest.ensembl.org/overlap/region/homo_sapiens/{chrom}:{pos}-{pos}?feature=variation;content-type=text/x-gff3"
    response = requests.get(url)
    
    if not response.ok:
        print(f"Error: {response.status_code} for {chrom}:{pos}")
        return None
    
    gff3_data = response.text
    
    for line in gff3_data.splitlines():
        if not line.startswith("#"):
            fields = line.split("\t")
            if len(fields) >= 9:
                attributes = fields[8]
                for attr in attributes.split(";"):
                    if attr.startswith("ID="):
                        rsid = attr.split("=")[1].replace("sequence_variant:", "")
                        return rsid
    return None

# Load sentinel variant list
sig_genes_file = "data/qtl.rna.saturation.maf01.11.12.24.rds"
output_file = "data/rsid_output.csv"

# Read the RDS file
sig_genes = pr.read_r(sig_genes_file)
sig_genes = sig_genes[None] 

# Filter the DataFrame based on the conditions for maxPC and pval_perm
filtered_sig_genes = sig_genes[(sig_genes['maxPC'] == 11) & (sig_genes['pval_perm'] < 0.05)]

# Extract unique variants
unique_variants = filtered_sig_genes['variant_id'].to_list()

# Initialize results list
results = []

# Iterate through each variant and extract RSID
for variant in unique_variants:
    chrom, pos = variant.split(":")
    pos = pos.split("[")[0]  # Remove brackets and annotations
    
    print(f"Processing {chrom}:{pos}...")
    rsid = get_rsid_from_gff3(chrom.replace("chr", ""), pos)
    
    results.append({
        "variant_id": variant,
        "chromosome": chrom,
        "position": pos,
        "rsid": rsid,
        "pval_perm": filtered_sig_genes.loc[filtered_sig_genes['variant_id'] == variant, 'pval_perm'].values[0],
        "maxPC": filtered_sig_genes.loc[filtered_sig_genes['variant_id'] == variant, 'maxPC'].values[0]
    })
    
    # Save intermediate results to output file
    if not os.path.exists(output_file) or os.stat(output_file).st_size == 0:
        pd.DataFrame(results).to_csv(output_file, index=False)
    else:
        pd.DataFrame([results[-1]]).to_csv(output_file, mode='a', header=False, index=False)

print(f"Processing complete. Results saved to {output_file}.")