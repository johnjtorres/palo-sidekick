"""Panorama class to interact with the XML API."""

import sys
from typing import Any

import click
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning


class Panorama:
    """
    Boilerplate code for performing HTTP GET requests on Panorama. Some
    commonly used calls are defined as functions
    """

    def __init__(self, hostname: str, api_key: str, timeout: int = 10) -> None:
        self.hostname = hostname
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = f"https://{self.hostname}/api"
        self.session = requests.Session()
        self.session.headers = {"X-PAN-KEY": self.api_key}
        self.session.verify = False
        urllib3.disable_warnings(InsecureRequestWarning)

    def get(self, resource: str, **kwargs: Any) -> requests.Response:
        """Perform an HTTP GET request on this Panorama."""
        url = self.base_url + resource

        try:
            response = self.session.get(url, timeout=self.timeout, **kwargs)
        except requests.exceptions.ConnectionError:
            msg = f"Could not establish a connection to {self.hostname}."
            click.echo(msg, err=True)
            sys.exit(1)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            msg = "Exited due to {code} {reason} error."
            msg = msg.format(code=response.status_code, reason=response.reason)
            click.echo(msg, err=True)
            sys.exit(1)

        return response
