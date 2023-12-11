import os
import logging
import argparse
from datetime import datetime
import time
import shutil
import sys

def setup_logging(log_file):
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def sync_folders(source, replica):
    if not os.path.exists(source):
        logging.error(f"Source Folder not Found: {source}")
        return

    try:
        shutil.rmtree(replica)
        shutil.copytree(source, replica)
        logging.info(f"Folder synchronization complete: {source} -> {replica}")
    except Exception as e:
        logging.error(f"Error during synchronization: {e}")

def periodic_sync(source_folder, replica_folder):
    logging.info("Starting periodic synchronization...")
    sync_folders(source_folder, replica_folder)
    logging.info("Periodic synchronization complete.")

def main():
    parser = argparse.ArgumentParser(description="One-way periodic synchronization script.")
    parser.add_argument("source_folder", help="Path to the source folder.")
    parser.add_argument("replica_folder", help="Path to the replica folder.")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds.")
    parser.add_argument("log_file", help="Path to the log file.")

    args = parser.parse_args()

    source_folder = os.path.abspath(args.source_folder)
    replica_folder = os.path.abspath(args.replica_folder)
    interval = args.interval
    log_file = args.log_file

    # Print paths to source and replica folders
    print(f"Source Folder: {source_folder}")
    print(f"Replica Folder: {replica_folder}")

    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder not found: {source_folder}")
        sys.exit(1)  # Exit the script if the source folder is not found

    # Set up logging
    setup_logging(log_file)

    # Initial synchronization
    sync_folders(source_folder, replica_folder)

    # Run periodic synchronization in a loop
    while True:
        periodic_sync(source_folder, replica_folder)
        time.sleep(interval)

if __name__ == "__main__":
    main()