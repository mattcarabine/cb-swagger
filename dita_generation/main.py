from openapi import load
import sys
from jinja2 import Environment, FileSystemLoader

def main():
    env = Environment(loader=FileSystemLoader('/Users/matt/cb-swagger/dita_generation'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("page_template.txt")

    with open(sys.argv[1], 'r') as f:
        swagger = load(f)

    for path, definition in swagger.paths.iteritems():
        topic_id = path.replace('/', '-')[1:]
        
        for method in ('post',):
            try:
                example = generate_example(definition[method]['responses']['200']['schema']['items'][0])
            except Exception as e:
                example = e
            print template.render(topic_id=topic_id, definition=definition[method], method=method, path=path, example=example)

def generate_example(curr_object):
    if 'type' in curr_object and curr_object['type'] == "object":
        return_obj = {}
        for name, property in curr_object['properties'].iteritems():
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