from openapi import load
import sys

with open(sys.argv[1], 'r') as f:
    swagger = load(f)


