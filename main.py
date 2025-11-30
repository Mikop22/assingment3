"""
******************************
CS 1026A Fall 2025
Assignment 3: Winter Olympics
Created by: Mikhai Wilson
Student ID: mwils338
Student Number: 251531881
File created: November 25, 2025
******************************
This file contains the user interface and comand system
"""
from olympics import *


def parse_command(text, host_dict):
    """
    Parse and execute user commands
    Commands must have exactly 3 parts: command type, parameter, and output filename
    No exception catching
    """
    
    # strip the leading/trailing whitespace
    text = text.strip()
    
    # split the command into parts in order to handle quoted strings for country names
    # First check if we have a quoted string (for country command)
    if "'" in text:
        # Find the first quote and last quote place 
        first_quote = text.find("'")
        last_quote = text.rfind("'")
        
        # Make sure we have a valid pair of quotes
        if first_quote != last_quote:
            # Get command (everything before the first quote)
            before_quote = text[:first_quote].strip().split()
            # Get the quoted part (including quotes)
            quoted_part = text[first_quote:last_quote+1]
            # Get everything after the last quote
            after_quote = text[last_quote+1:].strip().split()
            
            #Should be exactly: command before, quoted string, filename after
            if len(before_quote) != 1 or len(after_quote) != 1:
                raise ValueError("Incorrect command parameters")
            
            command = before_quote[0].lower()
            parameter = quoted_part
            output_filename = after_quote[0]
        else:
            raise ValueError("Incorrect command parameters")
    else:
        # No quotes so split normally (for year command)
        parts = text.split()
        
        # check that we have exactly 3 parts
        if len(parts) != 3:
            raise ValueError("Incorrect command parameters")
        
        command = parts[0].lower()
        parameter = parts[1]
        output_filename = parts[2]
    
    # validate the command type
    if command != 'year' and command != 'country':
        raise ValueError("Unknown command")
    
    # validate filename ends with .txt
    if not output_filename.endswith('.txt'):
        raise ValueError("Invalid filename")
    
    # execute the apropriate command
    if command == 'year':
        try:
            year = int(parameter)
        except ValueError:
            raise ValueError("Incorrect command parameters")
            
        output_year_results(output_filename, host_dict, year)
        
    elif command == 'country':
        # country name must be surrunded by single quotes
        if not (parameter.startswith("'") and parameter.endswith("'")):
            raise ValueError("Incorrect command parameters")
            
        # remove quotes from country name
        country_name = parameter[1:-1]  # Remove first and last quote
        output_country_results(output_filename, host_dict, country_name)


def command_system():
    """
    Main interactive command loop
    Prompts for host file first, then enters command loop
    to catch exceptions from parse_command
    """
    
    host_dict = None
    
    # keep prompting until we get a valid host file
    while not host_dict:
        filename = input("Enter host filename:").strip()
        
        try:
            host_dict = load_hosts(filename)
            # if we got a dict, but it's empty, treat it as invalid format
            if not host_dict:
                print("Incorrect host file format")
        except FileNotFoundError:
            print("Invalid host filename")
        except (ValueError, IndexError):
            print("Incorrect host file format")
    
    # main command loop
    while True:
        command = input("Enter a valid command")
        
        # check for quit command (case insensative)
        if command.strip().lower() == 'quit':
            break
        
        # try to parse and execute the command
        try:
            parse_command(command, host_dict)
        except ValueError as e:
            # print the error message and continue
            print(e)

