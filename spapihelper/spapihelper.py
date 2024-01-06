from sp_api.api import Catalog
from sp_api.api import Reports
from sp_api.base import Marketplaces, SellingApiException


credentials = dict(
    refresh_token="amazon_refresh_token",
    lwa_app_id="amazon_app_id",
    lwa_client_secret="amazon_client_secret",
)


# sample
def search_catalog_items(keyword):
    try:
        catalog = Catalog(Marketplaces.JP, credentials=credentials)
        response = catalog.list_items(
            Query=keyword, MarketplaceId=Marketplaces.JP.marketplace_id
        )
        return response.payload
    except SellingApiException as e:
        print(f"Error: {e}")
        return None


test_keyword = "book"
items = search_catalog_items(test_keyword)
print(items)
