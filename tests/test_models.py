# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Suppliers Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_pets.py:TestPetModel

"""
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service.models import Supplier, DataValidationError, db
from service import app
from .factories import SupplierFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Supplier  M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestSupplierModel(unittest.TestCase):
    """Test Cases for Supplier Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Supplier.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_supplier(self):
        """Create a supplier and assert that it exists"""
        supplier = Supplier(name="amazon", category="drugs", available=True)
        self.assertTrue(supplier is not None)
        self.assertEqual(supplier.id, None)
        self.assertEqual(supplier.name, "amazon")
        self.assertEqual(supplier.category, "drugs")
        self.assertEqual(supplier.available, True)
        # self.assertEqual(pet.gender, Gender.MALE)
        # supplier = Supplier(name="Fido", category="dog", available=False, gender=Gender.FEMALE)
        # self.assertEqual(pet.available, False)
        # self.assertEqual(pet.gender, Gender.FEMALE)

    def test_add_a_supplier(self):
        """Create a supplier and add it to the database"""
        suppliers = Supplier.all()
        self.assertEqual(suppliers, [])
        supplier = Supplier(name="amazon", category="drugs", available=True)
        self.assertTrue(supplier is not None)
        self.assertEqual(supplier.id, None)
        supplier.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(supplier.id, 1)
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 1)

    def test_update_a_supplier(self):
        """Update a Supplier"""
        supplier = SupplierFactory()
        logging.debug(supplier)
        supplier.create()
        logging.debug(supplier)
        self.assertEqual(supplier.id, 1)
        # Change it an save it
        supplier.category = "cosmetics"
        original_id = supplier.id
        supplier.update()
        self.assertEqual(supplier.id, original_id)
        self.assertEqual(supplier.category, "cosmetics")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0].id, 1)
        self.assertEqual(suppliers[0].category, "cosmetics")

    def test_delete_a_supplier(self):
        """Delete a Supplier"""
        supplier = SupplierFactory()
        supplier.create()
        self.assertEqual(len(Supplier.all()), 1)
        # delete the supplier and make sure it isn't in the database
        supplier.delete()
        self.assertEqual(len(Supplier.all()), 0)

    def test_serialize_a_supplier(self):
        """Test serialization of a Supplier"""
        supplier = SupplierFactory()
        data = supplier.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], supplier.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], supplier.name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], supplier.category)
        self.assertIn("available", data)
        self.assertEqual(data["available"], supplier.available)
        #self.assertIn("gender", data)
        #self.assertEqual(data["gender"], pet.gender.name)

    def test_deserialize_a_supplier(self):
        """Test deserialization of a Supplier"""
        data = {
            "id": 1,
            "name": "walmart",
            "category": "drugs",
            "available": True,
            #"gender": "FEMALE",
        }
        supplier = Supplier()
        supplier.deserialize(data)
        self.assertNotEqual(supplier, None)
        self.assertEqual(supplier.id, None)
        self.assertEqual(supplier.name, "walmart")
        self.assertEqual(supplier.category, "drugs")
        self.assertEqual(supplier.available, True)
       # self.assertEqual(pet.gender, Gender.FEMALE)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Supplier with missing data"""
        data = {"id": 1, "name": "walmart", "category": "drugs"}
        supplier = Supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        supplier = Supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)

    def test_deserialize_bad_available(self):
        """Test deserialization of bad available attribute"""
        test_supplier = SupplierFactory()
        data = test_supplier.serialize()
        data["available"] = "true"
        supplier = Supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)

    # def test_deserialize_bad_gender(self):
    #     """Test deserialization of bad gender attribute"""
    #     test_pet = PetFactory()
    #     data = test_pet.serialize()
    #     data["gender"] = "male"  # wrong case
    #     pet = Pet()
    #     self.assertRaises(DataValidationError, pet.deserialize, data)

    def test_find_supplier(self):
        """Find a Supplier by ID"""
        suppliers = SupplierFactory.create_batch(3)
        for supplier in suppliers:
            supplier.create()
        logging.debug(suppliers)
        # make sure they got saved
        self.assertEqual(len(Supplier.all()), 3)
        # find the 2nd supplier in the list
        supplier = Supplier.find(suppliers[1].id)
        self.assertIsNot(supplier, None)
        self.assertEqual(supplier.id, suppliers[1].id)
        self.assertEqual(supplier.name, suppliers[1].name)
        self.assertEqual(supplier.available, suppliers[1].available)

    def test_find_by_category(self):
        """Find Supplier by Category"""
        Supplier(name="amazon", category="drugs", available=True).create()
        Supplier(name="walmart", category="cosmetics", available=False).create()
        suppliers = Supplier.find_by_category("drugs")
        self.assertEqual(suppliers[0].category, "drugs")
        self.assertEqual(suppliers[0].name, "amazon")
        self.assertEqual(suppliers[0].available, True)

    def test_find_by_name(self):
        """Find a Supplier by Name"""
        Supplier(name="amazon", category="drugs", available=True).create()
        Supplier(name="walmart", category="cosmetics", available=False).create()
        suppliers = Supplier.find_by_name("amazon")
        self.assertEqual(suppliers[0].category, "drugs")
        self.assertEqual(suppliers[0].name, "amazon")
        self.assertEqual(suppliers[0].available, True)

    def test_find_by_availability(self):
        """Find Suppliers by Availability"""
        Supplier(name="amazon", category="drugs", available=True).create()
        Supplier(name="walmart", category="cosmetics", available=False).create()
        Supplier(name="target", category="food", available=True).create()
        suppliers = Supplier.find_by_availability(False)
        supplier_list = list(suppliers)
        self.assertEqual(len(supplier_list), 1)
        self.assertEqual(suppliers[0].name, "amazon")
        self.assertEqual(suppliers[0].category, "drugs")
        suppliers = Supplier.find_by_availability(True)
        supplier_list = list(suppliers)
        self.assertEqual(len(supplier_list), 2)

    # def test_find_by_gender(self):
    #     """Find Pets by Gender"""
    #     Pet(name="Fido", category="dog", available=True, gender=Gender.MALE).create()
    #     Pet(
    #         name="Kitty", category="cat", available=False, gender=Gender.FEMALE
    #     ).create()
    #     Pet(name="Fifi", category="dog", available=True, gender=Gender.MALE).create()
    #     pets = Pet.find_by_gender(Gender.FEMALE)
    #     pet_list = list(pets)
    #     self.assertEqual(len(pet_list), 1)
    #     self.assertEqual(pets[0].name, "Kitty")
    #     self.assertEqual(pets[0].category, "cat")
    #     pets = Pet.find_by_gender(Gender.MALE)
    #     pet_list = list(pets)
    #     self.assertEqual(len(pet_list), 2)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        suppliers = SupplierFactory.create_batch(3)
        for supplier in suppliers:
            supplier.create()

        supplier = Supplier.find_or_404(suppliers[1].id)
        self.assertIsNot(supplier, None)
        self.assertEqual(supplier.id, suppliers[1].id)
        self.assertEqual(supplier.name, suppliers[1].name)
        self.assertEqual(supplier.available, suppliers[1].available)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Supplier.find_or_404, 0)
