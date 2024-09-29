#!/bin/bash
echo "I'm to open a streamlit app in local host"
cd "C:\Users\HP\Desktop\guest_entry"
cd "temp_guest"
echo "Activating environment..."
cd 'Scripts'
activate
echo "Going back to entry folder"
cd ../..
cd 'guest_ms'
streamlit run entry.py