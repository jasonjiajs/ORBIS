# !/usr/bin/python
# -*- coding:utf-8 -*-

# Created by: Sixun(Bill) Tang
# Started: 09/17/2019
# Final Version: 09/24/2019
# Updated

# -------------------------------------------------------------------------------------------------------------------------------
# This Script is used to clean all the raw txt files converted from pdf files scraped from CIA website Chief of States directory
# There are 218 txt files in all
# The aim of the script is to clean all the txt files and give ideal output to be loaded into STATA
# -------------------------------------------------------------------------------------------------------------------------------



# set directory
txtPath = 'C:\\Users\\stang10\\Dropbox\\data sample\\txtstate'
outPath = 'C:\\Users\\stang10\\Dropbox\\data sample\\outtxt'

# import package
import re
import sys
import os
import os, os.path, shutil


# -------------------------------------------------------------------
# Define useful functions
# -------------------------------------------------------------------


# to judge whether the line is simply a page indicator
def is_page_line(char):
    num_count = 0
    if len(char.strip()) == 0:
        return False
    for y in char:
        if y in '1234567890':
            num_count += 1
    if ('page' in char.lower() and num_count>0) or num_count/len(char.strip())>0.9:
        return True
    else:
        return False

# judge whether a line is a country name 
def is_country(char):
    # clean all non-English character 
    char_check = ''
    for t in char:
        if t.isalpha() or t==' ':
            char_check +=t
    
    # some countries are named as ***[-]NDE
    if char.lower() in country_list or re.sub('nde$','',char_check.lower()).strip() in country_list:
        return True
    else:
        return False


# This function is used to add an item to an existing dictionary
# item is a list of tuples containing the key and the value
def add_item(item,e_dict):
    for i in item:
        key = i[0]
        value = i[1]
        if key not in e_dict:
            e_dict.update({key: value})
        elif value != e_dict[key] and value != '':
            e_dict[key] = e_dict[key] + ', ' + value   
    return e_dict

# This function is used to replace the abbreviation in a string character with the full name in a dictionary
def dict_replace(line,dict):
    line_list = line.split()
    for w in range(len(line_list)):
        item = line_list[w]
        for key in dict:
            if key in item:
                line_list[w] = re.sub(key,dict[key],item)
    
    line = ' '.join(line_list)

    # clean chracters
    line = re.sub(r'[\n]*', '', line).strip()
    line = re.sub(r'^[.]*', '', line).strip()
    return line

# This function is used to split a line into position and person name using auxiliary information and returns a useful observation
def split_line(spliter, a_dict, single_line):
    position_list = single_line.split(spliter)
    # judge the first element of the list is empty or not
    first_no = (position_list[0]!='')
    while '' in position_list: 
        position_list.remove('')
    while '\n' in position_list:
        position_list.remove('\n')
    # If a position_list has only one value, it means that neither the name or the position is missing (most of time this means no name for a position)
    if len(position_list) == 1:
        if first_no == 0:
            person_name = position_list[0]
            position = ''
        else:
            position = position_list[0]
            person_name = ''
    else:
        person_name = position_list[1].strip()
        position = position_list[0].strip()
    
    # now use a_dict to get full name
    person_name = dict_replace(person_name,a_dict)
    position = dict_replace(position,a_dict)
    
    return [person_name,position]


# ----------------------------------------------------------------
# Step 1: Preparation Files
# ----------------------------------------------------------------

# read country_list
# This file is scraped from CIA website
country_file = 'C:\\Users\\stang10\\Dropbox\\data sample\\country_list.txt'
with open(country_file, 'r', errors='ignore') as c_file:
    country_list = c_file.readlines()
    for i in range(len(country_list)):
        country_list[i] = country_list[i].replace('\n','')

# There are two additional country names that should be added to the list (One is a typo, the other is a subpart of Netherlands, this list could be added if we found problems later.)
country_list.append('afghanigstan')
country_list.append('netherlands antilles')  
country_list.append('hong kong')
country_list.append('macau')


# Get the name of all txt files in the directory
file_list = os.listdir(txtPath)

# Month Directory
Month_Dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

# use another file to record the number of total positions for country-year
record_file_name = outPath + '\\record_file\\record.txt'
record_file = open(record_file_name,'w',errors='ignore',encoding='UTF-8')

# ------------------------------------------------
# Run loop across files
# ------------------------------------------------


for file in file_list:
    if file.endswith('.txt'):
        input_file = re.sub(r'.txt$','',file)
        
        # Get year and month for each file
        year = int(input_file[:4])
        month = int(Month_Dict[input_file[4:]])

        file_name = txtPath + '\\' + file

        # Open file
        open_file = open(file_name, "r", errors="ignore",encoding='UTF-8')

        file_text = open_file.readlines()
        
        # -----------------------------------------------------------
        # Step 2: Generate separation for each file
        # The structure of each txt is: The first part-preface; The second part-Other introduction; The third part-Key abbreviations; The fourth part-main data;
        # The fifth part- politician in alphabetic order and index
        # What is useful to us is the third and the fourth part. The fifth part does not exist for some file
        # So we use identifier to separate these parts and clean the data we need
        # ------------------------------------------------------------
        for i, line in enumerate(file_text):
            if 'key to abbreviations' in line.lower():
                i_three = i
            if ('afghanistan' in line.lower() or 'afghanigstan' in line.lower()) and 'i_four' not in vars():  # the latter one is a typo in 2008June.txt, and the last condition is to assure that this appears for the first time
                i_four = i
            if "ALPHABETIC NAME INDEX" in line:
                i_five = i

        if 'i_three' in vars() and 'i_four' in vars():
            pass
        else:
            # This allows me to check for possible file where strategy fails
            print("Separation fails for %s." % (file_name))
            sys.exit(3)  # 3 means separation methodology needs to be looked at
        
        # For files which do not have the fifth part
        if 'i_five' not in vars():
            i_five = len(file_text)

        # ------------------------------------------------------------------------
        # Step 3: Get abbreviation dictionary (So as to replace the name suffix, prefix and position title)
        # For 2001May.txt and 2007December.txt, this part varies a little bit
        # ------------------------------------------------------------------------
       
        abbr_dict = {}
        # the number of questionable keys (after spliting lines)
        #  This is because in 2007December.txt, the key and item are in different lines
        ques_key = 0
        ques_key_list = []
        ques_item = 0
        for i, line in enumerate(file_text[(i_three + 1):i_four]):
            if is_page_line(line):
                continue
            if line != "\n":
                # For 2001May.txt and 2007December.txt
                if (year==2001 and month==5) or (year==2007 and month==12):
                    abbr_list = line.split(" ")  # use a single space to separate abbreviation sets
                     # Go through the items of the list
                    while '\n' in abbr_list:
                        abbr_list.remove('\n')

                    for i in range(len(abbr_list)):
                        abbr_list[i] = abbr_list[i].strip()

                    key = ''
                    item_one = ''



                    # Go over abbr_list to split between key and value
                    # Key contains a '.', except for NDE, and NDE is always in the first place.
                    for w in range(len(abbr_list)):
                        if '.' in abbr_list[w] or abbr_list[w].lower()=='nde':
                            key = ' '.join([key,abbr_list[w]])
                        else:
                            item_one = ' '.join([item_one,abbr_list[w]])

                    key = key.strip()
                    item_one = item_one.strip()

                    temp_list = [key, item_one]
                    
                    while '' in temp_list:
                        temp_list.remove('')

                    if len(temp_list)==1 and 'questionable' not in vars() and year==2007:  # year==2007 is to define between 2001May and 2007December
                        questionable = 1

                    if 'questionable' in vars():
                        if '.' in temp_list[0] or temp_list[0]=='NDE':
                            ques_key += 1
                            ques_key_list.append(temp_list[0])
                        else:
                            ques_value = ' '.join(temp_list)
                            abbr_dict.update({ques_key_list[ques_item]:ques_value})
                            ques_item += 1
                    else:
                        if key in abbr_dict:
                            abbr_dict[key] += ',' + item_one
                        else:
                            abbr_dict[key] = item_one


                    if ques_key==ques_item and ques_key>0:
                        break

                else:
                    abbr_list = line.split("  ")
                  # a list will have two sets of corresponding abbreviation, here we use tab to split the line (For most files)

                    # first set of item
                    key_one = abbr_list[0]
                    item_one = ""
                    key_two = ""
                    item_two = ""
                    abbr_list.remove(key_one)
                    while '' in abbr_list:
                        abbr_list.remove('')
                    # identify the structure of abbr_list
                    if len(abbr_list) > 3:
                        print("Abbreviation structure changed for %s" % (file_name))
                        sys.exit(4)


                    if len(abbr_list)>0:
                        item_one = abbr_list[0]
                    if len(abbr_list) == 3:
                        key_two = abbr_list[1]
                        item_two = abbr_list[2]
                    elif len(abbr_list) == 2:
                        item_two = abbr_list[1]
                        key_two = last_key_two
                    else:
                        pass

                    key_one = key_one.strip()
                    key_two = key_two.strip()

                    if key_one == '':
                        key_one = last_key_one
                        if key_two == '' and item_two == '':
                            continue

                    # here we define the key in the previous column to be the corresponding set 
                    # Because sometimes the key will respond to two values in the same column but different rows
                    last_key_one = key_one
                    last_key_two = key_two

                    # replace \n at the end of string
                    item_one = re.sub('\n', '', item_one)
                    item_two = re.sub('\n', '', item_two)

                    item_one = item_one.strip()
                    item_two = item_two.strip()

                    abbr_dict = add_item([(key_one,item_one),(key_two,item_two)],abbr_dict)
        
        # Delete empty keys
        if '' in abbr_dict:
            abbr_dict.pop('')
        
        for key in list(abbr_dict.keys()):
            if abbr_dict[key]=='':
                abbr_dict.pop(key)


        # ----------------------------------------------------------------------------
        # Step 4: Deal with the main part of data
        # ----------------------------------------------------------------------------

        # *******************************************
        # Step 4.1: Preparation of files
        # *******************************************

        # open a file as the final part of the data
        output_file_name = outPath + '\\' + input_file + '_output' + '.txt'
        output_file = open(output_file_name, 'w', errors='ignore',encoding='UTF-8')
        



        # Count for country each year
        country_count = 0
        # Count for position each country
        position_count = 0
        # Total position count
        t_pos_count = 0

        # *********************************************
        # Step 4.2: Initial clean: judge each line and divide into four types:
        #        0: observation line, containing position name and politician name
        #        1: country name
        #        2: country notes
        #        3: A position name may divide into several lines
        #        4: A name may divide into several lines
        # **********************************************
        
        # Output list after initial clean (judgment of lines and re-position)
        output_list_initial = []

        # initial clean
        for i, line in enumerate(file_text[i_four:i_five]):

            # find country first:
            if '..' not in line and line != '\n' and '   ' not in line.strip():
                # If the line simply contains information about pages, skip to next line
                if is_page_line(line):
                    continue
                else:
                    name_list = line.split()
                    line_content = ' '.join(name_list)

                    if '(continued)'  in line_content:
                        line_content = line_content.replace('(continued)','')
                        line_content = line_content.strip()

                    if is_country(line_content):
                        country_name = line_content.upper()
                        if country_name.lower()=='afghanigstan':
                            country_name = 'AFGHANISTAN'
                        line_last = 1  # line_last: 1-country 2-notation 3-position continue 4-name continue 0-observation 
                        if 'NDE' in country_name and 'country_name' in vars():
                            try:
                                country_name = re.sub(r'NDE', abbr_dict['NDE'], country_name)
                            except KeyError:
                                print(abbr_dict)
                                sys.exit(7)     
                        output_list_initial.append([year,month,country_name,'','','',line_last,i+i_four])
                    elif line[0]==' ' and line_last==0:  # name continue
                        line_last = 4
                        name_continue = line_content
                        output_list_initial.append([year,month,'','','',name_continue,line_last,i+i_four])
                    elif line_last !=1 and line_last !=2:  # position continue
                        line_last = 3
                        position_continue = line_content
                        output_list_initial.append([year,month,'','',position_continue,'',line_last,i+i_four])
                    else:
                        line_last = 2 
                        country_note = line_content
                        output_list_initial.append([year,month,'',country_note,'','',line_last,i+i_four])
                   

            elif line == '\n':
                pass
            else:
                if '..' in line:
                    line_last = 0
                    [person_name, position] = split_line('..',abbr_dict,line)

                    output_list_initial.append([year,month,'','',position,person_name,line_last,i+i_four])  # i+1 gives us a chance to trace back observation in each file

                elif '  ' in line: # this is another type of file
                    line_last = 0
                    [person_name, position] = split_line('  ',abbr_dict,line)
                    output_list_initial.append([year,month,'','',position,person_name,line_last,i+i_four])
        
        # ***************************
        # Step 4.3: Now add country_note, position and name to observations, and create a single line for each country containing country notes
        # ****************************

        country_note = ''
        country_name = ''
        name_continue = ''
        position_continue = ''
        # According to the output_list_initial, generate the ideal data set for use
        output_list_final = []

        for i in range(len(output_list_initial)):
            item = output_list_initial[i]
            line_identifier = item[6]
            location = item[7]
            if line_identifier == 1:
                if country_name!='' and country_name!=item[2]:  # This indicates there is a change of country, and we generate a single observation for each country and country-note at the end of each country
                    output_list_final.append([year,month,country_name,country_note,'','',-1]) # -1 notes that this line is created for tracking purpose
                    country_note = '' # reset all
                    position_continue = '' 
                    name_continue = ''
                    country_count += 1
                    print('%d\t%d\t%s\t%d'%(year,month,country_name,position_count), file=record_file)
                    t_pos_count += position_count
                    position_count = 0
                    
                country_name = item[2]
            elif line_identifier ==2:
                country_note = ' '.join([country_note,item[3]])
            elif line_identifier == 3:   # position_continue
                position_continue = ' '.join([position_continue,item[4]])
            elif line_identifier == 4:
                name_continue = ' '.join([name_continue, item[5]])
            elif line_identifier == 0:
                #   If country_note is non-empty, this means that we have not created a note observation for country
                output_list_final.append([year,month,country_name,'',' '.join([dict_replace(position_continue,abbr_dict),item[4]]),item[5],location+2])
                position_continue = ''
                if name_continue != '':
                    output_list_final[-2][5] = ' '.join([output_list_final[-2][5],dict_replace(name_continue,abbr_dict)])
                    name_continue = ''
                position_count += 1
            
            if i==len(output_list_initial)-1: # last observation, since there is no change in country name, we have to print the last country_name
                output_list_final.append([year,month,country_name,country_note,'','',-1]) # -1 notes that this line is created for tracking purpose
                country_count += 1
                print('%d\t%d\t%s\t%d'%(year,month,country_name,position_count), file=record_file)
                t_pos_count += position_count

        for item in output_list_final:
            print('%d\t%d\t%s\t%s\t%s\t%s\t%d'%(item[0],item[1],item[2],item[3],item[4],item[5],item[6]), file = output_file)







        open_file.close()
        output_file.close()
    
        del i_three, i_four, i_five

        print("Successful for %s, which has %d countries in record, the total number of countries is %d"%(file_name,country_count,len(country_list)-1))

record_file.close()