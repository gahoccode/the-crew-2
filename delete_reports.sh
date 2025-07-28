#!/bin/bash

# Shell script to delete report files and temporary database files
# Usage: ./delete_reports.sh

echo "Deleting report files and temporary database files..."

# List of files to delete
files_to_delete=(
    "report.md"
    "news.md"
    "executive_summary.md"
)

# Delete each file if it exists
for file in "${files_to_delete[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "Deleted: $file"
    else
        echo "File not found: $file"
    fi
done

# Delete ChromaDB lock files
echo "Cleaning up ChromaDB lock files..."
find . -name "chromadb-*.lock" -type f -delete 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Deleted ChromaDB lock files"
fi

echo "Done!"
