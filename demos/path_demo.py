from pathlib import Path

print("=" * 50)
print("PATHLIB DEMO - Learn Path Object")
print("=" * 50)

# ============================================
# 1. CREATING PATH OBJECTS
# ============================================
print("\n1️⃣ CREATING PATHS")
print("-" * 50)

# From string
file1 = Path("myfile.txt")
print(f"Simple path: {file1}")
print(f"Type: {type(file1)}")

# Current directory
current = Path(".")
print(f"Current directory: {current}")

# Absolute path
absolute = Path("/home/user/documents")
print(f"Absolute path: {absolute}")

# Home directory
home = Path.home()
print(f"Home directory: {home}")

# Current working directory
cwd = Path.cwd()
print(f"Current working directory: {cwd}")

# ============================================
# 2. JOINING PATHS (The / operator!)
# ============================================
print("\n2️⃣ JOINING PATHS")
print("-" * 50)

base = Path("projects")
## auto combine!! with Path object
project = base / "my_app" / "src" / "wow test" / "main.py"
print(f"Joined path: {project}")

# Works cross-platform! (Windows uses \, Unix uses /)
data_folder = Path("data")
log_file = data_folder / "logs" / "2024" / "server.log"
print(f"Log file path: {log_file}")

# ============================================
# 3. PATH PROPERTIES
# ============================================
print("\n3️⃣ PATH PROPERTIES")
print("-" * 50)

example = Path("/home/user/projects/app/main.py")
print(f"Full path: {example}")
print(f"Name (filename): {example.name}")
print(f"Stem (without extension): {example.stem}")
print(f"Suffix (extension): {example.suffix}")
print(f"Parent directory: {example.parent}")
print(f"Parent's parent: {example.parent.parent}")
print(f"Parts (tuple): {example.parts}")

# ============================================
# 4. CHECKING FILE/DIRECTORY STATUS
# ============================================
print("\n4️⃣ CHECKING FILE STATUS")
print("-" * 50)

# Create a test file
test_file = Path("test_demo.txt")
test_file.write_text("Hello, Path!")

print(f"Does {test_file} exist? {test_file.exists()}")
print(f"Is it a file? {test_file.is_file()}")
print(f"Is it a directory? {test_file.is_dir()}")
print(f"Is it absolute? {test_file.is_absolute()}")

# Check a directory
test_dir = Path(".")
print(f"\nDoes current dir exist? {test_dir.exists()}")
print(f"Is current dir a directory? {test_dir.is_dir()}")

# ============================================
# 5. READING & WRITING FILES
# ============================================
print("\n5️⃣ READING & WRITING FILES")
print("-" * 50)

# Write text to file
demo_file = Path("demo.txt")
demo_file.write_text("This is a demo file!\nLine 2\nLine 3")
print(f"Written to {demo_file}")

# Read text from file
content = demo_file.read_text()
print(f"Content:\n{content}")

# Read as lines
lines = demo_file.read_text().splitlines()
print(f"Number of lines: {len(lines)}")

# ============================================
# 6. CREATING DIRECTORIES
# ============================================
print("\n6️⃣ CREATING DIRECTORIES")
print("-" * 50)

# Create single directory
new_dir = Path("temp_folder")
new_dir.mkdir(exist_ok=True)  # exist_ok=True won't error if exists
print(f"Created: {new_dir}")

# Create nested directories
nested = Path("data/logs/2024/october")
nested.mkdir(parents=True, exist_ok=True)  # parents=True creates all
print(f"Created nested: {nested}")

# ============================================
# 7. LISTING FILES
# ============================================
print("\n7️⃣ LISTING FILES")
print("-" * 50)

# List all items in current directory
current_dir = Path(".")
print("Files in current directory:")
for item in current_dir.iterdir():
    if item.is_file():
        print(f"  📄 {item.name}")
    elif item.is_dir():
        print(f"  📁 {item.name}")

# Find all .txt files
print("\n.txt files:")
for txt_file in current_dir.glob("*.txt"):
    print(f"  📄 {txt_file}")

# Recursive search (** means search in subdirectories too)
print("\nAll .txt files (recursive):")
for txt_file in current_dir.glob("**/*.txt"):
    print(f"  📄 {txt_file}")

# ============================================
# 8. FILE OPERATIONS
# ============================================
print("\n8️⃣ FILE OPERATIONS")
print("-" * 50)

source = Path("demo.txt")
destination = Path("demo_copy.txt")

# Copy by reading and writing
destination.write_text(source.read_text())
print(f"Copied {source} to {destination}")

# Rename
## they are only labels, no instance
old_name = Path("demo_copy.txt")
new_name = Path("renamed_demo.txt")
old_name.rename(new_name)
## if the Path File doesnt exist(ie havent been created) - the rename is only
## renaming the label
print(f"Renamed {old_name} to {new_name}")

# Get file stats
stats = demo_file.stat()
print(f"File stats for {demo_file}:")
print(f"  Size: {stats.st_size} bytes")
print(f"  Modified time: {stats.st_mtime}")

# ============================================
# 9. DELETING FILES
# ============================================
print("\n9️⃣ DELETING FILES")
print("-" * 50)

# Delete file
if test_file.exists():
    test_file.unlink()  # unlink() = delete file
    print(f"✅ Deleted {test_file}")

if new_name.exists():
    new_name.unlink()
    print(f"✅ Deleted {new_name}")

# Delete empty directory
if new_dir.exists():
    new_dir.rmdir()  # rmdir() = delete empty directory
    print(f"✅ Deleted directory {new_dir}")

# ============================================
# 10. PRACTICAL EXAMPLE
# ============================================
print("\n🔟 PRACTICAL EXAMPLE: Log File Organizer")
print("-" * 50)

# Setup
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Create some fake log files
(logs_dir / "app.log").write_text("INFO: App started")
(logs_dir / "error.log").write_text("ERROR: Something broke")
(logs_dir / "debug.log").write_text("DEBUG: Variable x = 5")

# Process logs
print("Processing log files:")
for log_file in logs_dir.glob("*.log"):
    size = log_file.stat().st_size
    print(f"  📄 {log_file.name} ({size} bytes)")
    
    # Read and count lines
    lines = log_file.read_text().splitlines()
    print(f"     Lines: {len(lines)}")

# ============================================
# CLEANUP
# ============================================
print("\n🧹 CLEANUP")
print("-" * 50)

# Clean up demo files
for file in [demo_file, logs_dir / "app.log", logs_dir / "error.log", 
             logs_dir / "debug.log"]:
    if file.exists():
        file.unlink()

logs_dir.rmdir()

# Clean up nested directories (from innermost to outermost)
for dir_path in [Path("data/logs/2024/october"), 
                 Path("data/logs/2024"),
                 Path("data/logs"),
                 Path("data")]:
    if dir_path.exists():
        dir_path.rmdir()

print("✅ All demo files cleaned up!")

print("\n" + "=" * 50)
print("🎓 PATH STUDY SESSION COMPLETE!")
print("=" * 50)