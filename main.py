# Python
from typing import List
import json
# FastAPI
from fastapi import Body, FastAPI, status
from pydantic import Required
# Custom
from models.users import User, UserRegister
from models.tweet import Tweet

app = FastAPI()


# Path Operations.

# Users

# Signup
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user: UserRegister = Body(Required)):
    """ 
    Register a User in the app.

    Args:
        user (UserRegister): user with all the information to register.

    Returns:
        dictionary: json with all the user data.
    """
    # Write the user locally in the users.json file.
    with open("database/users.json", "r+", encoding="utf-8") as f:
        # Read as string and convert to dictionary
        results = json.loads(f.read())
        # Convert user to dictionary
        user_dict = user.dict()
        # Convert UUID to STR
        user_dict["user_id"] = str(user_dict["user_id"])
        # Convert datetime to STR
        user_dict["birth_date"] = str(user_dict["birth_date"])
        # Add user to my json
        results.append(user_dict)
        # Move to start
        f.seek(0)
        # Write in the file a json
        f.write(json.dumps(results))

        return user


# Login
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    pass


# All users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    pass


# One user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
def show_user():
    pass


# Delete one user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_user():
    pass


# Update one user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_user():
    pass


# Tweets

# Show all tweets
@app.get(
    path="/home",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"]
)
def home():
    return {"Twitter API": "Working Fine"}


# Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a simple tweet",
    tags=["Tweets"]
)
def show_tweet():
    pass


# Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post():
    pass


# Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_tweet():
    pass


# Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_tweet():
    pass
