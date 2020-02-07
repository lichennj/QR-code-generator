import csv
import qrcode
import os
import glob
import shutil
from PIL import Image, ImageDraw, ImageFont

# Below are global variables for font and size of the added text
local_font = ImageFont.truetype('calibri.ttf', 55)
local_font_small = ImageFont.truetype('calibri.ttf', 45)
local_font_smaller = ImageFont.truetype('calibri.ttf', 35)

#############################################################################################
# This code is used for generating QR code (in '.png' file format) with text printed at the bottom.
# Written by Chen Li 2019 Summer.
# Need a font file (.ttf)in the same folder of this python file ('calibri.ttf' is used)  
# Program Execution environment is in Python3 64 bit with 'qrcode' and 'pillow' module installed. 
#############################################################################################


#############################################################################################
# [gener_QR] outputs QR code as png files into subfolder same as the filename
# Parameters: [filename]: string of the filename
#             [filepath]: the full path to the current folder with this program
#############################################################################################   
def gener_QR(filename, filepath):
    qr_path = (filepath + '/' + filename)[:-4] + '_QR_codes/unsent/' # Create the folder for QR codes corresponding to the 
    print('Generating QR codes inside folder:', '\n', qr_path, '......')
    if not os.path.exists(qr_path):
        os.makedirs(qr_path)

    #with open(filename, 'rU') as csvfile
    current_file = filepath + '/' + filename
    with open(current_file, 'r') as csvfile: # open the csv file in read only mode 
        # next(csvfile, None) # skip header row to read the data (the header marks the type of the content of the row) ----(No need this line since the data from csv have already eliminated the first line)
        reader = csv.reader(csvfile, delimiter = ',', dialect=csv.excel_tab) # since the csv is exported from google sheet 

        for i, row in enumerate(reader): # Iterate over each element onside the csv file
            qr = qrcode.QRCode(
                version = 10, # The version parameter is an integer from 1 to 40 that controls the size of the QR Code
                error_correction=qrcode.constants.ERROR_CORRECT_L, # The error rate is set to be the smallest 7% from the module
                box_size=10, # box_size indicates how many pixels in each 'box' inside the qrcode
                border=12, # border parameter controls the the white border thick level
            )
            labeldata = row[0] # the QR code is generated from first column of the data
            labeldata = labeldata.replace('&', '&') # sometimes if this step is not perfomrd the qr code will eliminate the content after the first '&' symbol

            qr.add_data(labeldata)
            qr.make() # make the QR code

            #img = qr.make_image() 
            img = qr.make_image(fill_color="black", back_color="white") # tramsform QR code into image
            img.save(qr_path + row[1].format(i)) # save file to the same folder

    # move the '.csv' file into the newly generated folder
    dst = (filepath + '/' + filename)[:-4] + '_QR_codes/' + filename
    shutil.move(current_file, dst)
    return qr_path

#############################################################################################
# [iter_folder_text] 
# Iterates over the current folder with all the QR code '.png's inside 
# input: [qr_path] The path of the folder with all the QR '.png's 
# This is the outer loop of the [add_text] program
#############################################################################################
def iter_folder_text(qr_path):
    print('Adding text at bottom of QR codes inside folder:', '\n', qr_path, '......')
    for file in os.listdir(qr_path):
        add_text(file)
    print('Finished', '\n'*4, '****************___________(O____U____O)_________****************')


#############################################################################################
# [add_text]
# Add 'camper_name' to a single input '.png' file, the 'camper_name' is from the input '.png' file's name 
# input: [img_name] the name of a single '.png' file
# the output is the same '.png' file with text at bottom center added, there will be no new files, all the changes are applied to existing files.
#############################################################################################
def add_text(img_name):
    img = Image.open(img_name)
    draw = ImageDraw.Draw(img)
    size = img.size
    width = size[0]
    height = size[1]
    camper_name = img_name.split('_')[0]
    camper_name = camper_name.lower() # Convert the name to lower case
    #camper_name = camper_name.capitalize()
    words = camper_name.split(' ')
    camper_name = ' '.join([word.title() for word in words])
    ###
    # This part is used for calculating the offset of the text when its needed to be at center bottom of the image
    if (len(camper_name) < 15): 
        w, h = draw.textsize(camper_name, font=local_font)
        draw.text(((width-w)/2, height-90), camper_name, fill=(0), font=local_font)
    elif(len(camper_name) > 25):
        w, h = draw.textsize(camper_name, font=local_font_smaller)
        draw.text(((width-w)/2, height-90), camper_name, fill=(0), font=local_font_smaller)
    else:
        w, h = draw.textsize(camper_name, font=local_font_small)
        draw.text(((width-w)/2, height-90), camper_name, fill=(0), font=local_font_small)
    img.save(img_name)


#############################################################################################
# This main program is used for extracting the information inside the ".csv" file and output them into qr code with ".png" file suffix 
# Make sure the ".csv" file is inside the same folder as this program's parent folder
# It is able to iterate throughout the current folder with all the files with '.csv' and export the data into folder with same name as the '.csv' file
#############################################################################################
if __name__ == "__main__":
    filepath = os.getcwd() # read the current file path
    # filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Read the parent path of the current file
    print('\n'*2, '***********_____________QR CODE Generator_____________***********', '\n'*2, 'Starting generating QR codes, the current folder is:' , '\n' , filepath, '\n'*2)
    # iterate all the csv files in this folder
    #for root, dirs, files in os.walk(filepath, topdown=True):
    count = 0
    os.chdir(filepath)
    # Commented, was used for the function that [iter_folder_text] does
    #print(os.getcwd())
    #for files in os.getcwd():
    #    print(files)
    #    for file in files:
    #        if file.endswith('.csv'):
    #            gener_QR(str(file), filepath)
    extension = 'csv'
    path_list = []
    for file in glob.glob('*.{}'.format(extension)):
        print(str(file))
        path_list.append(gener_QR(str(file), filepath))
        count = count + 1
    print('Finished', count, 'folder in the parent folder.', '\n'*2, '****************___________(0____.____0)_________****************')
# Below 3 lines are for the add text at the bottom center of the 
#    for qr_path in path_list:
#            os.chdir(qr_path)
#            iter_folder_text(qr_path)

    input('Press Anykey to Exit......')












