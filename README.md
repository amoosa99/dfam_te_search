# Dfam RepeatModeler Transposable Element Search

Description

A web-based tool that allows a user to navigate transposable element data from Dfam's RepeatModeler program. The data is stored in a mySQL database and is accessed using a webpage. The database is already populated with transposable element data for Uraeginthus cyancephalus, and more data can be added using an included script.


Requirements

Apache2 Server - This tool was designed to run on an Apache2 HTTP web server. It may work on other types of web servers but it is not guaranteed.

Python 3 - The back-end code for this tool is written in Python 3. This project was tested and developed using Python 3.6.9, but later Python 3 versions will most likely work. 

MySQL Server - This tool relies on a MySQL database to store the transposable element data.

Mozilla Firefox - This project was developed and tested using Firefox 87.0. Other browsers may work but have not been validated.

JavaScript supported and enabled – This project uses AJAX for its interactive features, so JavaScript must be enabled in the browser for it to work properly.


Setup

1. Place all files on the Apache server. Make sure that the directory that the files are in is configured to execute CGI scripts.

2. Navigate to the 'setup' folder in the tool's directory.

3. Install all required Python libraries listed in requirements.txt.

4. Set MySQL server login credentials using the set_config.py script.
 
5. Run the create_db.py script to create the MySQL database. It will be named 'tedb'.


To upload Dfam RepeatModeler Data to the Database:

Transposable element data for U. cyanocephalus is available with this project’s source code at ‘setup/data/uraCya_rm2.45.fasta’. This and other Dfam RepeatModeler output files can be found at https://dfam.org/repository.

1. Download and get the path of the FASTA RepeatModeler output file.

2. Run the upload_te.py script using the FASTA file's path as the input (-i) parameter and the genus and 	species of the organism as the -g and -s parameters, respectively.

3. When the script terminates, the data will be added to the mySQL database and can be accessed.


Accessing the webpage to search the database

1. Navigate to the 'search.html' script on the Apache server in Firefox using its virtual filepath. 

2. Type in the name of a Dfam element type or family. A link is provided on the webpage to Dfam's classification site to find the different element types and families.

3. (Optional) Type in a DNA sequence to narrow down the results. The webpage will search for elements that match both the type/family and the sequence that are inputted.

4. To search only by sequence, leave the type/family field blank and simply type in a sequence.

5. Click ‘Submit’ to view results in the web browser. Click ‘Download’ to send the results to a FASTA file. Note that both ‘Submit’ and ‘Download’ give results based on what is typed into the search boxes.
