#!/usr/bin/env python3
"""
Arquivo WSGI para produção
"""

from app import app

if __name__ == "__main__":
    app.run()
