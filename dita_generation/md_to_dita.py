import mistune

def main():
    test_str = """```
    test codeblock
    ```
    """
    markdown = mistune.Markdown(renderer=CustomRenderer())
    print(markdown(test_str))

class CustomRenderer(mistune.Renderer):
    def codespan(self, text):
        return '<codeph>{}</codeph>'.format(text)
    
    def link(self, link, title, content):
        return '<xref href="{}">{}</xref>'.format(link, title or content)

    def block_code(self, code, language=None):
        return '<codeblock>{}</codeblock>'.format(code)

if __name__ == '__main__':
    main()