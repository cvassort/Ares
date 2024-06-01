import argparse
import os
import datetime
from script.scanner import scan_target
from script.web_tests import run_security_tests
from script.report_generator import generate_report



def main():
    parser = argparse.ArgumentParser(description='Automated security testing tool.')
    parser.add_argument('targets', metavar='T', type=str, nargs='+', help='IP or domain to scan')
    args = parser.parse_args()

    for target in args.targets:
        date_now = datetime.datetime.now().strftime("%d-%m-%Y")
        folder_name = f"{target}_{date_now}"
        folder_path = os.path.join("results", folder_name)
        os.makedirs(folder_path, exist_ok=True )
        print(f"Scanning {target}")
        scan_target(target, folder_path)
        run_security_tests(target, folder_path)
        # generate_report(target, folder_path)

if __name__ == "__main__":
    main()
