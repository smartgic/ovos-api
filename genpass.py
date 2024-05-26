#!/usr/bin/env python

import argparse
import bcrypt

parser = argparse.ArgumentParser()
parser.add_argument("--password", type=str, required=True)
args = parser.parse_args()

salt = bcrypt.gensalt(rounds=12)
password = args.password.encode("utf-8")
hasher = bcrypt.hashpw(password=password, salt=salt).decode("utf-8")

print(hasher)
