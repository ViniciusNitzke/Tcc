import unittest
import pytest

from app.domains.addresses.models import *


class TestAddressesModels(unittest.TestCase):
    def test_address_model_should_be_serialized(self):
        # Arrange
        _id = str(uuid4())
        address = Address(id=_id, active=True, street='Rua dos Testes', number='123', complement='Testando',
                          zip_code='00000000', city='Blumenau', state='Santa Catarina',
                          on_create=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          on_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Action
        response = address.serialize()

        # Assertions
        self.assertEqual(type(response), dict)
        self.assertIsInstance(address, Address)
        self.assertEqual({'id': _id, 'active': True, 'street': 'Rua dos Testes', 'number': '123',
                          'complement': 'Testando', 'zip_code': '00000000', 'city': 'Blumenau',
                          'state': 'Santa Catarina', 'on_create': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          'on_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}, response)

    def test_address_must_raise_an_empty_field_exception(self):

        # Arrange
        with pytest.raises(EmptyFieldsError) as exc:

            # Action
            Address(street='   ', number=None, zip_code="", city=None, state=None)
            Address()

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) cannot be empty: street, number, zip_code, city, state',
                         exc.value.description)

    def test_address_must_raise_a_not_str_exception(self):
        # Arrange
        with pytest.raises(TypeError) as exc:

            # Action
            Address(street=True, number=123, complement=2.5, zip_code=['00000000'], city={'Blumenau': 'SC'},
                    state=(False, 123))

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type str: street, number, complement, zip_code, city, state',
                         exc.value.description)

    def test_address_must_raise_a_not_bool_exception(self):
        # Arrange
        with pytest.raises(TypeError) as exc:

            # Action
            Address(active='True', street='Rua dos Testes', number='123', zip_code='00000', city='Blumenau', state='SC')

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type bool: active', exc.value.description)

    def test_address_must_raise_a_not_number_exception(self):
        # Arrange
        with pytest.raises(TextError) as exc:

            # Action
            Address(street='Rua dos Testes', number='MY number: 123', zip_code='00000-000', city='Blumenau', state='SC')

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be only numbers: number, zip_code', exc.value.description)

    def test_address_must_raise_a_not_number_or_letter_exception(self):
        # Arrange
        with pytest.raises(TextError) as exc:

            # Action
            Address(street='R. Dos Testes', number='123', zip_code='00000000', city='Blumenau', state='SC')

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be only letters or / and numbers: street', exc.value.description)

    def test_address_must_raise_a_not_letter_exception(self):
        # Arrange
        with pytest.raises(TextError) as exc:

            # Action
            Address(street='Rua Dos Testes', number='123', zip_code='00000000', city='B-N-U', state='13')

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be only letters: city, state', exc.value.description)

    def test_address_must_raise_an_size_exception(self):
        # Arrange
        with pytest.raises(SizeError) as exc:

            # Action
            Address(street='R'*51, number='1'*11, complement='a'*101, zip_code='000000000', city='B'*51, state='SC'*51)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("The field(s) 'street', 'number', 'complement', 'zip_code', 'city', 'state' must be the "
                         "following maximum sizes respectively: 50, 10, 100, 8, 50, 50",
                         exc.value.description)