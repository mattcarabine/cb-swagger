import argparse
import json
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
    first_heading = True

    def codespan(self, text):
        return '<codeph>{}</codeph>'.format(text.rstrip())

    def link(self, link, title, content):
        return '<xref href="{}">{}</xref>'.format(link, content or title)

    def block_code(self, code, language=None):
        code = code.rstrip('\n')
        if language:
            return '<codeblock outputclass="language-{}">{}</codeblock>'.format(language, code)
        else:
            return '<codeblock>{}</codeblock>'.format(code)

    def block_quote(self, text):
        return '<codeblock>{}</codeblock>'.format(text)
    
    def header(self, text, level, raw=None):
        # Dita only supports one title per section
        if level < 3:
            return '</section><section><title>{}</title>'.format(text)
        else:
            return '<p><b>{}</b></p>'.format(text)

    def double_emphasis(self, text):
        return '<b>{}</b>'.format(text)
    
    def emphasis(self, text):
        return '<i>{}</i>'.format(text)

    def hrule(self):
        # Dita has no horizontal rule
        return ''
    
    def inline_html(self, text):
        # Dita does not support inline html
        return ''

    def list_item(self, text):
        return '<li>{}</li>'.format(text)
    
    def list(self, body, ordered=True):
        if ordered:
            return '<ol>{}</ol>'.format(body)
        else:
            return '<ul>{}</ul>'.format(body)
    
    def table(self, header, body, cols):
        """Rendering table element. Wrap header and body in it.
        :param header: header part of the table.
        :param body: body part of the table.
        """
        col_string = ['<colspec colname="col{}" colwidth="1*"/>'.format(x+1) for x in range(cols)]
        output_str = ('<table>\n<tgroup cols="{}">\n{}\n'
                      '<thead>\n'.format(cols, '\n'.join(col_string)))
        return output_str + header + '</thead><tbody>{}</tbody>'.format(body) + '</tgroup>\n</table>'
        
    def table_row(self, content):
        """Rendering a table row. Like ``<tr>``.
        :param content: content of current table row.
        """
        return '<row>\n%s</row>\n' % content

    def table_cell(self, content, **flags):
        """Rendering a table cell. Like ``<th>`` ``<td>``.
        :param content: content of current table cell.
        :param header: whether this is header or not.
        :param align: align of current table cell.
        """
        return '<entry>%s</entry>\n' % content
        if flags['header']:
            tag = 'th'
        else:
            tag = 'td'
        align = flags['align']
        if not align:
            return '<%s>%s</%s>\n' % (tag, content, tag)
        return '<%s style="text-align:%s">%s</%s>\n' % (
            tag, align, content, tag
        )

class CustomMarkdownParser(mistune.Markdown):

    def output_table(self):
        aligns = self.token['align']
        aligns_length = len(aligns)
        cell = self.renderer.placeholder()

        # header part
        header = self.renderer.placeholder()
        cols = len(self.token['header'])
        for i, value in enumerate(self.token['header']):
            align = aligns[i] if i < aligns_length else None
            flags = {'header': True, 'align': align}
            cell += self.renderer.table_cell(self.inline(value), **flags)

        header += self.renderer.table_row(cell)

        # body part
        body = self.renderer.placeholder()
        for i, row in enumerate(self.token['cells']):
            cell = self.renderer.placeholder()
            for j, value in enumerate(row):
                align = aligns[j] if j < aligns_length else None
                flags = {'header': False, 'align': align}
                cell += self.renderer.table_cell(self.inline(value), **flags)
            body += self.renderer.table_row(cell)

        return self.renderer.table(header, body, cols)

MD_PARSER = CustomMarkdownParser(renderer=DitaRenderer())


def main():
    parsed_args = parse_arguments(sys.argv[1:])
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)),
                      trim_blocks=True, lstrip_blocks=True)
    file_template = env.get_template("page_template.txt")
    # ditamap_template = env.get_template("ditamap_template.txt")
    dita_file_list = []
    with open(parsed_args.spec_file, 'r') as f:
        swagger = load(f)

    port = swagger.host.split(':', 1)[1]

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
                            example_response = generate_example_response(response_object['schema'])
                            example_response = json.dumps(example_response, sort_keys=True, 
                                                          indent=4)
                            example_responses.append(
                                {'code': response_code,
                                 'example': example_response})

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
                            topic_id=topic_id, definition=definition[method], port=port,
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
