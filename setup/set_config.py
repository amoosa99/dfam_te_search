#!/usr/bin/env python3

import re
import sys
import configparser
import mysql.connector

"""A script that creates a config file containing the user's
MySQL login credentials"""

#creates the config file
def set_config():

    #creates config file and adds header
    config = open("config.txt", mode="w")
    config.write("[config]\n")
    
    #gets MySQL username and password
    username = input("Enter your MySQL server username: ")
    pswd = input("Enter your MySQL server password: ")
    
    #adds credentials to config file
    config.write("username={u}\n".format(u=username))
    config.write("pswd={p}\n".format(p=pswd))

    #closes file
    config.close()

    
if __name__ == "__main__":

	set_config()
