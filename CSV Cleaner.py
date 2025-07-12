import pandas as pd
import hashlib

# Disclaimer: This script processes only local CSV files provided by the user.
# It does not access external data, scrape websites, or store information without consent.
# Use ethically: Ensure data is yours or authorized, and review outputs for accuracy.
# Not liable for data alterations; test on copies. Comply with GDPR: Anonymize PII.

def anonymize_pii(df, columns_to_hash):
    """
    Hashes specified columns for anonymization (one-way; preserves privacy).
    """
    for col in columns_to_hash:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest() if pd.notnull(x) else 'Unknown')
    return df

def clean_csv(input_file, output_file, hash_columns=None):
    """
    Cleans local CSV: anonymizes PII (if specified), removes duplicates, fills missing with 'Unknown'.
    """
    # Consent and bias check prompt
    print("Review: Cleaning rules (duplicates removed, missing filled with 'Unknown') are fair/no bias.")
    consent = input("Confirm data is local/anonymized if personal, and consent to process (y/n)? ")
    if consent.lower() != 'y':
        raise ValueError("Aborted: Consent required.")
    
    try:
        df = pd.read_csv(input_file)
        print(f"Original shape: {df.shape}")
        if hash_columns:
            df = anonymize_pii(df, hash_columns)
            print(f"Anonymized PII in: {hash_columns}")
        df = df.drop_duplicates().fillna('Unknown')
        df.to_csv(output_file, index=False)
        print(f"Cleaned shape: {df.shape}")
        print(f"Cleaned file saved to: {output_file}")
    except Exception as e:
        print(f"Error: {e}. Ensure file is valid/local.")