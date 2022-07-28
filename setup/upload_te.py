#!/usr/bin/env python3

import re
import sys
import getopt
import configparser
import mysql.connector

"""A script that parses FASTA output files from Dfam RepeatModeler and
uploads the information to a mySQL database"""

#gets organism and input file name and then parses FASTA
def main(argv):

	input_file = ''
	genus = ''
	species = ''
	
	#takes input file and organism from CLI argument
	try:
		opts, args = getopt.getopt(argv,"i:g:s:",
					   ["input=","genus=","species="])


	#exits if arguments cannot be read or is missing
	except getopt.GetoptError:
		print("Invalid argument(s)")  

	#sets input file and organism from arguments 
	for opt, arg in opts:
		if opt in ("-i","--input"):
			input_file = arg
		elif opt in ("-g","--genus"):
			genus = arg
		elif opt in ("-s","--species"):
			species = arg
		else:
			sys.exit()

	#if input or organism are not found, then exit
	if not input_file or not genus or not species:

		if not input_file:
			print("Input file (-i/--input) not entered")
		if not genus:
			print("Organism genus (-g/--genus) not entered")
		if not species:
			print("Organism species (-s/--species not entered")
		
		sys.exit()

	#gets sequence information from FASTA file
	db_dicts = parse_fasta_info(input_file)	
	
	#uploads sequence information into database
	upload_to_db(db_dicts, genus, species)

#gets sequence, organism, element type/family, and sequence
def parse_fasta_info(file_path):

	#reads in file
	fasta = open(file_path,"r")

	#list of FASTA entries
	entries = []

	line = fasta.readline()

	while line:

		#remove newline
		line = line.rstrip()

		#pattern for header line	
		header_pattern = r">([^#]+)#(\w+)/?(\w*)"

		#match pattern in line
		header_match = re.search(header_pattern, line)

		#if line is a header line
		if header_match:

			#dictionary containing entry information
			entry_dict = {}

			#adds sequence and organism identifiers
			entry_dict['seq_id'] = header_match.group(1)

			#adds element type
			entry_dict['elem_type'] = header_match.group(2)

			#adds last non-null group as element family
			#this will be the same as type if family not present
			for group in header_match.groups()[::-1]:

				if group is not None:

					entry_dict['elem_fam'] = group
					break

			#gets sequence from the next lines
			seq_lines = []
			line = fasta.readline()
			while line and not line.startswith(">"):

				seq_lines.append(line)
				line = fasta.readline()

			#adds sequence to dictionary
			entry_dict['seq'] = "".join(seq_lines)

			#adds dictionary to list
			entries.append(entry_dict)
	
		#skip other lines
		else:
			
			line = fasta.readline()

		
	#closes file
	fasta.close()	

	return entries

#sends dictionaries containing TE data to database
def upload_to_db(db_dicts, genus, species):

    #gets MySQL username and password from config file
    parser = configparser.ConfigParser()
    parser.read("config.txt")
    username = parser.get("config", "username")
    pswd = parser.get("config", "pswd")

    #creates connection to mySQL database
    conn = mysql.connector.connect(user=username,
	 			   password=pswd,
				   host='localhost', database='tedb')

    #gets organism ID
    org_id = get_org_id(conn, genus, species)	

    #loops through data entries and attempts to add them to the database
    for entry in db_dicts:

	#creates cursor
        cursor = conn.cursor()

	#gets element ID
        elem_id = get_elem_id(conn, entry['elem_type'], entry['elem_fam'])

	#SQL query
        qry = """INSERT INTO sequences(seq_id, seq, elem_id, org_id)
		 VALUES(%s, %s, %s, %s)"""

	#adds sequence to database
        cursor.execute(qry, (entry['seq_id'], entry['seq'], elem_id, org_id))

	#closes cursor
        cursor.close()

    #commits changes
    conn.commit()

    #closes database connection
    conn.close()

#gets

#retrieves organism ID
#if organism is not in database, adds it
def get_org_id(conn, genus, species):

	#attempts to insert organism into database
	#if organism is already in database, it will not be added
	cursor = conn.cursor()
	qry = """INSERT IGNORE INTO organisms(genus, species)
		 VALUES(%s, %s)"""
	cursor.execute(qry, (genus, species))
	conn.commit()
	cursor.close()

	#gets organism ID
	cursor = conn.cursor(buffered=True)
	qry = """SELECT o.org_id
		 FROM organisms o
		 WHERE o.genus = %s AND o.species = %s"""
	cursor.execute(qry, (genus,species))
	org_id = cursor.fetchone()[0]
	cursor.close()

	#returns organism ID
	return org_id
	
#gets element family ID
#if element family is not in database, it is added
def get_elem_id(conn, elem_type, family):

	#attempts to insert element family into database
	#if element family is a duplicate, it will not be added
	cursor = conn.cursor(buffered=True)
	qry = """INSERT IGNORE INTO elements(type, fam)
		 VALUES(%s, %s)"""
	cursor.execute(qry, (elem_type, family))
	conn.commit()
	cursor.close()

	#gets element family ID
	cursor = conn.cursor(buffered=True)
	qry = """SELECT e.elem_id
		 FROM elements e
		 WHERE e.type = %s AND e.fam = %s"""
	cursor.execute(qry, (elem_type,family))
	elem_id = cursor.fetchone()[0]
	cursor.close()

	#returns element family ID
	return elem_id


if __name__ == "__main__":

	main(sys.argv[1:])
