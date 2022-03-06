import json
from birthdays import birthday_constants
from collections import defaultdict


def get_dictionary() -> dict:
    """
    This function creates and returns a dictionary that contains all of the
    birthdays in Jank.

    :return:    A dictionary that contains all birthdays in Jank in the
                following format:
                    {birthDate1: [userID1], birthDate2: [userID2, userID3,...],....}
    """
    # A dictionary that contains all birthdays in Jank in the following format:
    #   {birthDate1: [userID1], birthDate2: [userID2, userID3,...],....}
    birthdays = defaultdict(list)

    # Load in the JSON data about everyone's birthday
    with open(birthday_constants.BIRTHDAY_JSON_FILE) as json_file:
        data = json.load(json_file)

        # Place each person into the "birthdays" dictionary
        for birthday, user_id in data[birthday_constants.USERS_FIELD_NAME].items():
            birthdays[birthday].append(user_id)

    return dict(birthdays)

