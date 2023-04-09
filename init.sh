#!/bin/bash
rm -f qc.db
python -m api.scripts.db_setup
python api.py

