#!/usr/bin/env python3
"""Test script to debug the get_current_app function."""

import subprocess

def test_adb_command():
    """Test the ADB command that's failing."""
    device_id = "2b2289c9"
    adb_prefix = ["adb", "-s", device_id]
    
    print(f"Running command: {' '.join(adb_prefix + ['shell', 'dumpsys', 'window'])}")
    
    try:
        result = subprocess.run(
            adb_prefix + ["shell", "dumpsys", "window"], 
            capture_output=True, 
            text=True,
            encoding='utf-8'  # Explicitly set encoding
        )
        
        print(f"Return code: {result.returncode}")
        print(f"Stdout is None: {result.stdout is None}")
        print(f"Stderr is None: {result.stderr is None}")
        
        if result.stdout:
            print(f"Stdout length: {len(result.stdout)}")
            # Print first few lines
            lines = result.stdout.split('\n')[:10]
            for i, line in enumerate(lines):
                print(f"Line {i}: {line}")
                
            # Check for mCurrentFocus
            for line in result.stdout.split('\n'):
                if 'mCurrentFocus' in line:
                    print(f"Found mCurrentFocus: {line}")
                    break
        else:
            print("Stdout is empty or None")
            
        if result.stderr:
            print(f"Stderr: {result.stderr}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    test_adb_command()