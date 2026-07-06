"""Generate assignment CSV data for configured modules.

What the script does:
- Stores assignment records in a structured Python list of dictionaries.
- Normalizes mixed date formats into one standard format (YYYY-MM-DD).
- Maps source fields into clean CSV columns with snake_case names.
- Derives number_of_hours from credits using a consistent formula (credits * 2.5).
- Writes a ready-to-use CSV file for downstream analysis.

Usage:
	python3 create_assignment_data.py

This creates:
	data/assignment_dummy_data.csv

Optional argument:
	--output data/my_assignments.csv
		Write to a different CSV file.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path


# Source rows provided for ZDAT1003 and ZDAT1002. Date formats from the source
# are mixed, so dates are normalized to ISO format during row construction.
SOURCE_ASSIGNMENTS = [
	{
		"assignment_name": "Multiple Choice Probability and Statistics Test 1",
		"module_name": "Data Analysis Portfolio Assessment",
		"module_code": "ZDAT1003",
		"credits": 2,
		"release_date": "02/02/26",
		"final_deadline": "2/2/2026",
	},
	{
		"assignment_name": "Multiple Choice Probability and Statistics Test 2",
		"module_name": "Data Analysis Portfolio Assessment",
		"module_code": "ZDAT1003",
		"credits": 2,
		"release_date": "16/03/26",
		"final_deadline": "3/16/2026",
	},
	{
		"assignment_name": "Multiple Choice Probability and Statistics Test 3",
		"module_name": "Data Analysis Portfolio Assessment",
		"module_code": "ZDAT1003",
		"credits": 4,
		"release_date": "17/03/26",
		"final_deadline": "3/17/2026",
	},
	{
		"assignment_name": "Mini Portfolio 1",
		"module_name": "Data Analysis Portfolio Assessment",
		"module_code": "ZDAT1003",
		"credits": 2,
		"release_date": "06/04/26",
		"final_deadline": "5/27/2026",
	},
	{
		"assignment_name": "Mini Portfolio 2",
		"module_name": "Data Analysis Portfolio Assessment",
		"module_code": "ZDAT1003",
		"credits": 2,
		"release_date": "13/04/26",
		"final_deadline": "5/27/2026",
	},
	{
		"assignment_name": "Mini Portfolio 3",
		"module_name": "Data Analysis Portfolio Assessment",
		"module_code": "ZDAT1003",
		"credits": 2,
		"release_date": "20/04/26",
		"final_deadline": "5/27/2026",
	},
	{
		"assignment_name": "Mini Portfolio 4",
		"module_name": "Data Analysis Portfolio Assessment",
		"module_code": "ZDAT1003",
		"credits": 2,
		"release_date": "27/04/26",
		"final_deadline": "5/27/2026",
	},
	{
		"assignment_name": "Statistical Report",
		"module_name": "Data Analysis Portfolio Assessment",
		"module_code": "ZDAT1003",
		"credits": 24,
		"release_date": "01/06/26",
		"final_deadline": "6/24/2026",
	},
	{
		"assignment_name": "Maths Portfolio Task 1",
		"module_name": "Fundamental Skills Assessment",
		"module_code": "ZDAT1002",
		"credits": 5,
		"release_date": "27/10/25",
		"final_deadline": "09/06/26",
	},
	{
		"assignment_name": "Maths Portfolio Task 2",
		"module_name": "Fundamental Skills Assessment",
		"module_code": "ZDAT1002",
		"credits": 5,
		"release_date": "24/11/26",
		"final_deadline": "09/06/26",
	},
	{
		"assignment_name": "Maths Portfolio Task 3",
		"module_name": "Fundamental Skills Assessment",
		"module_code": "ZDAT1002",
		"credits": 5,
		"release_date": "02/02/26",
		"final_deadline": "09/06/26",
	},
	{
		"assignment_name": "Maths Portfolio Task 4",
		"module_name": "Fundamental Skills Assessment",
		"module_code": "ZDAT1002",
		"credits": 5,
		"release_date": "16/03/26",
		"final_deadline": "09/06/26",
	},
	{
		"assignment_name": "Maths Portfolio Task 5",
		"module_name": "Fundamental Skills Assessment",
		"module_code": "ZDAT1002",
		"credits": 5,
		"release_date": "18/05/26",
		"final_deadline": "09/06/26",
	},
	{
		"assignment_name": "Data Science Pipeline in your Workplace Task",
		"module_name": "Fundamental Skills Assessment",
		"module_code": "ZDAT1002",
		"credits": 5,
		"release_date": "07/01/26",
		"final_deadline": "18/02/26",
	},
	{
		"assignment_name": "Data Pipeline Poster",
		"module_name": "Fundamental Skills Assessment",
		"module_code": "ZDAT1002",
		"credits": 5,
		"release_date": "30/03/26",
		"final_deadline": "17/06/26",
	},
	{
		"assignment_name": "Calculus Video Assessment",
		"module_name": "Fundamental Skills Assessment",
		"module_code": "ZDAT1002",
		"credits": 5,
		"release_date": "19/05/26",
		"final_deadline": "24/06/26",
	},
	{
		"assignment_name": "Reflective Coursework",
		"module_name": "Synoptic Data Science Assessment 1",
		"module_code": "ZDAT1004",
		"credits": 16,
		"release_date": "16/03/26",
		"final_deadline": "03/06/26",
	},
	{
		"assignment_name": "Multiple Choice Knowledge Test",
		"module_name": "Synoptic Data Science Assessment 2",
		"module_code": "ZDAT1004",
		"credits": 4,
		"release_date": "06/07/26",
		"final_deadline": "06/07/26",
	},
	{
		"assignment_name": "Assessment Part 1",
		"module_name": "Software Portfolio Assessment",
		"module_code": "ZDAT1001",
		"credits": 10,
		"release_date": "12/01/26",
		"final_deadline": "28/01/26",
	},
	{
		"assignment_name": "Assessment Part 2",
		"module_name": "Software Portfolio Assessment",
		"module_code": "ZDAT1001",
		"credits": 10,
		"release_date": "16/03/26",
		"final_deadline": "22/04/26",
	},
	{
		"assignment_name": "Assessment Part 3",
		"module_name": "Software Portfolio Assessment",
		"module_code": "ZDAT1001",
		"credits": 20,
		"release_date": "04/05/26",
		"final_deadline": "17/06/26",
	},
]

# These headers define the exact CSV schema expected by the prototype dataset.
COLUMNS = [
	"module_code",
	"module_name",
	"assignment_name",
	"release_date",
	"due_date",
	"number_of_credits",
	"number_of_hours",
]


def parse_source_date(date_text: str) -> str:
	"""Convert supported source date strings to ISO format.

	Args:
		date_text: Source date string in DD/MM/YY, DD/MM/YYYY, or M/D/YYYY
			format. Empty and "NA" values are allowed.

	Returns:
		Date string in YYYY-MM-DD format, or an empty string if unavailable.

	Raises:
		ValueError: If the date does not match any supported format.
	"""

	clean_date_text = date_text.strip()
	if clean_date_text == "" or clean_date_text.upper() == "NA":
		return ""

	for date_format in ("%d/%m/%y", "%d/%m/%Y", "%m/%d/%Y"):
		try:
			return datetime.strptime(clean_date_text, date_format).date().isoformat()
		except ValueError:
			continue

	raise ValueError(f"Unsupported date format: {clean_date_text}")


def parse_credits(value: str | int | float) -> int:
	"""Convert source credits to an integer.

	Args:
		value: Credits value from the source data.

	Returns:
		Integer credits. Empty values return 0.
	"""

	if isinstance(value, str):
		clean_value = value.strip()
		if clean_value == "":
			return 0
		return int(float(clean_value))

	return int(value)


def build_rows() -> list[dict[str, str | int | float]]:
	"""Build assignment rows for CSV output from source assignment data.

	Returns:
		A list of dictionaries representing assignment rows.
	"""

	rows: list[dict[str, str | int | float]] = []

	for assignment in SOURCE_ASSIGNMENTS:
		credits = parse_credits(assignment["credits"])

		# Map source columns to the required output schema.
		rows.append(
			{
				"module_code": assignment["module_code"],
				"module_name": assignment["module_name"],
				"assignment_name": assignment["assignment_name"],
				"release_date": parse_source_date(str(assignment["release_date"])),
				"due_date": parse_source_date(str(assignment["final_deadline"])),
				"number_of_credits": credits,
				"number_of_hours": credits * 2.5,
			}
		)

	return rows


def write_csv(output_path: Path, rows: list[dict[str, str | int | float]]) -> None:
	"""Write assignment rows to a CSV file.

	Args:
		output_path: Destination path for the CSV file.
		rows: Assignment rows to write.

	Returns:
		None.
	"""

	# Ensure the repo-level data folder exists before writing the output file.
	output_path.parent.mkdir(parents=True, exist_ok=True)

	with output_path.open("w", newline="", encoding="utf-8") as csv_file:
		# DictWriter uses the fixed column order defined in COLUMNS.
		writer = csv.DictWriter(csv_file, fieldnames=COLUMNS)
		writer.writeheader()
		writer.writerows(rows)


def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments for CSV generation.

	Returns:
		The parsed command-line arguments.
	"""

	# Keep the CLI minimal by exposing only the output file path.
	parser = argparse.ArgumentParser(
		description="Generate assignment CSV data for configured modules."
	)
	parser.add_argument(
		"--output",
		type=Path,
		default=Path("data/assignment_dummy_data.csv"),
		help="Path to the CSV file to create.",
	)
	return parser.parse_args()


def main() -> None:
	"""Generate the assignment CSV file from the provided options.

	Returns:
		None.
	"""

	# Read command-line settings first so the script can be reused without
	# editing the source file each time.
	args = parse_args()

	# Generate rows from the fixed source dataset, then write one CSV file.
	rows = build_rows()
	write_csv(args.output, rows)

	# Print a short confirmation so the user can see where the file was created.
	print(f"Created {args.output} with {len(rows)} row(s).")


if __name__ == "__main__":
	main()
