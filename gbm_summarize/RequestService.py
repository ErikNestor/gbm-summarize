#!/usr/bin/env python3
'''
ReqService
Simple request wrapper for hitting CBioPortal API
'''
import json, requests

class ReqService:

    def __init__(self, settings=None):
        # Parse settings into instance vars for API requests
        if settings:
            self.base_url = settings['BASE_URI']
            self.request_params = settings['REQUEST_PARAMS']
            self.study_resource = settings['STUDY_RESOURCE']
            self.headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
    
    def make_request(self, gene_id=None, request_type='MUTATIONS'):
        # Assemble request header and body from instance vars
        url = self.base_url + self.study_resource[request_type]
        params = []

        for p in self.request_params[request_type]:
            params.append(
                (p, self.request_params[request_type][p])
            )

        data = f'{{"entrezGeneIds": [{gene_id}],"sampleListId": "gbm_tcga_cnaseq"}}'

        # Make the request
        try:
            response = requests.post(
                                    url,
                                    headers=self.headers,
                                    params=params,
                                    data=data
                                )
        except requests.exceptions.RequestException as e:
            print(f'API Request failed. Error: {e}')
            print(f'Request Type: {request_type} Gene ID: {gene_id}')
            response = None

        return response

    