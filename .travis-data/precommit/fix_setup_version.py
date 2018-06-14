# -*- coding: utf-8 -*-
"""Function to perform the version check for the pre-commit hook"""
import json
import os
import sys


def main():
    """Run the version check for the pre-commit hook"""
    import aiida_quantumespresso

    this_path = os.path.split(os.path.realpath(__file__))[0]

    # Get current JSON content
    setup_path = os.path.join(this_path, os.pardir, os.pardir, 'setup.json')
    with open(setup_path) as handle:
        setup_content = json.load(handle)

    # Retrieve version from python package
    sys.path.insert(0, os.path.join(this_path, os.pardir, os.pardir))
    version = aiida_quantumespresso.__version__

    setup_content['version'] = version

    # Rewrite JSON in a 'consistent' way (sorted, indented)
    with open(setup_path, 'w') as handle:
        json.dump(setup_content, handle, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
