import argparse
from pathlib import Path

def analyze_log_file(file_path: Path) -> None:
    """
    Analyze a log file for failed password attempts
    
    Args:
        file_path: Path to the log file to analyze
    """
    try:
        # Use context manager for automatic file closing
        with file_path.open('r') as log_file:
            for line_number, line in enumerate(log_file, 1):
                if "Failed password" in line:
                    print(f"[Line {line_number}] Potential Brute-Force Attack Detected: {line.strip()}")
                    
    except FileNotFoundError:
        print(f"Error: Log file not found at {file_path}")
    except IOError as e:
        print(f"Error reading file: {e}")
    except UnicodeDecodeError:
        print(f"Error: File encoding issue detected in {file_path}")

def main() -> None:
    """
    Main function to handle command-line arguments and start analysis
    """
    # Set up VS Code-friendly argument parsing
    parser = argparse.ArgumentParser(
        description="Log Monitoring Tool - Detect brute-force attacks",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "log_file",
        type=Path,
        help="Path to the log file to analyze"
    )
    
    args = parser.parse_args()
    
    # Perform the log analysis
    analyze_log_file(args.log_file)

if __name__ == "__main__":
    main()
