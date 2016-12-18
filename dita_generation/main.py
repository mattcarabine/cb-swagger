import argparse
import logging
from openapi import load
import os.path
import sys
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('OpenAPI2Dita')

def main():
    parsed_args = parse_arguments(sys.argv[1:])
    logger.info(parsed_args)
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)), trim_blocks=True, lstrip_blocks=True)
    file_template = env.get_template("page_template.txt")
    ditamap_template = env.get_template("ditamap_template.txt")
    dita_file_list = []
    with open(parsed_args.spec_file, 'r') as f:
        swagger = load(f)

    for path, definition in swagger.paths.items():
        topic_id = path.replace('/', '-')[1:]

        for method in ('get', 'post'):

            if method in definition and 'x-dita-path' in definition[method]:
                if not parsed_args.include_file or definition[method]['x-dita-path'] in parsed_args.include_file:
                    try:
                        example = generate_example_response(definition[method]['responses']['200']['schema']['items'][0])
                    except Exception as e:
                        logger.exception('example generation failed')
                        example = None

                    dita_file_name = '{}.dita'.format(definition[method]['x-dita-path'])
                    full_path = os.path.join(parsed_args.output_dir, dita_file_name)

                    required_parameters = []
                    optional_parameters = []
                    example_curl_command = 'curl -X {} -u Administrator:password http://{}{}'.format(method.upper(), swagger.host, path)

                    for parameter in sorted(definition[method]['parameters'], key=lambda x: x['name']):
                        if 'required' in parameter and parameter['required']:
                            required_parameters.append(parameter)
                        else:
                            optional_parameters.append(parameter)
                        
                        if 'x-example-1' in parameter:
                            example_curl_command += ' -d {}={}'.format(parameter['name'], parameter['x-example-1'])
                    
                    with open(full_path, 'w') as f:
                        f.write(file_template.render(topic_id=topic_id, definition=definition[method], 
                            required_parameters=required_parameters, optional_parameters=optional_parameters, 
                            method=method, path=path, example=example, example_curl_command=example_curl_command))
                        logger.info('Created {}'.format(os.path.abspath(full_path)))
                        dita_file_list.append(dita_file_name)

def parse_arguments(cli_args):
    parser = argparse.ArgumentParser(description='OpenApi2Dita - Convert an OpenAPI spec into a set of DITA pages')
    parser.add_argument('spec_file', help='Location of json OpenAPI spec')
    parser.add_argument('output_dir', default='.',
                        help='Output directory for dita files')
    parser.add_argument('--include-file', help='File to render', action='append')
    return parser.parse_args(cli_args)


def generate_example_response(curr_object):
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
            if curr_object['type'] == 'int':
                return_obj = 0
            elif curr_object['type'] == 'string':
                return_obj = 'string'
            else:
                return_obj = ''
    
    return return_obj

if __name__ == "__main__":
    main()
