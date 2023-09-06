import unicodedata
import usaddress

class Address:
    def __init__(self, address: str):
        self.full_address = unicodedata.normalize('NFKC', address)
        self.parsed_address = usaddress.tag(self.full_address)[0]
        self.zip = self.parsed_address['ZipCode']
        self.city = self.parsed_address['PlaceName']
        self.street_number = self.parsed_address['AddressNumber']
        self.street_name = self.parsed_address['StreetName']
        self.street_name_post_type = self.parsed_address['StreetNamePostType']
        self.address_1 = f'{self.street_number} {self.street_name} {self.street_name_post_type}'
        self.state = self.parsed_address['StateName']

    def __str__(self):
        return self.zip

    def __repr__(self):
        address = f'Address(full_address: \'{self.full_address}\''
        address = address + f', address_1: \'{self.address_1}\''
        address = address + f', street_number: \'{self.street_number}\''
        address = address + f', street_name: \'{self.street_name}\''
        address = address + f', street_name_post_type: \'{self.street_name_post_type}\''
        address = address + f', city: \'{self.city}\''
        address = address + f', zip: \'{self.zip}\''
        address = address + f', state: \'{self.state}\''
        return address  