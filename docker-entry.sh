#!/bin/bash

cd /usr/src/app
pip install --no-cache-dir -q -r requirements.txt
python uc_intg_madvr/driver.py