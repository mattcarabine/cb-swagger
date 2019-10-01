> NOTE: This branch is deprecated.
> New development is taking place in the `mad-hatter` and `release/6.0` branches.

## Get Started

Install dependencies.

```bash
cd dita_generation
pip3 install openapi
pip3 install six
pip3 install jinja2
```

Generate DITA files based on a Swagger spec in JSON.

```bash
python3 main.py test_input.json ./tmp
```

> For this to work the swagger spec endpoints must contain the `x-dita-path` key which specifies the name of the DITA file generated ([see example](https://github.com/mattcarabine/cb-swagger/blob/master/ns_server.yaml#L206)).
