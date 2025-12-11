#!/bin/bash
echo "=== DEBUG RPA ==="
echo "Timestamp: $(date)"
echo "User: $(whoami)"
echo "Working directory: $(pwd)"
echo "Python version: $(python3 --version)"
echo "Environment variables:"
env | grep -E "(DISPLAY|PATH|PYTHON)"
echo "Processes:"
ps aux | grep python
echo "Files in temp/:"
ls -la temp/ 2>/dev/null || echo "temp/ not found"
echo "Files in rpa_data/:"
ls -la rpa_data/ 2>/dev/null || echo "rpa_data/ not found"
echo "Redis status:"
redis-cli ping 2>/dev/null || echo "Redis not available"



























