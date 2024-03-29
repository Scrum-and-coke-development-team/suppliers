# Copyright 2016, 2021 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Models for Supplier Service

All of the models are stored in this module

Models
------
Supplier - A supplier that we interact with in the marketplace

Attributes:
-----------
name (string) - the name of the supplier
category (string) - the category the supplier belongs to
available (boolean) - whether or not the supplier is available

"""
import logging
from enum import Enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Supplier.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


# class Gender(Enum):
#     """Enumeration of valid Pet Genders"""

#     MALE = 0
#     FEMALE = 1
#     UNKNOWN = 3


class Supplier(db.Model):
    """
    Class that represents a Supplier

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    category = db.Column(db.String(63), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)
    status = db.Column(db.String(63), nullable=False)

    #gender = db.Column(
    #    db.Enum(Gender), nullable=False, server_default=(Gender.UNKNOWN.name)
    #)

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Supplier %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Supplier to the database
        """
        logger.info("Creating %s", self.name)
        # id must be none to generate next primary key
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Supplier to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a Supplier from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict:
        """Serializes a Supplier into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "available": self.available,
            "status": self.status
 #           "gender": self.gender.name,  # convert enum to string
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Supplier from a dictionary
        Args:
            data (dict): A dictionary containing the Supplier data
        """
        try:
            self.name = data["name"]
            self.category = data["category"]
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + str(type(data["available"]))
                )
        #     self.gender = getattr(Gender, data["gender"])  # create enum from string
            self.status = data["status"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid supplier: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid supplier: body of request contained bad or no data " + str(error)
            )
        return self
#
    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app: Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """Returns all of the Suppliers in the database"""
        logger.info("Processing all Suppliers")
        return cls.query.all()

    @classmethod
    def find(cls, supplier_id: int):
        """Finds a Supplier by it's ID

        :param supplier_id: the id of the supplier to find
        :type supplier_id: int

        :return: an instance with the supplier_id, or None if not found
        :rtype: Supplier

        """
        logger.info("Processing lookup for id %s ...", supplier_id)
        return cls.query.get(supplier_id)

    @classmethod
    def find_or_404(cls, supplier_id: int):
        """Find a Supplier by its id

        :param supplier_id: the id of the Supplier to find
        :type supplier_id: int

        :return: an instance with the supplier_id, or 404_NOT_FOUND if not found
        :rtype: Supplier

        """
        logger.info("Processing lookup or 404 for id %s ...", supplier_id)
        return cls.query.get_or_404(supplier_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Suppliers with the given name

        :param name: the name of the Suppliers you want to match
        :type name: str

        :return: a collection of Suppliers with that name
        :rtype: list

        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category: str) -> list:
        """Returns all of the Suppliers in a category

        :param category: the category of the Suppliers you want to match
        :type category: str

        :return: a collection of Suppliers in that category
        :rtype: list

        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available: bool = True) -> list:
        """Returns all Suppliers by their availability

        :param available: True for suppliers that are available
        :type available: str

        :return: a collection of Suppliers that are available
        :rtype: list

        """
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)

    # @classmethod
    # def find_by_gender(cls, gender: Gender = Gender.UNKNOWN) -> list:
    #     """Returns all Pets by their Gender

    #     :param gender: values are ['MALE', 'FEMALE', 'UNKNOWN']
    #     :type available: enum

    #     :return: a collection of Pets that are available
    #     :rtype: list

    #     """
    #     logger.info("Processing gender query for %s ...", gender.name)
    #     return cls.query.filter(cls.gender == gender)
