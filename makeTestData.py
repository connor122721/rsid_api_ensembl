# module load anaconda/2023.07-py3.11
# source activate msprime_env

# Load packages
import pandas as pd
import os

# Working directory
os.chdir("/standard/vol185/cphg_Manichaikul/users/csm6hg")

# Create a simplified dataset for testing
test_data = {
    'variant_id': ['1:1026225', '2:2000000', '3:3000000', '4:4000000', '5:5000000'],
    'maxPC': [11, 11, 10, 11, 11],
    'pval_perm': [0.01, 0.03, 0.05, 0.02, 0.001]
    }

# Convert to a DataFrame
test_df = pd.DataFrame(test_data)

# Save to a CSV file
test_df.to_csv("data/test_data.csv", index=False)

# Load the file as if it were the input dataset
loaded_test_df = pd.read_csv("data/test_data.csv")
print(loaded_test_df)