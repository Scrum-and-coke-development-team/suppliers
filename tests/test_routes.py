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
Pet API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_service.py:TestSupplierServer
"""

import os
import logging
import unittest

# from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from service import app, status
from service.models import db, init_db
from .factories import SupplierFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
# logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/suppliers"
WRONG_URL = "/funhouse"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestSupplierServer(unittest.TestCase):
    """Supplier Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_suppliers(self, count):
        """Factory method to create pets in bulk"""
        suppliers = []
        for _ in range(count):
            test_supplier = SupplierFactory()
            resp = self.app.post(
                BASE_URL, json=test_supplier.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test supplier"
            )
            new_supplier = resp.get_json()
            test_supplier.id = new_supplier["id"]
            suppliers.append(test_supplier)
        return suppliers

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
       # data = resp.get_json()
       # self.assertEqual(data["name"], "Supplier REST API Service")

    def test_get_supplier_list(self):
        """Get a list of Suppliers"""
        self._create_suppliers(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_supplier(self):
        """Get a single Supplier"""
        # get the id of a supplier
        test_supplier = self._create_suppliers(1)[0]
        resp = self.app.get(
            "/suppliers/{}".format(test_supplier.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_supplier.name)

    def test_get_supplier_not_found(self):
        """Get a Supplier thats not found"""
        resp = self.app.get("/suppliers/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_supplier(self):
        """Create a new supplier"""
        test_supplier = SupplierFactory()
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_supplier = resp.get_json()
        self.assertEqual(new_supplier["name"], test_supplier.name, "Names do not match")
        self.assertEqual(
            new_supplier["category"], test_supplier.category, "Categories do not match"
        )
        self.assertEqual(
            new_supplier["available"], test_supplier.available, "Availability does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_supplier = resp.get_json()
        self.assertEqual(new_supplier["name"], test_supplier.name, "Names do not match")
        self.assertEqual(
            new_supplier["category"], test_supplier.category, "Categories do not match"
        )
        self.assertEqual(
            new_supplier["available"], test_supplier.available, "Availability does not match"
        )

    def test_create_supplier_no_data(self):
        """Create a Supplier with missing data"""
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_supplier_no_content_type(self):
        """Create a supplier with no content type"""
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_supplier_bad_available(self):
        """ Create a supplier with bad available data """
        test_supplier = SupplierFactory()
        logging.debug(test_supplier)
        # change available to a string
        test_supplier.available = "true"
        resp = self.app.post(
            BASE_URL, json=test_supplier.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_pet_bad_gender(self):
    #     """ Create a Pet with bad available data """
    #     pet = PetFactory()
    #     logging.debug(pet)
    #     # change gender to a bad string
    #     test_pet = pet.serialize()
    #     test_pet["gender"] = "male"    # wrong case
    #     resp = self.app.post(
    #         BASE_URL, json=test_pet, content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_supplier(self):
        """Update an existing Supplier"""
        # create a supplier to update
        test_supplier = SupplierFactory()
        resp = self.app.post(
            BASE_URL, json=test_supplier.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the supplier
        new_supplier = resp.get_json()
        logging.debug(new_supplier)
        new_supplier["category"] = "unknown"
        resp = self.app.put(
            "/suppliers/{}".format(new_supplier["id"]),
            json=new_supplier,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_supplier = resp.get_json()
        self.assertEqual(updated_supplier["category"], "unknown")

    def test_delete_supplier(self):
        """Delete a Supplier"""
        test_supplier = self._create_suppliers(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_supplier.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_supplier.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_supplier_list_by_category(self):
        """Query Suppliers by Category"""
        suppliers = self._create_suppliers(10)
        test_category = suppliers[0].category
        category_suppliers = [supplier for supplier in suppliers if supplier.category == test_category]
        resp = self.app.get(
            BASE_URL, query_string="category={}".format(quote_plus(test_category))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(category_suppliers))
        # check the data just to be sure
        for supplier in data:
            self.assertEqual(supplier["category"], test_category)

#    # @patch('service.routes.Supplier.find_by_name')
#     def test_bad_request(self, bad_request_mock):
#         """ Test a Bad Request error from Find By Name """
#         bad_request_mock.side_effect = DataValidationError()
#         resp = self.app.get(BASE_URL, query_string='name=walmart')
#         self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

#     # @patch('service.routes.Pet.find_by_name')
#     def test_mock_search_data(self, supplier_find_mock):
#         """ Test showing how to mock data """
#         supplier_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'walmart'})]
#         resp = self.app.get(BASE_URL, query_string='name=walmart')
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_disable_supplier(self):
            """Disable an existing Supplier"""
            # create a supplier to disable
            test_supplier = SupplierFactory()
            resp = self.app.post(
                BASE_URL, json=test_supplier.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

            # Disable the supplier
            new_supplier = resp.get_json()
            logging.debug(new_supplier)
            resp = self.app.put(
                "/suppliers/{}/disable".format(new_supplier["id"]),
                json=new_supplier,
                content_type=CONTENT_TYPE_JSON,
            )
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            updated_supplier = resp.get_json()
            self.assertEqual(updated_supplier["status"], "disabled")

    def test_method_not_allowed(self):
        """Make an illegal method call"""
        resp = self.app.put(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)