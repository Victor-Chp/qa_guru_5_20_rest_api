from requests import Response
from jsonschema import validate
from helper import load_json_schema, users_session, resources_session, register_session, login_session

url = "https://reqres.in/api/"
url_users = url + "users"
url_resources = url + "unknown"
url_reg = url + "register"
url_login = url + "login"


def test_create_user():
    name = "jane"
    job = "job"
    response = users_session.post("/", json={"name": name, "job": job})
    assert response.status_code == 201
    assert response.json()["name"] == name


def test_create_user_schema_validation():
    name = "morpheus"
    job = "job"
    schema = load_json_schema("post_create_user.json")
    response = users_session.post("/", json={"name": name, "job": job})
    validate(instance=response.json(), schema=schema)


def test_get_single_user_schema_validation():
    id_user = 2
    schema = load_json_schema("get_single_user.json")
    response = users_session.get(f"/{id_user}")
    validate(instance=response.json(), schema=schema)


def test_get_single_user():
    id_user = 2
    response = users_session.get(f"/{id_user}")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == id_user


def test_single_user_not_found():
    id_user = 23
    response = users_session.get(f"/{id_user}")
    assert response.status_code == 404
    assert response.text == "{}"


def test_update_user_firstname_schema_validation():
    params = {
        "first_name": "Bill",
        "last_name": "MacDuck",
        "email": "billdac@gmail.com",
        "job": "Golden Store",
    }
    response = users_session.post("/", params)
    id_user = response.json()["id"]
    params["first_name"] = "George"
    schema = load_json_schema("update_user_firstname.json")
    response = users_session.put(f"/{id_user}", json=params)
    validate(instance=response.json(), schema=schema)


def test_update_user_firstname():
    params = {
        "first_name": "Bill",
        "last_name": "MacDuck",
        "email": "billdac@gmail.com",
        "job": "Golden Store",
    }

    response = users_session.post("/", params)
    id_user = response.json()["id"]
    params["first_name"] = "George"
    response = users_session.put(f"/{id_user}", json=params)
    assert response.status_code == 200
    assert response.json()["first_name"] == params["first_name"]


def test_get_users_list_schema_validation():
    response = users_session.get("/")
    schema = load_json_schema("get_users_list.json")
    validate(instance=response.json(), schema=schema)


def test_users_list_default_lenght():
    default_users_count = 6
    response: Response = users_session.get("")
    assert len(response.json()["data"]) == default_users_count


def test_delete_user_id():
    params = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@gmail.com",
        "planet": "Earth",
    }

    response = users_session.post("", params=params)
    id_user = response.json()["id"]
    response = users_session.delete(str(id_user))
    assert response.status_code == 204
    assert response.text == ""


def test_get_list_resources_schema_validation():
    response = resources_session.get("")
    schema = load_json_schema("get_list_resources.json")
    validate(instance=response.json(), schema=schema)


def test_get_list_resources():
    response = resources_session.get("")
    assert response.status_code == 200
    assert response.json()["data"][0]["id"] != ""
    assert response.json()["data"][0]["name"] != ""


def test_get_single_resourse_schema_validation():
    id_resource = 2
    response = resources_session.get(str(id_resource))
    schema = load_json_schema("get_single_resource.json")
    validate(instance=response.json(), schema=schema)


def test_get_single_resource():
    id_resource = 2
    response = resources_session.get(str(id_resource))
    assert response.status_code == 200
    assert response.json()["data"]["id"] != ""
    assert response.json()["data"]["name"] != ""


def test_register_successful_schema_validation():
    json_data = {"email": "eve.holt@reqres.in", "password": "pistole1233"}
    response = register_session.post("", json=json_data)
    schema = load_json_schema("post_register_succesful.json")
    validate(instance=response.json(), schema=schema)


def test_register_successful():
    json_data = {"email": "eve.holt@reqres.in", "password": "pistole1233"}
    response = register_session.post("", json=json_data)
    assert response.status_code == 200


def test_register_unsuccessful_schema_validation():
    json_data = {"email": "sydney@fife"}
    response = register_session.post("", json=json_data)
    schema = load_json_schema("post_register_unsuccesful.json")
    validate(instance=response.json(), schema=schema)


def test_register_unsuccessful():
    json_data = {"email": "sydney@fife"}
    response = register_session.post("", json=json_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_login_successful_schema_validation():
    json_data = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    response = login_session.post("", json=json_data)
    schema = load_json_schema("post_login_successful.json")
    validate(instance=response.json(), schema=schema)


def test_login_successful():
    json_data = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    response: Response = login_session.post("", json=json_data)
    assert response.status_code == 200
    assert response.json()["token"] != ""


def test_login_unsuccessful_schema_validation():
    json_data = {"email": "peter@klaven"}
    response = login_session.post("", json=json_data)
    schema = load_json_schema("post_login_unsuccessful.json")
    validate(instance=response.json(), schema=schema)


def test_login_unsuccessful():
    json_data = {"email": "peter@klaven"}
    response: Response = login_session.post("", json=json_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_delayed_response_schema_validation():
    params = {"delay": 3}
    response = users_session.get("", params=params)
    schema = load_json_schema("get_delayed_response.json")
    validate(instance=response.json(), schema=schema)


def test_delayed_response():
    params = {"delay": 3}
    response = users_session.get("", params=params)
    assert response.status_code == 200
    assert response.json()["data"][0]["id"] != ""


def test_requested_page_number():
    page = 2
    response = users_session.get("", params={"page": page})
    assert response.status_code == 200
    assert response.json()["page"] == page


def test_delete_user_returns_204():
    id_user = 2
    response = users_session.delete(f"/{id_user}")
    assert response.status_code == 204
    assert response.text == ""
