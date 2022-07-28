#!/usr/bin/env python3

import cgi, json
import os
import mysql.connector
import textwrap

"""A CGI script that searches a transposable element database using user defined search terms from an HTML form and outputs the results in a FASTA file"""

def main():

    #gets form data
    form = cgi.FieldStorage()
    term = form.getvalue('search_term')
    seq = form.getvalue('search_seq')

    #checks for blank terms and formats them for SQL query
    term, seq = process_terms(term, seq)

    #queries database for matching TEs
    fasta = query_db(term, seq)

    print("Content-Type:text/plain\n")

    print(fasta)



#formats search terms for SQL query
def process_terms(term, seq):

	#checks for blank inputs
	if term is None:
		term = "" 
 
	if seq is None:
		seq = ""

	#formats inputs for SQL query

	term = "%" + term + "%"
	seq = "%" + seq + "%"

	return term, seq

#queries TE database for elements that match search term or sequence
def query_db(term, seq):
        
    #gets MySQL username and password from config file
    parser = configparser.ConfigParser()
    parser.read("./setup/config.txt")
    username = parser.get("config", "username")
    pswd = parser.get("config", "pswd")

    #creates connection to mySQL database
    conn = mysql.connector.connect(user=username,
	 			   password=pswd,
				   host='localhost', database='tedb')
    
    #the mysql query
    qry = """
	SELECT s.seq_id AS seq_id, s.seq AS seq, e.type AS elem_type,
               e.fam AS family, o.genus AS genus, o.species AS species
	FROM sequences s
		JOIN elements e ON s.elem_id = e.elem_id
		JOIN organisms o ON s.org_id = o.org_id
	WHERE (e.type LIKE %s OR e.fam LIKE %s)
		AND s.seq LIKE %s
    """
    cursor.execute(qry, (term, term, seq))

    #creates FASTA file for results
    fasta = ""

    for (seq_id, seq, elem_type, family, genus, species) in cursor:

	#writes sequence information as FASTA header string
        header_string = ">"+seq_id+"|"+elem_type+"/"+family+"|"+ \
                        genus+"_"+species+"\n"

        fasta += header_string

	#wraps sequence to 70 characters to comply with FASTA recommendation
        seq_strings = textwrap.wrap(seq, width=70) 

        for seq in seq_strings:

            fasta += seq+"\n"

	#newline to denote end of the sequence
        fasta += "\n"

    #closes cursor
    cursor.close()

    #closes connection to the mySQL database
    conn.close()

    return fasta

if __name__ == '__main__':
    main()
