#!/usr/bin/python

import argparse
from passlib.context import CryptContext

parser = argparse.ArgumentParser()
parser.add_argument('--password', type=str, required=True)
args = parser.parse_args()

hasher = CryptContext(schemes=['bcrypt'])
print(hasher.hash(args.password))
