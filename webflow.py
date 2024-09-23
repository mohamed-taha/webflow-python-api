from typing import Any, Literal

from django.conf import settings
import requests


class WebflowApi:
    """
    A class for interacting with the Webflow CMS API.

    This class provides methods to perform various operations on Webflow sites, collections, and items.
    It handles authentication and low-level API requests, offering a convenient interface for:

    - Retrieving site and collection information
    - Managing CMS items (create, read, update, delete)
    - Publishing sites
    - Handling domains
    - Managing webhooks

    The class uses the Webflow API key stored in Django settings for authentication.

    Usage:
        api = WebflowApi()
        sites = api.list_sites()
        items = api.list_items(collection_id)

    Note: Ensure that the WEBFLOW_API_KEY is properly set in your Django settings.
    """

    WEBFLOW_URL = "https://api.webflow.com"
    HEADERS = {
        'Accept-Version': "1.0.0",
        'Authorization': f"Bearer {settings.WEBFLOW_API_KEY}",
        'content-type': "application/json"
    }


    def _webflow_request(
        self, method: Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        path: str,
        **kwargs: Any
    ) -> dict:
        res = requests.request(
            method,
            f"{self.WEBFLOW_URL}/{path}",
            headers=self.HEADERS,
            **kwargs
        )

        print(res.json())

        res.raise_for_status()

        return res.json()

    def info(self) -> dict:
        return self._webflow_request('GET', 'info')

    def list_sites(self) -> dict:
        return self._webflow_request('GET', 'sites')

    def get_site(self, site_id: str) -> dict:
        return self._webflow_request('GET', f'sites/{site_id}')

    def publish_site(self, site_id: str, domain_names) -> dict:
        """Takes site_id->str and domain_names->list as arguments"""
        # TODO: Fix
        domains = {"domains": domain_names}
        return self._webflow_request('POST', f'sites/{site_id}/publish', json=domains)

    def list_domains(self, site_id) -> dict:
        return self._webflow_request('GET', f'sites/{site_id}/domains')

    def list_collections(self, site_id: str) -> dict:
        return self._webflow_request('GET', f'sites/{site_id}/collections')

    def get_collection(self, collection_id: str) -> dict:
        return self._webflow_request('GET', f'collections/{collection_id}')


    def list_items(
        self,
        collection_id: str,
        limit: int = 100,
        offset: int = 0,
        all: bool = False
    ) -> dict:
        """
        List items in a CMS collection
        """
        if all:
            all_items = []
            resp = self.list_items(collection_id, offset=offset, all=False)
            all_items.extend(resp['items'])

            while(len(all_items) < resp['total']):
                offset += 100
                resp = self.list_items(collection_id, offset=offset, all=False)
                all_items.extend(resp['items'])

            resp['items'] = all_items
            resp['count'] = len(all_items)

            return resp
        else:
            return self._webflow_request('GET', f'collections/{collection_id}/items?limit={limit}&offset={offset}')

    def get_item(self, collection_id: str, item_id: str) -> dict:
        return self._webflow_request('GET', f'collections/{collection_id}/items/{item_id}')

    def create_item(self, collection_id: str, item_data: dict, live: bool = False) -> dict:
        data = {}
        data['fields'] = item_data

        l = '?live=true' if live else ''

        return self._webflow_request('POST', f'collections/{collection_id}/items{l}', json=data)

    def update_item(
        self,
        collection_id: str,
        item_id: str,
        item_data: dict,
        live: bool = False
    ) -> dict:
        data = {}
        data['fields'] = item_data

        l = '?live=true' if live else ''

        return self._webflow_request('PUT', f'collections/{collection_id}/items/{item_id}{l}', json=data)

    def patch_item(
        self,
        collection_id: str,
        item_id: str,
        item_data: dict,
        live: bool = False
    ) -> dict:
        data = {}
        data['fields'] = item_data

        l = '?live=true' if live else ''

        return self._webflow_request('PATCH', f'collections/{collection_id}/items/{item_id}{l}', json=data)

    def remove_item(self, collection_id: str, item_id: str) -> dict:
        return self._webflow_request('DELETE', f'collections/{collection_id}/items/{item_id}')

    def list_webhooks(self, site_id: str) -> dict:
        return self._webflow_request('GET', f'sites/{site_id}/webhooks')

    def get_webhook(self, site_id: str, webhook_id: str) -> dict:
        return self._webflow_request('GET', f'sites/{site_id}/webhooks/{webhook_id}')

    def create_webhook(self, site_id: str, triggerType: str, url: str, filter: dict) -> dict:
        data = {
            'triggerType': triggerType,
            'url': url,
            'filter': filter
        }

        return self._webflow_request('POST', f'sites/{site_id}/webhooks', json=data)

    def remove_webhook(self, site_id: str, webhook_id: str) -> dict:
        return self._webflow_request('DELETE', f'sites/{site_id}/webhooks/{webhook_id}') 
        