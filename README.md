Tiny toolbox with two standalone Python scripts for decoding / analyzing message and event datasets (e.g., exported logs). The goal is to quickly parse raw text/CSV/JSON-like dumps and compute simple stats you can explore or pipe into other tools.
Files: messages_analyzer.py and events_analyzer.py. 

What’s inside

messages_analyzer.py – helpers to read a message dump and summarize activity (per-sender counts, simple time-based groupings, basic text stats). 

events_analyzer.py – utilities to scan event-style records and build quick aggregates over time (occurrence counts, simple timelines).
