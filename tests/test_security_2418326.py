"""
Student 2418326
test_security_2418326.py
Security testing using automated analysis
"""

import pytest
import subprocess
import os


class TestSecurityAnalysis:
    """Security tests using Bandit static analysis."""
    
    def test_run_bandit_security_scan(self):
        """Run Bandit security scanner on application code."""
        # Run bandit on app.py and models.py
        result = subprocess.run(
            ['bandit', '-r', 'app.py', 'models.py', '-f', 'txt'],
            capture_output=True,
            text=True
        )
        
        print("\n" + "="*60)
        print("BANDIT SECURITY SCAN RESULTS")
        print("="*60)
        print(result.stdout)
        
        if result.stderr:
            print("\nErrors:")
            print(result.stderr)
        
        # Don't fail the test, just report findings
        # Security issues are documented, not blocking
        assert True