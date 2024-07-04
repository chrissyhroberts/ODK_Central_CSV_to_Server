import argparse
import csv
import os
import uuid
from xml.etree.ElementTree import Element, SubElement, ElementTree
from datetime import datetime

# Read CSV file
def read_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    return rows, reader.fieldnames

# Recursively build the XML structure
def build_xml_structure(parent, name, value):
    name_parts = name.split('/')
    current_field = name_parts.pop(0)
    
    # Find or create the current field element
    current_element = parent.find(current_field)
    if current_element is None:
        current_element = SubElement(parent, current_field)
    
    # If there are more name parts, continue building the structure
    if name_parts:
        build_xml_structure(current_element, "/".join(name_parts), value)
    else:
        current_element.text = value

# Create XML files from CSV data
def create_xml_files(csv_data, fieldnames, serverform, versionid):
    folder_name = "instances/"
    os.makedirs(folder_name, exist_ok=True)

    for i, row in enumerate(csv_data):
        unique_id = str(uuid.uuid4())
        root = Element("data", {
            "xmlns:jr": "http://openrosa.org/javarosa",
            "xmlns:orx": "http://openrosa.org/xforms",
            "id": serverform,
            "version": versionid
        })

        for name in fieldnames:
            value = row[name]
            build_xml_structure(root, name, value)
        
        # Add timestamp field (current timestamp)
        timestamp = SubElement(root, "timestamp")
        timestamp.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        deviceid = SubElement(root, "device_id")
        deviceid.text = unique_id.replace('-', '')
        
        meta = SubElement(root, "meta")
        instanceID = SubElement(meta, "instanceID")
        instanceID.text = f"uuid:{unique_id}"
        
        xml_filename = os.path.join(folder_name, f"uuid{unique_id}.xml")
        tree = ElementTree(root)
        tree.write(xml_filename, encoding='utf-8', xml_declaration=True)

def main():
    parser = argparse.ArgumentParser(description='Convert CSV data to individual XML files using form definition.')
    parser.add_argument('csv_filename', type=str, help='Path to the CSV file containing the data')
    parser.add_argument('serverform', type=str, help='Server form ID')
    parser.add_argument('versionid', type=str, help='Version ID')

    args = parser.parse_args()
    csv_path = args.csv_filename
    serverform = args.serverform
    versionid = args.versionid

    csv_data, fieldnames = read_csv(csv_path)
    create_xml_files(csv_data, fieldnames, serverform, versionid)

if __name__ == '__main__':
    main()

# EXAMPLE : python3.11 02_parse_csv_to_xmls.py input_data.csv "test" "20240704101524"
