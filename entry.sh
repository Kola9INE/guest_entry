#!/bin/bash
echo "I'm to open a streamlit app in local host"
cd "C:\Users\HP\Desktop\guest_entry"
echo "Activating environment..."
source temp_guest/Scripts/activate
cd guest_ms
streamlit run bravaFD.py