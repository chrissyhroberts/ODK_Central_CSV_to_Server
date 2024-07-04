# ODK_Central_CSV_to_Server
Sends data from a CSV file to an ODK Central project

## Overview

* Create an XLSForm (test.xls) and add it to your Central server
* Go to KoBoToolbox, upload your form, deploy and then change the URL to finish **/json**
* This will show the json file. Copy it and save to i.e. **/test.json**
* Run **01_read_and_print_json.py** which will create an empty csv file **test.csv** that you'll populate with data
  * python3.11 01_read_and_print_json.py jsonfile outputcsvfile```
    * ```python3.11 01_read_and_print_json.py test.json test.csv```
* Enter your data and save the csv file as something like **input_data.csv**
* Run **02_parse_csv_to_xmls.py** to transcode lines of the csv file to xml submission files for Central
  * python3.11 02_parse_csv_to_xmls.py input_data.csv formid version
    * ```python3.11 02_parse_csv_to_xmls.py input_data.csv "test" "20240704101524"```
* Update **credentials.txt** to match your central server credentials
* Run **03_submit_to_Central.py** to submit all xml files to the server
  * python3.11 03_submit_to_Central.py projectid formid version credentials
    * ```python3.11 03_submit_to_Central.py 138 "test" "20240704101524" "credentials.txt"```
