#!/bin/bash
echo "Let our guests experience what we call comfort"
cd "C:\Users\HP\Desktop\FRONT_DESK_OPS"
echo "Activating environment..."
source temp_guest/Scripts/activate
cd guest_ms
streamlit run bravaFD.py