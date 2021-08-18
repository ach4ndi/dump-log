import argparse, os, sys, json

# Create the parser
my_parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
my_parser.add_argument('Path',
                       metavar='path',
                       type=str,
                       help='path to log file')
my_parser.add_argument('-t',
                       '--text',
                       action='store',
                       help='select output format, default:text')
my_parser.add_argument('-o',
                       '--output',
                       action='store',
                       help='select output destination')

# Execute parse_args()
args = my_parser.parse_args()

input_pathfile = args.Path
input_pathdir = os.path.dirname(os.path.abspath(input_pathfile))
input_pathfilename = os.path.basename(input_pathfile)

output_format = 'text'

output_filename = ''
output_path = ''
output_content = ''

delimeter = '\t\t'

if args.text:
    if not args.text in ['text','json']:
        print('Desired output format is Invalid')
        sys.exit()
    
    if args.text == 'json':
        output_format = 'json'

split_filename = input_pathfilename.split('.')
output_filename = split_filename[0]
    
file_open = open(args.Path, 'r')
    
if output_format == 'text': 
    output_content = file_open.read()

if output_format == 'json': 
    string_list = file_open.readlines()
    
    result = []
    
    for line in string_list:
        sline = line.split(delimeter)
        field_names = []
        field_c = 1
        
        for g in range(len(sline)):
            field_names.append('field_{}'.format(field_c))
            field_c +=1
        
        result.append({field_name: sline[idx] for idx, field_name in enumerate(field_names)})
    
    output_content = json.dumps(result)

if output_format == 'json':
    output_path = '{}\{}.json'.format(input_pathdir,output_filename)
else:
    output_path = '{}\{}.txt'.format(input_pathdir,output_filename)

if args.output:
    if args.output == '':
        print('Output path is invalid')
        sys.exit()
    
    output_path = args.output
    
    if not os.path.exists(output_path):
        os.makedirs(os.path.dirname(os.path.abspath(output_path)))
    
file_save = open(output_path, 'w')
file_save.write(output_content)