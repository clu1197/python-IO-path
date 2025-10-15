"""
Task: Merge and Deduplicate CSV Files
You have multiple CSV files in a directory containing user data with duplicates. Write a program that:

Finds all CSV files in a given directory (use pathlib)
Merges them into a single dataset
Removes duplicate users based on email (keep the most recent entry based on a timestamp)
Writes the clean data to a new CSV file sorted by username
Creates a report showing:

Number of files processed
Total records found
Duplicates removed
Final record count


Sample CSV format (users_1.csv, users_2.csv, etc.):
"""

from pathlib import Path
import csv
from datetime import datetime
from collections import defaultdict
import sys

class CSVMerger:
    """Merges and deduplicates CSV files from a directory."""
    
    def __init__(self, input_dir, 
                 output_file="merged_users.csv", 
                 dedupe_field="email", 
                 date_field="signup_date"):
        """
        Initialize the CSV merger.
        
        Args:
            input_dir: Directory containing CSV files
            output_file: Output filename for merged data
            dedupe_field: Field to use for deduplication
            date_field: Field to use for determining most recent entry
        """
        self.input_dir = Path(input_dir)
        self.output_file = Path(output_file)
        self.dedupe_field = dedupe_field
        self.date_field = date_field
        
        # Statistics
        self.stats = {
            "files_processed": 0,
            "total_records": 0,
            "duplicates_removed": 0,
            "final_count": 0,
            "errors": []
        }
        
    def setup_sample_data(self):
        """Create sample CSV files for testing."""
        print("📁 Creating sample data directory and files...")
        
        self.input_dir.mkdir(exist_ok=True)
        
        # Sample data for users_1.csv
        users_1 = [
            ["username", "email", "signup_date", "status"],
            ["john_doe", "john@example.com", "2024-01-15", "active"],
            ["jane_smith", "jane@example.com", "2024-02-20", "active"],
            ["bob_jones", "bob@example.com", "2024-01-10", "inactive"]
        ]
        
        # Sample data for users_2.csv (with duplicates and updates)
        users_2 = [
            ["username", "email", "signup_date", "status"],
            ["john_doe", "JOHN@example.com", "2024-03-01", "premium"],  # Duplicate, newer
            ["alice_wonder", "alice@example.com", "2024-02-15", "active"],
            ["charlie_brown", "charlie@example.com", "2024-01-20", "active"]
        ]
        
        # Sample data for users_3.csv (different column order)
        users_3 = [
            ["email", "username", "status", "signup_date"],  # Different order!
            ["jane@EXAMPLE.com", "jane_smith", "premium", "2024-03-10"],  # Duplicate, newer
            ["david_lee", "david@example.com", "active", "2024-02-01"]
        ]
        
        # Write sample files
        self._write_csv(self.input_dir / "users_1.csv", users_1)
        self._write_csv(self.input_dir / "users_2.csv", users_2)
        self._write_csv(self.input_dir / "users_3.csv", users_3)
        
        # Create an empty file to test edge case
        (self.input_dir / "users_empty.csv").write_text("")
        
        print(f"✅ Created sample files in {self.input_dir}/\n")
    
    def _write_csv(self, filepath, data):
        """Helper to write CSV data."""
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    
    def find_csv_files(self):
        """Find all CSV files in the input directory."""
        if not self.input_dir.exists():
            print(f"❌ Directory {self.input_dir} doesn't exist!")
            return []
        
        csv_files = list(self.input_dir.glob("*.csv"))
        print(f"📂 Found {len(csv_files)} CSV file(s)")
        return csv_files
    
    def parse_date(self, date_str):
        """Parse date string to datetime object."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            return datetime.min  # Return minimum date if parsing fails
    
    def read_csv_file(self, filepath):
        """
        Read a CSV file and return records as list of dicts.
        Handles different column orders and malformed rows.
        """
        records = []
        
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Check if file is empty
                if reader.fieldnames is None:
                    self.stats["errors"].append(f"{filepath.name}: Empty file")
                    return records
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Validate required fields exist
                        if self.dedupe_field not in row:
                            raise ValueError(f"Missing {self.dedupe_field} field")
                        if self.date_field not in row:
                            raise ValueError(f"Missing {self.date_field} field")
                        
                        records.append(row)
                    except Exception as e:
                        self.stats["errors"].append(
                            f"{filepath.name}:{row_num}: {str(e)}"
                        )
            
            print(f"  ✓ {filepath.name}: {len(records)} records")
            
        except Exception as e:
            self.stats["errors"].append(f"{filepath.name}: {str(e)}")
            print(f"  ✗ {filepath.name}: Error - {str(e)}")
        
        return records
    
    def merge_and_deduplicate(self, all_records):
        """
        Merge records and remove duplicates based on dedupe_field.
        Keeps the most recent entry based on date_field.
        """
        # Dictionary to store best record for each unique identifier
        unique_records = {}
        
        for record in all_records:
            # Get identifier (case-insensitive for email)
            identifier = record[self.dedupe_field].lower().strip()
            
            # Parse date
            record_date = self.parse_date(record.get(self.date_field, ""))
            
            # Keep record if new or more recent than existing
            if identifier not in unique_records:
                unique_records[identifier] = record
            else:
                existing_date = self.parse_date(
                    unique_records[identifier].get(self.date_field, "")
                )
                if record_date > existing_date:
                    unique_records[identifier] = record
        
        return list(unique_records.values())
    
    def sort_records(self, records, sort_field="username"):
        """Sort records by specified field."""
        return sorted(records, key=lambda x: x.get(sort_field, "").lower())
    
    def write_output(self, records, fieldnames):
        """Write deduplicated records to output file."""
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
            print(f"\n✅ Wrote {len(records)} records to {self.output_file}")
        except Exception as e:
            print(f"❌ Error writing output: {str(e)}")
            self.stats["errors"].append(f"Output write error: {str(e)}")
    
    def generate_report(self):
        """Generate and save processing report."""
        report_file = Path("merge_report.txt")
        
        report_lines = [
            "=" * 60,
            "CSV MERGE & DEDUPLICATION REPORT",
            "=" * 60,
            f"Input Directory: {self.input_dir}",
            f"Output File: {self.output_file}",
            f"Deduplication Field: {self.dedupe_field}",
            "",
            "STATISTICS:",
            "-" * 60,
            f"Files Processed: {self.stats['files_processed']}",
            f"Total Records Found: {self.stats['total_records']}",
            f"Duplicates Removed: {self.stats['duplicates_removed']}",
            f"Final Record Count: {self.stats['final_count']}",
            "",
        ]
        
        if self.stats["errors"]:
            report_lines.extend([
                "ERRORS/WARNINGS:",
                "-" * 60,
            ])
            for error in self.stats["errors"]:
                report_lines.append(f"  • {error}")
        else:
            report_lines.append("No errors encountered ✓")
        
        report_lines.append("=" * 60)
        
        report_content = "\n".join(report_lines)
        report_file.write_text(report_content)
        
        print("\n" + report_content)
        print(f"\n📄 Report saved to {report_file}")
    
    def process(self):
        """Main processing pipeline."""
        print("=" * 60)
        print("CSV MERGER & DEDUPLICATOR")
        print("=" * 60)
        print()
        
        # Find CSV files
        csv_files = self.find_csv_files()
        if not csv_files:
            print("No CSV files found!")
            return
        
        print()
        
        # Read all files
        all_records = []
        fieldnames_set = set()
        
        for csv_file in csv_files:
            records = self.read_csv_file(csv_file)
            if records:
                all_records.extend(records)
                # Collect all fieldnames
                fieldnames_set.update(records[0].keys())
                self.stats["files_processed"] += 1
        
        self.stats["total_records"] = len(all_records)
        
        if not all_records:
            print("\n❌ No valid records found!")
            return
        
        # Ensure consistent fieldnames
        fieldnames = sorted(fieldnames_set)
        
        # Merge and deduplicate
        print(f"\n🔄 Merging and deduplicating...")
        unique_records = self.merge_and_deduplicate(all_records)
        self.stats["duplicates_removed"] = len(all_records) - len(unique_records)
        
        # Sort by username
        print(f"📊 Sorting by username...")
        sorted_records = self.sort_records(unique_records, "username")
        self.stats["final_count"] = len(sorted_records)
        
        # Write output
        self.write_output(sorted_records, fieldnames)
        
        # Generate report
        self.generate_report()
    
    def cleanup(self):
        """Delete all generated files."""
        print("\n" + "=" * 60)
        print("CLEANUP")
        print("=" * 60)
        
        input("\nPress Enter to delete all generated files...")
        
        # Delete CSV files in input directory
        if self.input_dir.exists():
            for csv_file in self.input_dir.glob("*.csv"):
                csv_file.unlink()
                print(f"🗑️  Deleted {csv_file}")
            
            # Remove directory if empty
            try:
                self.input_dir.rmdir()
                print(f"🗑️  Deleted directory {self.input_dir}")
            except OSError:
                print(f"⚠️  Directory {self.input_dir} not empty, keeping it")
        
        # Delete output files
        for file in [self.output_file, Path("merge_report.txt")]:
            if file.exists():
                file.unlink()
                print(f"🗑️  Deleted {file}")
        
        print("\n✅ Cleanup complete!")


def main():
    """Main entry point."""
    # Configuration
    input_dir = "csv_data"
    output_file = "merged_users.csv"
    
    # Create merger instance
    merger = CSVMerger(
        input_dir=input_dir,
        output_file=output_file,
        dedupe_field="email",
        date_field="signup_date"
    )
    
    # Setup sample data (comment this out if you have your own CSV files)
    merger.setup_sample_data()
    
    # Process files
    merger.process()
    
    # Cleanup (optional)
    merger.cleanup()


if __name__ == "__main__":
    main()