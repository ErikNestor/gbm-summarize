#!/usr/bin/env python3

import sys, yaml
from helpers import Helpers, Formatters

settings = {}
with open('lib/settings.yaml', 'r') as s:
    settings = yaml.load(s)

def main(params):
    # We are a fully lowercase compliant operation
    params = [p.upper() for p in params]

    h = Helpers(settings)
    (args_valid, msg) = h.check_args(params)

    if not args_valid:
        # Uh-oh, bad args. Show message and bail.
        print(f'gbm_summarize: {msg}')
        sys.exit()

    # Querying on multiple genes generates different output
    multiple_args = len(params) > 1

    f = Formatters()
    total_copied_or_altered = 0
    for param in params:
        # Get mutation rate
        mut_rate = h.get_mutation_rate(gene_symbol=param)
        # Get alteration rate
        alt_rate = h.get_alteration_rate(gene_symbol=param)
        # Get rate for genes exhibiting alteration and mutation
        combined_rate = alt_rate + mut_rate

        if multiple_args:
            # Display combined rate only and tally
            print(f'{param} is mutated or copy number altered in {f.decimal_to_percent(combined_rate)} of cases.')
            total_copied_or_altered = total_copied_or_altered + combined_rate
        else:
            # Display mutation rate
            print(f'{param} is mutated in {f.decimal_to_percent(mut_rate)} of cases.')
            # Display alteration rate
            print(f'{param} is copy number altered in {f.decimal_to_percent(alt_rate)} of cases.')
            # Display combined rate
            print(f'\nCases with at least one mutation or copy number alteration in {param}: {f.decimal_to_percent(combined_rate)} of all cases.')

    if multiple_args:
        print(f'\nCases with at least one mutation or copy number alteration in one of the genes: {f.decimal_to_percent(total_copied_or_altered)}')

if __name__ == "__main__":
    main(sys.argv[1:])
