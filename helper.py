import json
import logging
import os.path
import allure
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from requests import Session, Response
import curlify


def load_json_schema(name: str):
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "schemas", name
    )
    with open(schema_path) as schema:
        return json.loads(schema.read())


class CustomSession(Session):
    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def request(self, method, url, *args, **kwargs) -> Response:
        response = super(CustomSession, self).request(
            method=method, url=self.base_url + url, *args, **kwargs
        )
        curl = curlify.to_curl(response.request)
        status_code = response.status_code

        logging.info(f"Status code: {status_code}\n{curl}")
        with step(f"{method} {self.base_url}{url}"):
            allure.attach(
                body=f"Status code: {status_code}\n{curl}",
                name="Request curl",
                attachment_type=AttachmentType.TEXT,
                extension="txt",
            )

            try:
                response_body = response.json()
            except json.JSONDecodeError:
                response_body = response.text

            allure.attach(
                body=json.dumps(response_body),
                name="Response body",
                attachment_type=AttachmentType.JSON,
                extension="json"
            )
            return response


users_session = CustomSession("https://reqres.in/api/users")
resources_session = CustomSession("https://reqres.in/api/unknown/")
register_session = CustomSession("https://reqres.in/api/register/")
login_session = CustomSession("https://reqres.in/api/login/")
