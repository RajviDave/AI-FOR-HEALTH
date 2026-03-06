import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-name", required=True)

args = parser.parse_args()

participant_folder = args.name