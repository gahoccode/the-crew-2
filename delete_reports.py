#!/usr/bin/env python3
"""
Python script to delete report files and temporary database files
Usage: python delete_reports.py
"""

import os
import glob
import sys


def delete_reports():
    """Delete report files and temporary database files."""
    print("Deleting report files and temporary database files...")
    
    # List of files to delete
    files_to_delete = [
        "report.md",
        "news.md", 
        "executive_summary.md"
    ]
    
    # Delete each file if it exists
    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except OSError as e:
                print(f"Error deleting {file}: {e}")
        else:
            print(f"File not found: {file}")
    
    # Delete ChromaDB lock files
    print("Cleaning up ChromaDB lock files...")
    try:
        lock_files = glob.glob("chromadb-*.lock")
        for lock_file in lock_files:
            os.remove(lock_file)
            print(f"Deleted: {lock_file}")
        
        if not lock_files:
            print("No ChromaDB lock files found")
        else:
            print(f"Deleted {len(lock_files)} ChromaDB lock files")
            
    except OSError as e:
        print(f"Error cleaning ChromaDB lock files: {e}")
    
    print("Done!")


if __name__ == "__main__":
    delete_reports()