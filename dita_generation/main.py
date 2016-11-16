import argparse
from openapi import load
import os.path
import sys
from jinja2 import Environment, FileSystemLoader

def main():
    parsed_args = parse_arguments(sys.argv[1:])
    env = Environment(loader=FileSystemLoader('/Users/matt/cb-swagger/dita_generation'), trim_blocks=True, lstrip_blocks=True)
    file_template = env.get_template("page_template.txt")
    ditamap_template = env.get_template("ditamap_template.txt")
    dita_file_list = []
    with open(parsed_args.spec_file, 'r') as f:
        swagger = load(f)

    for path, definition in swagger.paths.items():
        topic_id = path.replace('/', '-')[1:]
        
        for method in ('get', 'post'):
            if method in definition and 'x-dita-path' in definition[method]:
                try:
                    example = generate_example(definition[method]['responses']['200']['schema']['items'][0])
                except Exception as e:
                    example = e
                
                dita_file_name = '{}.dita'.format(definition[method]['x-dita-path'])
                with open(os.path.join(parsed_args.output_dir, dita_file_name), 'w') as f:
                    f.write(file_template.render(topic_id=topic_id, definition=definition[method], method=method, path=path, example=example))
                    dita_file_list.append(dita_file_name)
   
    with open(os.path.join(parsed_args.output_dir, "rest-api.ditamap"), 'w') as f:
        f.write(ditamap_template.render(urls=dita_file_list))

def parse_arguments(cli_args):
    parser = argparse.ArgumentParser(description='OpenApi2Dita - Convert an OpenAPI spec into a set of DITA pages')
    parser.add_argument('spec_file', help='Location of json OpenAPI spec')
    parser.add_argument('output_dir', default='.',
                        help='Output directory for dita files')
    return parser.parse_args(cli_args)

def generate_example(curr_object):
    if 'type' in curr_object and curr_object['type'] == "object":
        return_obj = {}
        for name, property in curr_object['properties'].items():
            return_obj[name] = generate_example(property)
    elif 'type' in curr_object and curr_object['type'] == "array":
        return_obj = []
        for item in curr_object['items']:
            return_obj.append(generate_example(item))
    else:
        try:
            return_obj = curr_object['example']
        except KeyError:
            return_obj = ""
    
    return return_obj

if __name__ == "__main__":
    main()
