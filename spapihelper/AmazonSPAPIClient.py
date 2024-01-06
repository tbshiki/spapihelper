from sp_api.api import Catalog, Orders, Reports
from sp_api.base import Marketplaces, SellingApiException

import time
import requests


class AmazonSPAPIClient:
    def __init__(
        self,
        marketplace=Marketplaces.JP,
        refresh_token=None,
        lwa_app_id=None,
        lwa_client_secret=None,
    ):
        self.marketplace = marketplace
        self.credentials = {
            "refresh_token": refresh_token,
            "lwa_app_id": lwa_app_id,
            "lwa_client_secret": lwa_client_secret,
        }

    def search_catalog_items(self, keyword):
        try:
            catalog = Catalog(self.marketplace, credentials=self.credentials)
            response = catalog.list_items(Query=keyword, MarketplaceId=self.marketplace.marketplace_id)
            return response.payload
        except SellingApiException as e:
            print(f"Catalog API Error: {e}")
            return None

    def get_orders(self, created_after, created_before):
        try:
            orders = Orders(self.marketplace, credentials=self.credentials)
            response = orders.get_orders(
                CreatedAfter=created_after,
                CreatedBefore=created_before,
                MarketplaceIds=[self.marketplace.marketplace_id],
            )
            return response.payload
        except SellingApiException as e:
            print(f"Orders API Error: {e}")
            return None

    def request_listing_report(self, report_type="GET_MERCHANT_LISTINGS_ALL_DATA"):
        try:
            reports_api = Reports(credentials=self.credentials, marketplace=self.marketplace)
            response = reports_api.create_report(reportType=report_type)
            return response.payload
        except SellingApiException as e:
            print(f"Report Request Error: {e}")
            return None

    def request_order_report(self, report_type="GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL", **kwargs):
        try:
            reports_api = Reports(credentials=self.credentials, marketplace=self.marketplace)
            response = reports_api.create_report(reportType=report_type, dataStartTime=kwargs.get("dataStartTime"), dataEndTime=kwargs.get("dataEndTime"))
            return response.payload
        except SellingApiException as e:
            print(f"Order Report Request Error: {e}")
            return None

    def get_report_document_url(self, report_document_id):
        try:
            reports_api = Reports(credentials=self.credentials, marketplace=self.marketplace)
            response = reports_api.get_report_document(report_document_id)
            return response.payload.get("url")
        except SellingApiException as e:
            print(f"Get Report Document Error: {e}")
            return None

    def download_report_data(self, report_document_id, temp_gzip_file_name):
        try:
            url = self.get_report_document_url(report_document_id)
            if url:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(temp_gzip_file_name, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            else:
                print("Report URL is not available.")
                return False
        except Exception as e:
            print(f"Error downloading report: {e}")
            return False

    def wait_for_report_to_be_ready(self, report_id, timeout=300, interval=30):
        elapsed_time = 0
        while elapsed_time < timeout:
            try:
                reports_api = Reports(credentials=self.credentials, marketplace=self.marketplace)
                response = reports_api.get_report(report_id)
                if response.payload.get("processingStatus") == "DONE":
                    return response.payload.get("reportDocumentId")
                time.sleep(interval)
                elapsed_time += interval
            except SellingApiException as e:
                print(f"Error while waiting for report: {e}")
                return None
        return None

    def download_report_data(self, report_document_id, temp_gzip_file_name):
        try:
            url = self.get_report_document_url(report_document_id)
            if url:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(temp_gzip_file_name, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            else:
                print("Report URL is not available.")
                return False
        except Exception as e:
            print(f"Error downloading report: {e}")
            return False
