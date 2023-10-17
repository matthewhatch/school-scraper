import pyap
import unicodedata
import usaddress

class Address:
    def __init__(self, address: str):
        address_parser = pyap.parse(unicodedata.normalize('NFKC', address), country='US')
        if len(address_parser) > 0:
            self.parsed_address = address_parser[0].as_dict()
            self.full_address = self.parsed_address['full_address']
            self.zip = self.parsed_address['postal_code']
            self.city = self.parsed_address['city']
            self.street_number = self.parsed_address['street_number']
            self.street_name = f'{self.parsed_address["street_name"]} {self.parsed_address["street_type"]}'
            self.state = self.parsed_address['region1']
            self.address_1 = f'{self.street_number} {self.street_name}'
        else:
            self.address_parser, type = usaddress.tag(address)
            self.zip = self.address_parser['ZipCode']
            self.city = self.address_parser['PlaceName']
            self.state = self.address_parser['StateName']

            if type == "PO Box":
                self.po_box_type = self.address_parser['USPSBoxType']
                self.po_box_number = self.address_parser['USPSBoxID']
                self.full_address = f"{self.po_box_type} {self.po_box_number}, {self.city}, {self.state} {self.zip}"
                self.address_1 = f'{self.po_box_type} {self.po_box_number}'
            elif type == "Street Address":
                self.street_number = self.address_parser['AddressNumber']
                self.street_name = self.address_parser['StreetName']
                self.full_address = f"{self.street_number} {self.street_name}, {self.city}, {self.state} {self.zip}"
                self.address_1 = f'{self.street_number} {self.street_name}'
            elif type == "Ambiguous":
                self.address_1 = f'{self.city} {self.state}'
                self.full_address = f"{self.city}, {self.state} {self.zip}"

    def __str__(self):
        address = f'Address(full_address: \'{self.full_address}\''
        address = address + f', address_1: \'{self.address_1}\''
        address = address + f', street_number: \'{self.street_number}\''
        address = address + f', street_name: \'{self.street_name}\''
        address = address + f', city: \'{self.city}\''
        address = address + f', zip: \'{self.zip}\''
        address = address + f', state: \'{self.state}\''
        return address

    def __repr__(self):
        address = f'Address(full_address: \'{self.full_address}\''
        address = address + f', address_1: \'{self.address_1}\''
        address = address + f', street_number: \'{self.street_number}\''
        address = address + f', street_name: \'{self.street_name}\''
        address = address + f', city: \'{self.city}\''
        address = address + f', zip: \'{self.zip}\''
        address = address + f', state: \'{self.state}\''
        return address