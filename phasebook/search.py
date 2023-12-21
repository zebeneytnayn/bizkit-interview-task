from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    results = []

    for user in USERS:
        if (
            ("id" in args and args["id"] == user["id"]) or
            ("name" in args and args["name"].lower() in user["name"].lower()) or
            ("age" in args and user["age"] - 1 <= int(args["age"]) <= user["age"] + 1) or
            ("occupation" in args and args["occupation"].lower() in user["occupation"].lower())
        ):
            results.append(user)

    # remove id duplicate
    unique_results = {user["id"]: user for user in results}.values()

    # sorts
    sorted_results = sorted(unique_results, key=lambda x: (
        x["id"] == args.get("id", ""),
        x["name"].lower() == args.get("name", "").lower(),
        abs(x["age"] - int(args.get("age", 0))),
        x["occupation"].lower() == args.get("occupation", "").lower()
    ))

    return list(sorted_results)

