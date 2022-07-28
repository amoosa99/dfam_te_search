#!/usr/bin/env python3

import cgi, json
import os
import mysql.connector

"""A CGI script that searches a transposable element database to autocomplete
element name searches in an HTML form. Limits results to five to prevent
long search suggestion lists"""

def main():

    print("Content-Type: application/json\n\n")

    #gets form data
    form = cgi.FieldStorage()
    term = form.getvalue('search_term')

    #checks for blank term and formats them for SQL query
    term = process_term(term)

    #queries database for matching TEs
    results = query_db(term)

    #prints the matches in JSON format
    print(json.dumps(results))

#formats search terms for SQL query
def process_term(term):

	#checks for blank inputs 
	if term is None:
		term = "" 

	#formats inputs for SQL query
	term = "%" + term + "%"

	return term

#queries TE database for elements that match the searched type or family
def query_db(term):

    #gets MySQL username and password from config file
    parser = configparser.ConfigParser()
    parser.read("./setup/config.txt")
    username = parser.get("config", "username")
    pswd = parser.get("config", "pswd")

    #creates connection to mySQL database
    conn = mysql.connector.connect(user=username,
	 			   password=pswd,
				   host='localhost', database='tedb')

    #cursors for checking types and families
    curs = conn.cursor(buffered=True)
    
    #results of the queries
    results = []

    #queries the database for element types that match term
    qry = """
	SELECT e.type AS elem_type, e.type LIKE %s AS type_found,
	       e.fam AS family, e.fam LIKE %s AS fam_found
	FROM elements e
	WHERE e.type LIKE %s OR e.fam LIKE %s
    """
    curs.execute(qry, (term, term, term, term))

    #a list to keep track of results found to prevent duplicates
    result_list = []

    #adds matches to results
    for (elem_type, type_found, family, fam_found) in curs:

	#if the match was to an element type
        if type_found == 1:

            #if result has not already been added
            if elem_type not in result_list: 

                results.append({'label': elem_type, \
                                           'value': elem_type})
                result_list.append(elem_type)

	#if the match was to a family of elements
        elif fam_found == 1:

            #if result has not already been seen
            if family not in result_list:

                results.append({'label': family, 'value': family})
                result_list.append(elem_type)

	#terminate when five unique results are found
        if len(results) == 5:

            break

    #closes cursors
    curs.close()

    #closes connection to the mySQL database
    conn.close()

    return results


if __name__ == '__main__':
    main()
