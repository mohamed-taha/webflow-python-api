# webflow-python-api
A single Python class for interacting with the Webflow CMS API. This `WebflowApi` class provides a simple interface for common Webflow operations, including managing sites, collections, items, and webhooks.


**Note:** This is not a comprehensive wrapper, but a utility class I created for personal use and decided to share. It may serve as a helpful starting point for others working with the Webflow API in Python projects.

Feel free to use, modify, and extend this class for your own Webflow API integrations.


## Usage

```python
api = WebflowApi()
sites = api.list_sites()
items = api.list_items(collection_id)
```
