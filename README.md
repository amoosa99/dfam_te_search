# Dfam RepeatModeler Transposable Element Search

Description

A web-based tool that allows a user to navigate transposable element data from Dfam's RepeatModeler program (https://www.dfam.org/repository). The data is stored in a mySQL database and is accessed using a web browser. The project comes with transposable element data for Uraeginthus cyancephalus, and more data can be added using an included script.


Requirements

Linux OS - The instructions given here use Ubuntu 18.04. The commands and file
paths will likely be different when using a different OS.

Apache2 Server - This tool was designed to run on an Apache2 HTTP web server. It may work on other types of web servers but it is not guaranteed.

Python 3 - The back-end code for this tool is written in Python 3. This project was tested and developed using Python 3.6.9, but later Python 3 versions will most likely work. 

MySQL Server - This tool relies on a MySQL database to store the transposable element data.

Mozilla Firefox - This project was developed and tested using Firefox 87.0. Other browsers may work but have not been validated.

JavaScript supported and enabled – This project uses AJAX for its interactive features, so JavaScript must be enabled in the browser for it to work properly.


Set Up Apache2 server

1. If this is not already done, configure the /var/www/html directory to run
   CGI scripts. Do this as follows:

	a. Use the command 'sudo a2enmod cgi'.

	b. Add the following text to the apache2 configuration file
           (/etc/apache2/apache2.conf):

		<Directory /var/www/html/>
			Options +ExecCGI
			AddHandler cgi-script .cgi .py
		</Directory>

	c. Restart Apache with 'sudo systemctl restart apache2'

2. Give yourself ownership over the /var/www/html directory with
   'sudo chown -r [your_username] .' replacing [your_username] with your
   system username.

3. Set permissions of /var/www/html with 'chmod -r 755 .' to ensure that 
   you have permission to write files to this directory while others do not.

4. Place all files in the /var/www/html directory.


Setting up MySQL Server

1. Use 'mysql_secure_installation' to begin setup. 

2. Create a root password for the MySQL database. Your username will be "root"
   and your password will be the one you created.

3. Answer yes to all other prompts to complete setup. 


Creating the Python Virtual Environment

1. Navigate to the project directory.  

2. Install python3-venv. 

3. Use the command 'python3 -m venv venv' to create a virtual environment
   called 'venv' inside the project directory. 

4. Activate the virtual environment using 'source ./venv/bin/activate'

5. Install required packages using 'pip3 install -r requirements.txt'

6. Use 'deactivate' to exit the virtual environment.


Creating the Transposable Element Database

1. Navigate to the 'setup' folder in the project directory.

2. Run the script 'set_config.py' and enter your MySQL username and password
   that were set up earlier. If the steps earlier were followed, the username
   should be "root" and the password should be the one set during MySQL setup.

3. Run the script 'create_db.py' to set up the MySQL database.

4. The 'upload_te.py' script can be used to populate the database with FASTA
   data from the Dfam RepeatModeler. This script requires an input file along
   with the genus and species of the organism that the data is from.

   To upload the included data, use the following command:

	
   command './upload_te.py -i ./data/uraCya_rm2.45.fasta -g Uraeginthus
            -s cyanocephalus'



Accessing the Search Tool

1. Open a web browser and navigate to:

	'localhost:80/dfam_te_search-1.1/search.html'

2. Searches can now be done by element type, element family, or sequence. 
   Beginning to type an element type or family will return an autocomplete
   list of elements in the database that match.


Example Searches using the Included Dataset

These searches assume that you are only using the included sample data.
The number of results will vary if you have more data in the database.

1. Type "LI" in the 'Search by type/family' box and leave the "Search by
   sequence" box blank. The autocomplete should suggest "LINE". Click on 
   that and then click "Search". The table should populate with 16 results.

2. Type "ERV" in the 'Search by type/family' box and leave the "Search by 
   sequence" box blank. The autocomplete should give several suggestions.
   Click on "ERV2" and click search. You should get 23 results. 

   Type "GTTGAC" in the "Search by sequence" box. Leave "ERV2" in the 
   "Search by type/family" box. Click "Search" to filter the results
   to ones containing the inputted sequence. Only 1 result should be returned. 

3. Leave the "Search by type/family" box blank and type "AAGTC" in the 
   "Search by sequence" box. Click "Search" to find elements that contain
   this sequence. This should return 24 results.
