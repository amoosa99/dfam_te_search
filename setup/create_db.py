#!/usr/bin/env python3

import re
import sys
import configparser
import mysql.connector

"""A script that creates a MySQL database for storing transposable
genomic element data"""

#creates the database
def create_db():

    #gets MySQL username and password from config file
    parser = configparser.ConfigParser()
    parser.read("config.txt")
    username = parser.get("config", "username")
    pswd = parser.get("config", "pswd")

    #creates connection to mySQL database
    conn = mysql.connector.connect(user=username,
	 			   password=pswd,
				   host='localhost')

    #creates cursor
    cursor = conn.cursor()

    #creates and selects database
    qry = """CREATE DATABASE IF NOT EXISTS tedb"""
    cursor.execute(qry)
    qry = """use tedb"""
    cursor.execute(qry)

    #creates sequences table
    qry = """CREATE TABLE IF NOT EXISTS sequences (
             seq_id VARCHAR(50) NOT NULL,
             seq TEXT NOT NULL, 
             elem_id SMALLINT NOT NULL,
             org_id SMALLINT NOT NULL,
             PRIMARY KEY(seq_id)
             )"""
    cursor.execute(qry)

    #creates elements table
    qry = """CREATE TABLE IF NOT EXISTS elements (
             elem_id SMALLINT NOT NULL AUTO_INCREMENT,
             type VARCHAR(20) NOT NULL,
             fam VARCHAR(20) NOT NULL,
             PRIMARY KEY(elem_id),
             UNIQUE(type, fam)
             )"""
    cursor.execute(qry)

    #creates organisms table
    qry = """CREATE TABLE IF NOT EXISTS organisms (
             org_id SMALLINT NOT NULL AUTO_INCREMENT,
             genus VARCHAR(50) NOT NULL, 
             species VARCHAR(50) NOT NULL,
             PRIMARY KEY(org_id),
             UNIQUE(genus, species)
             )"""
    cursor.execute(qry)

    #closes connection and cursor
    conn.close()
    cursor.close()

    
if __name__ == "__main__":

	create_db()
