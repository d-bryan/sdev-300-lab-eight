"""
File: user.py
Author: Dylan Bryan
Date: 11/29/20, 9:30 AM
Project: sdev-300-lab-seven
Purpose: User profile class
"""
import json
from passlib.hash import sha256_crypt as crypt

USER_ID = 0  # counter for number of users


def hash_user_password(password):
    """
    Hashes the original password
    :return: STRING hashed password
    """
    return crypt.hash(password)


def set_user_id():
    """
    Sets the current users ID
    for easier access similar to a
    database
    :return: USER ID
    """
    user_id = USER_ID
    user_id += 1
    return user_id


class User:
    """
    User object to store data about the user once they
    create an account
    """

    def __init__(self, username, password, confirm_password,
                 first_name, last_name, favorite_color,
                 favorite_animal, area_of_study, years_of_study):
        """
        Constructor for User profile object to be used through
        the web application
        :param username: Username of user
        :param password: Hashed password
        :param confirm_password: confirmed hashed password
        :param first_name: First name
        :param last_name: Last name
        :param favorite_color: Favorite color
        :param favorite_animal: Favorite animal
        :param area_of_study: Area of study
        :param years_of_study: Years studied
        """
        # initialize the object
        self.user_id = set_user_id()
        self.username = username
        self.password = password
        self.confirm_password = confirm_password
        self.first_name = first_name
        self.last_name = last_name
        self.favorite_color = favorite_color
        self.favorite_animal = favorite_animal
        self.area_of_study = area_of_study
        self.years_of_study = years_of_study
        # hash the passwords
        self.confirm_hashed_match()

    def confirm_hashed_match(self):
        """
        Checks that the confirmed password
        matches the original hashed password
        then proceeds to hash confirmed password
        :return: STRING hashed confirm password
        """
        # hash the user password
        hashed_password = hash_user_password(self.password)
        self.password = hashed_password
        # verify the user password
        verified = crypt.verify(self.confirm_password, hashed_password)
        if verified is False:
            return
        # set the hash of password to confirmed password
        self.confirm_password = self.password
# end confirm_hashed_match method

    def to_string_json(self):
        """
        Creates a JSON output to be used in registered users text file
        :return: JSON output
        """
        data = dict(user_id=self.user_id,
                    username=self.username,
                    password=self.password,
                    confirmed_password=self.confirm_password,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    favorite_color=self.favorite_color,
                    favorite_animal=self.favorite_animal,
                    area_of_study=self.area_of_study,
                    years_of_study=self.years_of_study)
        # create formatted json object for use in user file
        return json.dumps(data)
# end to_string_json method
