from pathlib import Path

log_file = Path("server.log")
summary_file = Path("summary.txt")

log_content = """2024-10-15 10:23:45 INFO Server started
2024-10-15 10:24:12 ERROR Database connection failed
2024-10-15 10:24:15 WARNING Retrying connection
2024-10-15 10:24:20 INFO Connection established
2024-10-15 10:25:33 ERROR Timeout on request
2024-10-15 10:26:01 INFO Request completed"""

log_file.write_text(log_content)
print(f"Created {log_file}\n")


# ============================================
# MAIN PROGRAM: Analyze logs
# ============================================
print("=" * 50)
print("LOG FILE ANALYZER")
print("=" * 50)

if not log_file.exists():
    print(f"Error: {log_file} not found!")
    exit()

log_counts = {
    "ERROR" : 0,
    "WARNING": 0,
    "INFO":0
}
error_lines = []

print(f"Reading {log_file} ...")
with open(log_file, "r") as file:
    for line in file:
        line = line.upper()
        if "ERROR" in line:
            log_counts["ERROR"] = log_counts.get("ERROR", 0) + 1
        elif "WARNING" in line:
            log_counts["WARNING"] = log_counts.get("WARNING", 0) + 1
        elif "INFO" in line:
            log_counts["INFO"] = log_counts.get("INFO", 0) + 1

print(f"Writing summary to {summary_file}...")
with open(summary_file, "w") as file:
    file.write("Log File Analysis Summary \n")
    file.write("=" * 30 + "\n")
    for level, count in log_counts.items():
        file.write(f"{level}: {count}\n")
    file.write("=" * 30 + "\n")
    file.write(f"Total log entries: {sum(log_counts.values())}\n")



print(f"Contents of {summary_file}:")
print(summary_file.read_text())

# ============================================
# CLEANUP: Delete all created files
# ============================================
print("=" * 50)
print("CLEANUP")
print("=" * 50)

files_to_delete = [log_file, summary_file]
for file in files_to_delete:
    if file.exists():
        file.unlink()
        print(f"Deleted {file}")

print("\nCleanup complete! All files removed.")