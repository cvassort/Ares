import os 
import csv
import re

def parser(target, folder_path):
    print("This is a parser function")
    
    
    
    
  
def parser(target, folder_path):
  print("This is a parser function")
  
  def parse_nmap_output(target, folder_path):
    nmap_folder_path = os.path.join(folder_path, 'nmap')
    nmap_file_path = os.path.join(nmap_folder_path, f'{target}_nmap.txt')
    with open(nmap_file_path, 'r') as nmap_file:
      nmap_output = nmap_file.read()
    return nmap_output
  
  nmap_output = parse_nmap_output(target, folder_path)
  
  # Parse the nmap output and extract the relevant information
  # Here is an example of how you can extract the port, state, and service information
  port_state_service = re.findall(r'(\d+)/\w+\s+(\w+)\s+(\w+)', nmap_output)
  
  # Save the extracted information in a CSV file
  csv_file_path = os.path.join(folder_path, f'{target}_nmap.csv')
  with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Port', 'State', 'Service'])
    writer.writerows(port_state_service)
  
  return csv_file_path