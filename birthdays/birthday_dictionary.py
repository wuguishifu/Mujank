import json
from birthdays import birthday_constants


def get_dictionary() -> dict:
    """
    This function creates and returns a dictionary that contains all of the
    birthdays in Jank.

    :return:    A dictionary that contains all birthdays in Jank in the
                following format:
                    {birthDate1: [userID1], birthDate2: [userID2, userID3,...],....}
    """

    with open(birthday_constants.BIRTHDAY_JSON_FILE) as json_file:
        return json.load(json_file)[birthday_constants.USERS_FIELD_NAME]



