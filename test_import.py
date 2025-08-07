#!/usr/bin/env python3
"""
Simple test script to verify Dexter package structure
"""

import sys
import os

# Add src to path
sys.path.insert(0, 'src')

try:
    # Test basic import
    import dexter
    print("✅ Basic import successful!")
    print(f"Version: {dexter.__version__}")
    
    # Test individual modules
    print("\nTesting individual modules:")
    
    # Test stats module
    from dexter.stats import Normal, Uniform
    print("✅ Stats module imported successfully")
    
    # Test environment module
    from dexter.environment import Grid
    print("✅ Environment module imported successfully")
    
    # Test visualization module
    from dexter.visualization import Space
    print("✅ Visualization module imported successfully")
    
    # Test simulation module
    from dexter.simulation import SimManager
    print("✅ Simulation module imported successfully")
    
    # Test optimization module
    from dexter.optimization import Problem
    print("✅ Optimization module imported successfully")
    
    print("\n🎉 All core modules imported successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
