import pyap
import unicodedata
import usaddress

class Address:
    def __init__(self, address: str):
        address_parser = pyap.parse(unicodedata.normalize('NFKC', address), country='US')
        self.parsed_address = address_parser[0].as_dict()
        self.full_address = self.parsed_address['full_address']
        self.zip = self.parsed_address['postal_code']
        self.city = self.parsed_address['city']
        self.street_number = self.parsed_address['street_number']
        self.street_name = f'{self.parsed_address["street_name"]} {self.parsed_address["street_type"]}'
        self.address_1 = f'{self.street_number} {self.street_name}'
        self.state = self.parsed_address['region1']

    def __str__(self):
        return self.zip

    def __repr__(self):
        address = f'Address(full_address: \'{self.full_address}\''
        address = address + f', address_1: \'{self.address_1}\''
        address = address + f', street_number: \'{self.street_number}\''
        address = address + f', street_name: \'{self.street_name}\''
        address = address + f', city: \'{self.city}\''
        address = address + f', zip: \'{self.zip}\''
        address = address + f', state: \'{self.state}\''
        return address  