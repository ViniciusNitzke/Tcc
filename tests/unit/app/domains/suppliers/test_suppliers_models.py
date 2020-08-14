import unittest
import pytest

from app.domains.suppliers.models import *


class TestSuppliersModels(unittest.TestCase):
    def test_serializing_the_suppliers_model(self):
        # Arrange
        id = str(uuid4())
        address_id = str(uuid4())
        category_id = str(uuid4())
        supplier = Supplier(id=id,
                            active=True,
                            company_name='Teste Inc',
                            cnpj='73808025000190',
                            trading_name='Teste',
                            phone="04732342021",
                            email='empresa@business.com',
                            address_id=address_id,
                            category_id=category_id,
                            on_create=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            on_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Action
        json = supplier.serialize()

        # Assertions
        self.assertIsInstance(supplier, Supplier)
        self.assertEqual(type(json), dict)
        self.assertEqual(json['id'], id)
        self.assertEqual(json['active'], True)
        self.assertEqual(json['company_name'], 'Teste Inc')
        self.assertEqual(json['cnpj'], '73808025000190')
        self.assertEqual(json['trading_name'], 'Teste')
        self.assertEqual(json['phone'], '04732342021')
        self.assertEqual(json['email'], 'empresa@business.com')
        self.assertEqual(json['address_id'], address_id)
        self.assertEqual(json['category_id'], category_id)
        self.assertEqual(json['on_create'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(json['on_update'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    def test_serialize_summed_version_should_return_a_summed_dict(self):
        # Arrange
        id = str(uuid4())
        address_id = str(uuid4())
        category_id = str(uuid4())
        supplier = Supplier(id=id,
                            active=True,
                            company_name='Teste Inc',
                            cnpj='73808025000190',
                            trading_name='Teste',
                            phone="04732342021",
                            email='empresa@business.com',
                            address_id=address_id,
                            category_id=category_id,
                            on_create=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            on_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Action
        response = supplier.serialize_summed_version()

        # Assertions
        self.assertIsInstance(supplier, Supplier)
        self.assertEqual(type(response), dict)
        self.assertEqual(response, {'id': id,
                                    'trading_name': 'Teste',
                                    'on_create': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    'on_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})

    def test_supplier_must_raise_an_empty_field_exception(self):
        # Arrange
        with pytest.raises(EmptyFieldsError) as exc:

            # Action
            Supplier(company_name='  ', cnpj=None, trading_name='   ', phone=None, email='  ', address_id=None,
                     category_id=None)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) cannot be empty: company_name, cnpj, trading_name, phone, email, '
                         'address_id, category_id', exc.value.description)

    def test_supplier_must_raise_a_not_str_exception(self):
        # Arrange
        address_id = str(uuid4())
        category_id = str(uuid4())
        with pytest.raises(TypeError) as exc:

            # Action
            Supplier(company_name=True, cnpj='19482738496717', trading_name=(False,123), phone='28173948571',
                     email='teste@teste.com', address_id=address_id, category_id=category_id,)
        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type str: company_name, trading_name',
                         exc.value.description)

    def test_supplier_must_raise_a_not_bool_exception(self):
        # Arrange
        address_id = str(uuid4())
        category_id = str(uuid4())
        with pytest.raises(TypeError) as exc:

            # Action
            Supplier(active='True', company_name="Test Company", cnpj='19482738496717',
                     trading_name="Trading test name", phone='28173948571', email='teste@teste.com',
                     address_id=address_id, category_id=category_id,)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type bool: active', exc.value.description)

    def test_supplier_must_raise_a_not_number_exception(self):
        # Arrange
        address_id = str(uuid4())
        category_id = str(uuid4())
        with pytest.raises(TextError) as exc:

            # Action
            Supplier(company_name="Test Company", cnpj='MY number: 123', trading_name="Trading test name",
                     phone='(28)94857173', email='teste@teste.com', address_id=address_id, category_id=category_id)
        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be only numbers: cnpj, phone', exc.value.description)

    def test_supplier_must_raise_a_not_letter_exception(self):
        # Arrange
        with pytest.raises(TextError) as exc:

            # Action
            address_id = str(uuid4())
            category_id = str(uuid4())
            Supplier(company_name="Test Company123", cnpj='19482738496717', trading_name="Trading test name123",
                     phone='28173948571', email='teste@teste.com', address_id=address_id, category_id=category_id,)
        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be only letters: company_name, trading_name',
                         exc.value.description)

    def test_supplier_must_raise_an_email_exception(self):
        # Arrange
        with pytest.raises(EmailError) as exc:

            # Action
            address_id = str(uuid4())
            category_id = str(uuid4())
            Supplier(company_name="Test Company", cnpj='19482738496717', trading_name="Trading test name",
                     phone='28173948571', email='email', address_id=address_id, category_id=category_id,)
        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('E-mail must be a valid email', exc.value.description)

    def test_supplier_must_raise_a_maximum_size_exception(self):
        # Arrange
        with pytest.raises(SizeError) as exc:

            # Action
            Supplier(company_name="T"*201, cnpj='19482738496717231231', trading_name="T"*201, phone='1'*12,
                     email=f"teste@test{'e'*187}.com", address_id='1'*37, category_id='2'*37)
        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("The field(s) 'company_name', 'trading_name', 'phone', 'email', 'address_id', 'category_id' "
                         "must be the following maximum sizes respectively: 200, 200, 11, 200, 36, 36",
                         exc.value.description)

    def test_supplier_must_raise_a_minimum_size_exception(self):
        # Arrange
        address_id = str(uuid4())
        category_id = str(uuid4())
        with pytest.raises(SizeError) as exc:

            # Action
            Supplier(company_name="Test Company", cnpj='19482738496717231231', trading_name="Trading test name",
                     phone='123456789', email='teste@teste.com', address_id=address_id, category_id=category_id)
        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("The field(s) 'phone' must be the following minimum sizes respectively: 10",
                         exc.value.description)

    def test_supplier_must_raise_an_exactly_size_exception(self):
        # Arrange
        address_id = str(uuid4())
        category_id = str(uuid4())
        with pytest.raises(SizeError) as exc:

            # Action
            Supplier(company_name="Test Company", cnpj='1', trading_name="Trading test name",
                     phone='12345678910', email='teste@teste.com', address_id=address_id, category_id=category_id)
        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("The field(s) 'cnpj' must be the following exactly sizes respectively: 14",
                         exc.value.description)
