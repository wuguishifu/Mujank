import json
from collections import defaultdict

BIRTHDAY_JSON = "birthdays/birthdays.json"


def get_dictionary() -> dict:
    """
    This function creates and returns a dictionary that contains all of the
    birthdays in Jank.

    :return:    A dictionary that contains all birthdays in Jank in the
                following format:
                    {birthDate1: [userID1], birthDate2: [userID2, userID3],....}
    """
    # A dictionary that contains all birthdays in Jank in the
    # following format:
    #       {birthDate1: [userID1], birthDate2: [userID2, userID3...],....}
    birthdays = defaultdict(list)

    # Load in the JSON data about everyone's birthday
    with open(BIRTHDAY_JSON) as json_file:
        data = json.load(json_file)

        # Place each person into the "birthdays" dictionary
        for birthday, user_id in data["people"].items():
            birthdays[birthday].append(user_id)

    return dict(birthdays)

