import re
#function for getting initial file name from the input string and also creating a save filepath for convenience
# with detailed specification what was done to image
def get_file_name(input_string):
    output_filename = ""
    symbol_counter = 0
    for i in range (-1, -len(input_string), -1 ):
        symbol_counter += 1
        if input_string[i-1] == "/" or i == -len(input_string):
            output_filename = input_string[len(input_string)-symbol_counter:len(input_string)]
            break
    for ext in [".png", ".jpg", ".jpeg"]:
        if ext in output_filename:
            output_filename = output_filename.replace(ext, "")
            output_filepath = re.sub(output_filename+ext, "", input_string) + "Enhanced/"
    return output_filename, output_filepath 