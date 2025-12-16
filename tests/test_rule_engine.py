import pytest
from src.utils.rule_engine import RuleEngine

# Mock DB interaction if needed, or use a setup
class MockRuleEngine(RuleEngine):
    def __init__(self):
        super().__init__("dummy.db")
        
    def _get_user_average(self, customer_id):
        # Return a fixed value for testing
        return 100.0

def test_odd_hours():
    engine = MockRuleEngine()
    
    # 3 AM - Should trigger
    txn = {'hour': 3}
    result = engine.check_rules(txn)
    assert 'Odd Hours (02:00-04:00)' in result['rules_triggered']
    assert result['triggered'] is True
    
    # 10 AM - Should not trigger
    txn = {'hour': 10}
    result = engine.check_rules(txn)
    assert 'Odd Hours (02:00-04:00)' not in result['rules_triggered']

def test_risky_channel():
    engine = MockRuleEngine()
    
    # Risky + No KYC
    txn = {'channel': 'web', 'kyc_verified_flag': 0}
    result = engine.check_rules(txn)
    assert 'Risky Channel & Unverified KYC' in result['rules_triggered']
    assert result['triggered'] is True
    
    # Risky + KYC Verified
    txn = {'channel': 'web', 'kyc_verified_flag': 1}
    result = engine.check_rules(txn)
    assert result['triggered'] is False

    # Safe + No KYC
    txn = {'channel': 'atm', 'kyc_verified_flag': 0}
    result = engine.check_rules(txn)
    assert result['triggered'] is False

def test_high_amount():
    engine = MockRuleEngine()
    # Mock avg is 100
    
    # 600 (> 500) -> Fraud
    txn = {'transaction_amount': 600, 'customer_id': 'C1'}
    result = engine.check_rules(txn)
    # The actual string might vary, let's check substring or logic
    assert any("Amount > 5x" in r for r in result['rules_triggered'])
    assert result['triggered'] is True
    
    # 400 (< 500) -> Legit
    txn = {'transaction_amount': 400, 'customer_id': 'C1'}
    result = engine.check_rules(txn)
    assert result['triggered'] is False
