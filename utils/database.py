# Python
import json
from typing import List

# Custom
from models.tweet import RESPONSE_MODEL_TWEET


def write_json(src: str, opt: str, keys: List[str], response_model, name: str):
    # Write the user locally in the users.json file.
    with open(src, opt, encoding="utf-8") as f:
        # Read as string and convert to dictionary
        results = json.loads(f.read())
        # Convert object to dictionary
        object_dict = response_model.dict()
        # Convert all values to str
        for k in keys:
            print("Key", k)
            object_dict[k] = str(object_dict[k])

        if name == RESPONSE_MODEL_TWEET:
            # Cast user info to str
            object_dict["by"]["user_id"] = str(object_dict["by"]["user_id"])
            object_dict["by"]["birth_date"] = str(
                object_dict["by"]["birth_date"])

        # Add object to json
        results.append(object_dict)
        # Move to start
        f.seek(0)
        # Write json in the file
        f.write(json.dumps(results))
        return response_model


def search_by_uuid(src : str, id : str):
    with open(src, 'r', encoding="utf-8") as f:
        # Read as string and convert to dictionary
        results = json.loads(f.read())

        for element in results:
            if element["user_id"] == id:
                return element
        return None