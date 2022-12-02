import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app
from App.controllers import (
    create_user,
    get_all_users_json,
    get_all_users,
    create_image,
    create_distributor,
    distribute,
    get_all_distributors,
)

# This commands file allow you to create convenient CLI commands for testing controllers


app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print("database intialized")


"""
User Commands
"""

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup("user", help="User object commands")

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f"{username} created!")


# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == "string":
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli


"""
Generic Commands
"""


@app.cli.command("init")
def initialize():
    create_db(app)
    print("database intialized")


"""
Test Commands
"""

test = AppGroup("test", help="Testing commands")


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))


app.cli.add_command(test)


# Create users for tests
@app.cli.command("create-users")
def create_users_command():
    create_user("rob1", "robpass")
    create_user("rob2", "robpass")
    create_user("rob3", "robpass")
    create_user("rob4", "robpass")
    print("rob1-rob4 created")


@app.cli.command("create-user")
def create_user_command():
    create_user("bob", "bobpass")
    print("bob created!")


@app.cli.command("add-user-images")
def add_images_command():
    users = get_all_users()
    for user in users:
        create_image(user.id, "https://picsum.photos/200/300")
        create_image(user.id, "https://picsum.photos/201/301")
        create_image(user.id, "https://picsum.photos/202/302")
        create_image(user.id, "https://picsum.photos/203/303")
    print("images added")


@app.cli.command("distribute-data")
def distribute_data_command():
    users = get_all_users()
    dist = create_distributor(len(users))
    distribute(dist.id)
    print("data distributed...see table below")
    distributors = get_all_distributors()
    print("FEED ID  |  RECEIVER  |  SENDER  |  DISTRIBUTOR  |  SEEN")
    for distributor in distributors:
        for feed in distributor.feed:
            print(
                f"    {feed.id}    |    {feed.receiver_id}    |    {feed.sender_id}    |    {feed.distributor_id}    |   {feed.seen}    "
            )
