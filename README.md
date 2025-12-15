# AI Ops Assistant – Order Intelligence System

This project is a simple AI Ops Assistant that processes incoming orders and makes operational decisions based on inventory availability and daily production capacity.

## Features
- Automatically reads orders and inventory data
- Tracks daily production capacity (200 units/day)
- Prevents negative inventory
- Handles urgent and normal orders
- Generates decisions: Approve, Split, Delay, Escalate
- Produces human-readable reasoning
- Logs execution to a file

## Tech Stack
- Python
- Pandas

## How to Run
1. Install Python 3
2. Install dependency:
3. Run the program:

## Output
- Console output with decisions
- Log file `output.log` containing execution proof

## Notes
- This system focuses on execution and logic, not theory.
- Designed to behave like a real Ops Assistant.
