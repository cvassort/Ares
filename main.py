import argparse
import os
import datetime
from script.scanner import scan_target
from script.web_tests import run_security_tests
from script.report_generator import generate_pdf_report
import shutil

def read_targets_from_file(file_path):
    """
    Read targets from a file.

    Args:
        file_path (str): The path to the file containing the targets.

    Returns:
        list: A list of targets read from the file.

    """
    with open(file_path, 'r') as file:
        targets = [line.strip() for line in file if line.strip()]
    return targets

def main():
    """
    Entry point of the program.
    
    This function parses command line arguments, reads targets from file if provided,
    creates a folder for storing results, scans each target, copies CSS file to the folder,
    and generates a PDF report for each target.
    """
    parser = argparse.ArgumentParser(description='Automated security testing tool.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--target', type=str, help='Single IP or domain to scan')
    group.add_argument('-f', '--file', type=str, help='File containing IPs or domains to scan')
    args = parser.parse_args()

    if args.target:
        targets = [args.target]
    elif args.file:
        targets = read_targets_from_file(args.file)
    
    for target in targets:
        date_now = datetime.datetime.now().strftime("%d-%m-%Y")
        folder_name = f"{target}_{date_now}"
        folder_path = os.path.join("results", folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Scanning {target}")
        scan_target(target, folder_path)
        run_security_tests(target, folder_path)
        css_source = "./script/styles.css"
        css_dest = os.path.join(folder_path, "style.css")
        shutil.copy(css_source, css_dest)
        generate_pdf_report(target, folder_path)

if __name__ == "__main__":
    main()
