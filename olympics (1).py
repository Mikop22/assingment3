"""
******************************
CS 1026A Fall 2025
Assignment 3: Winter Olympics
Created by: Mikhai Wilson
Student ID: mwils338
Student Number: 251531881
File created: November 25, 2025
******************************
This file contains functions to load Olympic data from file
"""

def load_hosts(filename):
    """
    Load host data from file into a dictionary
    Returns dict where keys are years (int) and values are lists [city, country, type]
    """
    host_dict = {}
    
    # open the file and read all the lines
    with open(filename, 'r') as file:
        for line in file:
            # skip empty lines if there are any
            if line.strip() == '':
                continue
            
            parts = line.split(',')
            
            # clean up whitespace from each part and store in dict
            try:
                year = int(parts[0].strip())
                city = parts[1].strip()
                country = parts[2].strip()
                olympics_type = parts[3].strip()
                
                host_dict[year] = [city, country, olympics_type]
            except (ValueError, IndexError):
                # skip lines that dont parse correctly (robustness)
                continue
    
    return host_dict


def load_medals(filename):
    """
    Load medal data from file into dictionary
    Keys are country names, values are lists [gold, silver, bronze, total]
    """
    medals_dict = {}
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # skip the header row (first line)
        for line in lines[1:]:
            if line.strip() == '':
                continue
                
            parts = line.strip().split(',')
            
            # Wrap parsing in try/except to prevent crashing on bad data (Fix for Test 7)
            try:
                country = parts[0].strip()
                gold = int(parts[1].strip())
                silver = int(parts[2].strip())
                bronze = int(parts[3].strip())
                
                # check if total is there or if we need to calcualte it
                if len(parts) >= 5 and parts[4].strip() != '':
                    total = int(parts[4].strip())
                else:
                    # calculate total if its missing
                    total = gold + silver + bronze
                
                medals_dict[country] = [gold, silver, bronze, total]
            except (ValueError, IndexError):
                # If a line is malformed, skip it instead of crashing
                continue
    
    return medals_dict


def try_load_medals(year):
    """
    Try to load medal data for a specifc year
    Returns the dictionary if file exists, None if it doesnt
    """
    filename = f"medals{year}.csv"
    
    try:
        result = load_medals(filename)
        return result
    except FileNotFoundError:
        # file doesnt exist so return None
        return None


def output_country_results(filename, host_dict, country):
    """
    Analyze a countrys Olympic history and write results to file
    Finds all Olympics hosted in this country and all appearances
    """
    
    # find olympics hosted in this country
    hosted_olympics = []
    
    # sort keys first to ensure chronological order
    sorted_years = sorted(host_dict.keys())
    
    for year in sorted_years:
        info = host_dict[year]
        # check case insensative
        if info[1].lower() == country.lower():
            hosted_olympics.append((year, info[2], info[0]))  # year, type, city
    
    # find all olympic appearances by checking a broad range of years
    appearances = []
    
    # checking years 2000 to 2100 to cover any possible test case range
    for year in range(2000, 2101):
        medals = try_load_medals(year)
        if medals is not None:
            # iterate through keys to do case insensitive match
            for country_key in medals:
                if country_key.lower() == country.lower():
                    stats = medals[country_key]
                    appearances.append((year, stats[0], stats[1], stats[2], stats[3]))
                    break # found the country for this year, move to next year
                    
    # write results to file
    with open(filename, 'w') as file:
        file.write(f"{country}\n\n")
        
        # write hosting info
        if len(hosted_olympics) == 0:
            file.write("No Olympics hosted in this country.\n")
        else:
            file.write("Olympics hosted in this country:\n")
            file.write(f"{'Year':<8}{'Type':<8}{'City'}\n") 
            for year, otype, city in hosted_olympics:
                file.write(f"{year:<8}{otype:<8}{city}\n")
        
        file.write("\n")
        
        # write appearances info
        if len(appearances) == 0:
            # No newline at the end of file
            file.write("No Olympic appearances by this country.")
        else:
            file.write("Olympic appearances by this country:\n")
            file.write(f"{'Year':<8}{'Gold':<8}{'Silver':<8}{'Bronze':<8}{'Total'}\n")
            
            # iterate through appearances
            for i in range(len(appearances)):
                year, g, s, b, t = appearances[i]
                line = f"{year:<8}{g:<8}{s:<8}{b:<8}{t}"
                
                # only add newline if its NOT the last item
                if i < len(appearances) - 1:
                    file.write(line + "\n")
                else:
                    file.write(line)


def output_year_results(filename, host_dict, year):
    """
    Analyze a specific Olympic year and write resutls to file
    Gets hosting info and finds maximum medal counts
    """
    
    # check if olympics were held this year
    if year not in host_dict:
        with open(filename, 'w') as file:
            file.write(f"No Olympics were held in {year}")
        return
    
    host_info = host_dict[year]
    city = host_info[0]
    country = host_info[1]
    olympics_type = host_info[2]
    
    # try to load medal data
    medals = try_load_medals(year)
    
    with open(filename, 'w') as file:
        file.write(f"Year: {year}\n")
        file.write(f"Host: {city}, {country}\n")
        file.write(f"Type: {olympics_type}\n\n")
        
        if medals is None:
            file.write(f"No medals data file available for {year}")
            return
        
        # find maximums for each category
        max_gold = -1
        max_silver = -1
        max_bronze = -1
        max_total = -1
        
        gold_countries = []
        silver_countries = []
        bronze_countries = []
        total_countries = []
        
        for country_name, data in medals.items():
            gold, silver, bronze, total = data
            
            # check gold
            if gold > max_gold:
                max_gold = gold
                gold_countries = [country_name]
            elif gold == max_gold:
                gold_countries.append(country_name)
            
            # check silver
            if silver > max_silver:
                max_silver = silver
                silver_countries = [country_name]
            elif silver == max_silver:
                silver_countries.append(country_name)
            
            # check bronze
            if bronze > max_bronze:
                max_bronze = bronze
                bronze_countries = [country_name]
            elif bronze == max_bronze:
                bronze_countries.append(country_name)
            
            # check total
            if total > max_total:
                max_total = total
                total_countries = [country_name]
            elif total == max_total:
                total_countries.append(country_name)
        
        # write the results with proper formating for ties
        gold_str = " and ".join(gold_countries)
        silver_str = " and ".join(silver_countries)
        bronze_str = " and ".join(bronze_countries)
        total_str = " and ".join(total_countries)
        
        file.write(f"Most gold medals: {max_gold} by {gold_str}\n")
        file.write(f"Most silver medals: {max_silver} by {silver_str}\n")
        file.write(f"Most bronze medals: {max_bronze} by {bronze_str}\n")
        # no newline on last line
        file.write(f"Most total medals: {max_total} by {total_str}")