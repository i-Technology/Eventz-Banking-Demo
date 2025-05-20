#!/bin/bash

echo "📡 Running Eventz Banking Demo Simulation"
python3 main.py

echo "🧾 Converting business summary to PDF..."
pandoc Y_summary_report.md -o Y_summary_report.pdf

echo "✅ Done! Open Y_summary_report.pdf to view stakeholder summary."
