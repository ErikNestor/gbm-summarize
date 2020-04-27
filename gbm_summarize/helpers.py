#!/usr/bin/env python3
'''
Helpers
Assorted helpers for file and request parsing
'''
import csv
from RequestService import ReqService
from CacheManager import CacheManager

class Helpers:
    def __init__(self, settings):
        self.settings = settings
        self.build_symbol_to_id_map()


    def build_symbol_to_id_map(self):
        self.symbol_to_id_map = self.parse_csv(mapping_file=self.settings['GENE_SYMBOL_TO_ID_MAPPING_FILE'])


    def symbol_to_id(self, key):
        return self.symbol_to_id_map.get(key, None)


    def parse_csv(self, mapping_file=None):
        # Init empty table
        table = {}

        # If we've got a mapping file, read it in
        if (mapping_file):
            try:
                with open(mapping_file) as f:
                    rdr = csv.reader(f)
                    for id, sym in rdr:
                        table.update({sym : id})
            except EnvironmentError:
                print('Mapping file not found!')
    
        return table


    def check_args(self, args):
        # Verify command line arguments
        #   for correct amount and valid gene codes
        # Returns a tuple containing a boolean status and a message
        ret_val = (True, 'Success')

        if not args or len(args) > 3:
            # Incorrect number of args
            ret_val = (False, 'Please supply 1-3 gene codes to use gbm_summarize')

        for arg in args:
            # We can't process genes that aren't in our mapping table
            if not self.symbol_to_id(arg):
                ret_val = (False, 'Unparsable gene code supplied as argument.')
            
        return ret_val

    def get_payload(self, gene_symbol, request_type):
        # Attempt to pull payload from cache
        cs = CacheManager(self.settings['CACHE_FILE'])
        cache_key = f'{gene_symbol}_{request_type}'
        json_response = cs.fetch(cache_key)

        # Otherwise hit the API
        if not json_response:
            rs = ReqService(self.settings)
            json_response = rs.make_request(self.symbol_to_id(gene_symbol), request_type=request_type).json()

            # If request was successful, update cache
            if json_response:
                cs.update(cache_key, json_response)
            else:
                sys.exit()

        return json_response


    def get_alteration_rate(self, gene_symbol):
        payload = self.get_payload(gene_symbol, request_type='ALTERATIONS')

        # Get number of records
        num_items = len(payload)

        # Count altered gene records
        alteration_count = 0;
        for record in payload:
            if record['alteration'] == 2 or record['alteration'] == -2:
                alteration_count = alteration_count + 1

        # Return rate as decimal
        return alteration_count/num_items


    def get_mutation_rate(self, gene_symbol):
        payload = self.get_payload(gene_symbol, request_type='MUTATIONS')
        
        # Hardcoded placeholder til I figure out what they're expecting for this percentage
        return .1 # TODO: FIND THIS OUT!!


class Formatters:
    def decimal_to_percent(self, decimal=None):
        if decimal:
            return f'{(decimal*100):.0f}%'
