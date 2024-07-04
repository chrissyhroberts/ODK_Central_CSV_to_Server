import json
import argparse
import csv

# Load form definition from a JSON file
def load_form_definition(form_path):
    with open(form_path, 'r') as formfile:
        formdef = json.load(formfile)
    return formdef

# Extract 'name' attributes and their hierarchical path
def extract_names(data):
    names = []
    hierarchy = []

    def extract(d, current_prefix):
        if isinstance(d, dict):
            if 'name' in d and 'type' in d and d['type'] != 'end_group':
                new_prefix = f"{current_prefix}/{d['name']}" if current_prefix else d['name']
                names.append(new_prefix)
            if d.get('type') == 'begin_group':
                hierarchy.append(d['name'])
            for key, value in d.items():
                if isinstance(value, (dict, list)):
                    extract(value, current_prefix)
            if d.get('type') == 'end_group':
                hierarchy.pop()
        elif isinstance(d, list):
            for index, item in enumerate(d):
                new_prefix = "/".join(hierarchy)
                extract(item, new_prefix)

    extract(data, '')
    return names

# Write CSV with extracted 'name' attributes
def write_csv(names, output_path):
    headers = names

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

def main():
    parser = argparse.ArgumentParser(description='Load and export ODK form definition to CSV with name attributes.')
    parser.add_argument('json_filename', type=str, help='Path to the JSON file containing the form definition')
    parser.add_argument('csv_filename', type=str, help='Path to the CSV file to export')
    
    args = parser.parse_args()
    form_path = args.json_filename
    csv_path = args.csv_filename

    formdef = load_form_definition(form_path)
    names = extract_names(formdef['survey'])
    write_csv(names, csv_path)

if __name__ == '__main__':
    main()

#EXAMPLE : python3.11 01_read_and_print_json.py test.json test.csv