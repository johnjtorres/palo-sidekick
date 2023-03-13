"""Defined Panorama class to interact with the XML API."""

import sys
import xml.etree.ElementTree as ET
from typing import Any, List, Optional

import click
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning


class Panorama:
    def __init__(self, hostname: str, api_key: str, timeout: int = 10) -> None:
        self.hostname = hostname
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = f"https://{self.hostname}/api"
        self.session = requests.Session()
        self.session.headers = {"X-PAN-KEY": self.api_key}
        self.session.verify = False
        urllib3.disable_warnings(InsecureRequestWarning)

    @property
    def device_groups(self) -> Optional[List[str]]:
        resource = "/?type=op&cmd=<show><devicegroups/></show>"
        response = self.get(resource)
        root = ET.fromstring(response.text)
        device_groups = root.findall(".//devicegroups/entry")
        if not device_groups:
            return None
        return [dg.attrib["name"] for dg in device_groups]

    def get(self, resource: str, **kwargs: Any) -> requests.Response:
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
