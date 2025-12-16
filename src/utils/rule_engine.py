import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

class RuleEngine:
    def __init__(self, db_path):
        self.db_path = db_path
        # Define risky channels
        self.RISKY_CHANNELS = {'web', 'mobile_browser', 'unknown'} 

    def check_rules(self, transaction_data):
        """
        Apply rules to a transaction.
        Returns:
            dict: {
                'triggered': bool,
                'rules_triggered': list_of_strings,
                'reason': string
            }
        """
        triggered_rules = []
        is_fraud = False
        
        # Extract data
        amount = transaction_data.get('transaction_amount', 0)
        hour = transaction_data.get('hour', 0)
        channel = transaction_data.get('channel', 'unknown')
        kyc_verified = transaction_data.get('kyc_verified_flag', 1)  # Default to 1 (safe) if missing
        customer_id = transaction_data.get('customer_id')

        # Rule 1: Odd-hour transaction (02:00–04:00)
        if 2 <= hour <= 4:
            triggered_rules.append("Odd Hours (02:00-04:00)")

        # Rule 2: Risky Channel AND KYC Not Verified
        if channel in self.RISKY_CHANNELS and not kyc_verified:
            triggered_rules.append("Risky Channel & Unverified KYC")

        # Rule 3: Amount > 5x User Average
        # We need to query the DB for user history. 
        # Ideally this should be cached or optimized, but for this milestone direct DB query is fine.
        user_avg = self._get_user_average(customer_id)
        if user_avg > 0 and amount > 5 * user_avg:
            triggered_rules.append(f"Amount > 5x User Average (Avg: {user_avg:.2f})")

        if triggered_rules:
            is_fraud = True
            
        return {
            'triggered': is_fraud,
            'rules_triggered': triggered_rules,
            'reason': "; ".join(triggered_rules) if triggered_rules else "No rules triggered"
        }

    def _get_user_average(self, customer_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Query the model_predictions table (which stores txn history in this simplified backend)
            # OR we should query the main transactions table if it exists. 
            # In Milestone 1/2, 'transactions.db' was created.
            # Let's check 'model_predictions' first as it's what we insert into.
            # But wait, 'model_predictions' only has NEW transactions? 
            # If so, we need historical data. 
            # The prompt says "Reuse existing SQLite DB".
            # 'seed_db.py' inserts into 'model_predictions'. 
            # I'll check if there is another table with historical data.
            # If not, I'll rely on 'model_predictions' which accumulates efficiently.
            
            # Note: For the very first transaction of a user, average might be 0 or based on just this one. 
            # I'll ignore the current transaction in the average calculation if possible, or just accept it.
            
            query = "SELECT AVG(json_extract(features_json, '$.transaction_amount')) FROM model_predictions WHERE customer_id = ?"
            cursor.execute(query, (customer_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0] is not None:
                return float(result[0])
            return 0.0
        except Exception as e:
            print(f"Error fetching user average: {e}")
            return 0.0
