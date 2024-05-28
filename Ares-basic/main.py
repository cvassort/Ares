
import sys
from utils.fast_scanner import scan_nmap
from utils.directory_discovery import brute_force_directories



if __name__ == '__main__':
    if __name__ == '__main__':
      target = sys.argv[1]
      fast_scan_result = scan_nmap(target)
      print("fast scan result is", fast_scan_result)
      brute_force_directories(target, './wordlist/SecLists/Discovery/Web-Content/big.txt')
      sys.exit(0)