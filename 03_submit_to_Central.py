import requests
import base64
import os
import argparse
import xml.etree.ElementTree as ET
import re

# Function to read credentials from a file
def read_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials

# Function to clean XML content
def clean_xml_content(xml_content):
    # Remove any invalid characters that might cause issues
    cleaned_content = re.sub(r'[^\x09\x0A\x0D\x20-\x7F]', '', xml_content)
    return cleaned_content

# Function to validate XML
def validate_xml(xml_content):
    try:
        ET.fromstring(xml_content)
        return True, None
    except ET.ParseError as e:
        return False, str(e)

# Function to submit a submission
def submit_submission(url, headers, submission_xml):
    response = requests.post(url, headers=headers, data=submission_xml.encode('utf-8'))

    if response.status_code in (200, 201):
        print(f"Successfully submitted: {submission_xml[:50]}...")
    else:
        print(f"Failed to submit: {response.status_code}, {response.text}")

def main():
    parser = argparse.ArgumentParser(description='Submit XML data to ODK Central.')
    parser.add_argument('project_id', type=int, help='Project ID')
    parser.add_argument('form_id', type=str, help='Form ID')
    parser.add_argument('form_version', type=str, help='Form version')
    parser.add_argument('credentials_file', type=str, help='Path to the credentials file')

    args = parser.parse_args()

    project_id = args.project_id
    form_id = args.form_id
    form_version = args.form_version
    credentials_file = args.credentials_file

    # Read credentials from file
    credentials = read_credentials(credentials_file)
    base_url = credentials['base_url']
    username = credentials['username']
    password = credentials['password']

    # Encode username and password in Base64 for Basic Authentication
    auth_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

    # Headers for Basic Authentication
    headers = {
        "Authorization": f"Basic {auth_credentials}",
        "Content-Type": "application/xml"
    }

    # Path to the instances folder
    folder_name = "instances/"

    # Construct the URL for submission
    submission_url = f"{base_url}/v1/projects/{project_id}/forms/{form_id}/submissions"

    # Iterate through each XML file in the instances folder and submit it
    for filename in os.listdir(folder_name):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_name, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                submission_xml = file.read()

                # Clean the XML content
                cleaned_xml = clean_xml_content(submission_xml)

                # Validate XML
                is_valid, error_message = validate_xml(cleaned_xml)
                if not is_valid:
                    print(f"Invalid XML in file {filename}: {error_message}")
                    continue

                # Submit the XML data
                submit_submission(submission_url, headers, cleaned_xml)

if __name__ == '__main__':
    main()

# EXAMPLE : python3.11 03_submit_to_Central.py 138 "test" "20240704101524" "credentials.txt"
