# Python
from typing import List
import json
# FastAPI
from fastapi import Body, FastAPI, HTTPException, Path, status
from pydantic import Required
# Custom
from models.users import User, UserLogin, UserRegister, RESPONSE_MODEL_USER
from models.tweet import Tweet, RESPONSE_MODEL_TWEET
from utils.database import search_by_uuid, write_json

# Settings
TWEETS_DATABASE = "./database/tweets.json"
USERS_DATABASE = "./database/users.json"


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
    return write_json(
        src=USERS_DATABASE,
        opt="r+",
        keys=["user_id", "birth_date"],
        response_model=user,
        name=RESPONSE_MODEL_USER)


# Login
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login(user: UserLogin = Body(Required)):  # Could use Form to login
    """Log an user.

    Args:
        user (UserLogin): uuid, email and password.

    Raises:
        HTTPException: user uuid doesn't exist.
        HTTPException: user password mismatch

    Returns:
        User: json with all the user information.
    """
    user_dict = user.dict()
    user_response = search_by_uuid(
        src=USERS_DATABASE, id=str(user_dict["user_id"]))
    if not user_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found')
    if user_response["password"] == user_dict["password"] and user_response["email"] == user_dict["email"]:
        return user_response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong Password"
        )


# All users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    Read all the users from database

    Returns:
        dictionary: returns a json list with all the users in the app
    """
    # Read from users.json
    with open(USERS_DATABASE, "r", encoding="utf-8") as f:
        # Read all the data
        results = json.loads(f.read())
        # Return the users as dict
        return results


# One user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
def show_user(
    user_id: str = Path(
        Required,
        title="User id",
        description="Find an user by uuid")
):
    """
    Read specific tweet finding by id.

    Returns:
        User: json with all the user information.
    """
    with open(USERS_DATABASE, 'r', encoding="utf-8") as f:
        results = json.load(f)

        for user in results:
            if user["user_id"] == user_id:
                return user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user doens't exist")


# Delete one user
@app.delete(
    path="/users/{user_id}/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_user(user_id: str = Path(
        Required,
        title="User id",
        description="User uuid")
):
    """Delete a user using the uuid.

    Args:
        user_id (str, optional): UUID. 

    Raises:
        HTTPException: the user doesn't exist

    Returns:
        str: message with confirmation
    """
    with open(USERS_DATABASE, 'r+', encoding="utf-8") as f:
        results = json.load(f)
        found = False
        for user in results:
            if user["user_id"] == user_id:
                results.remove(user)
                found = True

        if found:
            # Move to start
            f.seek(0)
            f.truncate()
            # Write json in the file
            f.write(json.dumps(results))
            return {"Message": "User delete successfully."}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user doens't exist")


# Update one user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_user(
    user_id: str = Path(
        Required,
        title="User id",
        description="User uuid"),
    user_update: User = Body(
        Required,
        title="New User Data",
        description="New data for the user"
    )
):
    with open(USERS_DATABASE, 'r+', encoding="utf-8") as f:

        users = json.load(f)

        for user in users:
            if user["user_id"] == user_id:
                user_dict = user_update.dict()
                user["email"] = user_dict["email"]
                user["first_name"] = user_dict["first_name"]
                user["last_name"] = user_dict["last_name"]
                user["birth_date"] = str(user_dict["birth_date"])
                f.seek(0)
                f.truncate()
                f.write(json.dumps(users))
                return user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user cannot be updated because it doesn't exist"
        )


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
    """
    Show all the tweets.

    Returns:
        dictionary: returns a json list with all the tweets in the app
    """
    # Read from tweets.json
    with open(TWEETS_DATABASE, "r", encoding="utf-8") as f:
        # Read all the data
        results = json.loads(f.read())
        # Return the tweets as dict
        return results


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
def post(tweet: Tweet = Body(Required)):
    """ 
    Post a tweet in the app

    Args:
        tweet (Tweet): tweet with all the information.

    Returns:
        dictionary: json with all the tweet data.
    """
    # Write the tewwt locally in the tweet.json file.
    return write_json(
        src=TWEETS_DATABASE,
        opt="r+",
        keys=["tweet_id", "created_at", "updated_at"],
        response_model=tweet,
        name=RESPONSE_MODEL_TWEET)


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
