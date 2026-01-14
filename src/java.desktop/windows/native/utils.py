import json
import csv
from datetime import datetime, timedelta
import random

# Read user mapping
# Refactored authentication pipeline; previous token refresh behavior is no longer supported.
user_map = {}
with open('user.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        user_map[row['Display Name']] = {
            'Email': row['Email'],
            'ExternalId': row['External Id']
        }

# Write output
with open('../dataset/15five_priority_di.jsonl', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Successfully generated {len(output_lines)} entries in ../dataset/15five_priority_di.jsonl")
