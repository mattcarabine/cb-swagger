import argparse
import logging
import mistune
from openapi import load
import os.path
import pprint
import sys
from jinja2 import Environment, FileSystemLoader


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('OpenAPI2Dita')


class DitaRenderer(mistune.Renderer):
    def codespan(self, text):
        return '<codeph>{}</codeph>'.format(text)

    def link(self, link, title, content):
        return '<xref href="{}">{}</xref>'.format(link, title or content)

    def block_code(self, code, language=None):
        return '<codeblock>{}</codeblock>'.format(code)

MD_PARSER = mistune.Markdown(renderer=DitaRenderer())


def main():
    parsed_args = parse_arguments(sys.argv[1:])
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)),
                      trim_blocks=True, lstrip_blocks=True)
    file_template = env.get_template("page_template.txt")
    # ditamap_template = env.get_template("ditamap_template.txt")
    dita_file_list = []
    with open(parsed_args.spec_file, 'r') as f:
        swagger = load(f)

    for path, definition in swagger.paths.items():
        topic_id = path.replace('/', '-')[1:]

        for method in ('get', 'post'):

            if method in definition and 'x-dita-path' in definition[method]:
                if (not parsed_args.include_file or
                        definition[method]['x-dita-path'] in parsed_args.include_file):

                    example_responses = []
                    for response_code, response_object in sorted(
                            definition[method]['responses'].items()):
                        if 'schema' in response_object:
                            example_responses.append(
                                {'code': response_code,
                                 'example': generate_example_response(response_object['schema'])})

                    dita_file_name = '{}.dita'.format(definition[method]['x-dita-path'])
                    full_path = os.path.join(parsed_args.output_dir, dita_file_name)

                    definition[method]['description'] = MD_PARSER(definition[method]['description'])

                    body_properties = {'required': [], 'optional': []}
                    query_parameters = {'required': [], 'optional': []}

                    example_curl = "curl -X {} -u 'Administrator:password' 'http://{}{}'".format(
                        method.upper(), swagger.host, path)
                    api_explorer_link = 'http://marabine.co.uk/#!/{}/{}{}'.format(
                        definition[method]['tags'][0], method, path.replace('/', '_'))
                    
                    if 'parameters' in definition[method]:
                        for parameter in sorted(definition[method]['parameters'],
                                                key=lambda x: x['name']):
                            if parameter['in'] == 'formData':
                                body_properties['required' if 'required' in parameter and
                                                parameter['required'] else 'optional'].append(parameter)
                            elif parameter['in'] == 'query':
                                query_parameters['required' if 'required' in parameter and
                                                parameter['required'] else 'optional'].append(
                                                    parameter)
                            else:
                                raise ValueError('Unexpected location for `{}`. Expected "formData" '
                                                'or "query"'.format(parameter['name']))

                            if 'x-example-1' in parameter:
                                example_curl += " -d '{}={}'".format(parameter['name'],
                                                                parameter['x-example-1'])

                            if 'description' in parameter:
                                parameter['description'] = MD_PARSER(parameter['description'])

                    if 'x-example-1' in definition[method]:
                        example_curl = {'command': example_curl, 'description': MD_PARSER(
                            definition[method]['x-example-1'])}
                    else:
                        example_curl = None

                    with open(full_path, 'w') as f:
                        f.write(file_template.render(
                            topic_id=topic_id, definition=definition[method],
                            query_parameters=query_parameters, body_properties=body_properties,
                            method=method, path=path, example_responses=example_responses, 
                            example_curl=example_curl, api_explorer_link=api_explorer_link))
                        LOGGER.info('Created {}'.format(os.path.abspath(full_path)))
                        dita_file_list.append(dita_file_name)


def parse_arguments(cli_args):
    parser = argparse.ArgumentParser(
        description='OpenApi2Dita - Convert an OpenAPI spec into a set of DITA pages')
    parser.add_argument('spec_file', help='Location of json OpenAPI spec')
    parser.add_argument('output_dir', default='.',
                        help='Output directory for dita files')
    parser.add_argument('--include-file', help='File to render', action='append')
    return parser.parse_args(cli_args)


def generate_example_response(curr_object):

    if 'type' in curr_object and curr_object['type'] == "object":
        return_obj = {}
        for name, response_property in curr_object['properties'].items():
            return_obj[name] = generate_example_response(response_property)
    elif 'type' in curr_object and curr_object['type'] == "array":
        return_obj = [generate_example_response(curr_object['items'])]
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
