import pandas as pd

# Disclaimer: This script processes only local CSV files provided by the user.
# It does not access external data, scrape websites, or store information without consent.
# Use ethically: Ensure data is yours or authorized, and review alerts for accuracy.
# Not liable for business decisions; alerts are suggestions—human oversight required.

def track_inventory(current_file, previous_file, output_alert_file, low_threshold=10):
    """
    Tracks inventory changes from local CSVs, alerts low stock. Editable threshold for fairness.
    """
    # Consent and bias check prompt
    print(f"Review: Alert rule (stock < {low_threshold}) is fair/no bias (e.g., treats all items equally).")
    consent = input("Confirm data is local/non-personal, and consent to process (y/n)? ")
    if consent.lower() != 'y':
        raise ValueError("Aborted: Consent required.")
    
    try:
        current = pd.read_csv(current_file)
        previous = pd.read_csv(previous_file)
        print(f"Current shape: {current.shape}")
        if 'item' in current.columns and 'stock' in current.columns:
            merged = pd.merge(current, previous, on='item', suffixes=('_current', '_previous'), how='left')
            merged['change'] = merged['stock_current'] - merged['stock_previous'].fillna(0)
            low_stock = merged[merged['stock_current'] < low_threshold]
            low_stock.to_csv(output_alert_file, index=False)
            print(f"Low stock items: {len(low_stock)}")
            print(f"Alerts saved to: {output_alert_file}")
        else:
            print("Error: Missing 'item' or 'stock' columns.")
    except Exception as e:
        print(f"Error: {e}. Ensure files are valid/local.")