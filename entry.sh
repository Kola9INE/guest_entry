#!/bin/bash
echo "Let our guests experience what we call comfort"
echo "Activating environment..."
source .venv/Scripts/activate
cd guest_ms
streamlit run bravaFD.py
