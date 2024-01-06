# spapihelper

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)





# 在庫レポート
# https://developer-docs.amazon.com/sp-api/docs/report-type-values-inventory
# https://developer-docs.amazon.com/sp-api/docs/inventory-reports-attributes#get_flat_file_open_listings_data
# 在庫レポート :
# 出品詳細レポート (カスタム) :
# Amazonが出荷する在庫 :
# 出品中の商品レポートLite : GET_MERCHANT_LISTINGS_DATA_LITE
# 出品中の商品レポートLite : GET_MERCHANT_LISTINGS_DATA_LITER
# 出品中の商品レポート :
# 出品されていない商品のレポート :
# すべての出品商品のレポート : GET_MERCHANT_LISTINGS_ALL_DATA
# キャンセルされた商品のレポート : GET_MERCHANT_CANCELLED_LISTINGS_DATA
# 販売済みの商品情報レポート :
# 手数料見積りレポート :

# 特定のレポートタイプをリクエスト
report_response = client.request_report("GET_MERCHANT_LISTINGS_ALL_DATA")
# 他のレポートタイプをリクエスト
other_report_response = client.request_report("ANOTHER_REPORT_TYPE")

# 注文レポート
# https://developer-docs.amazon.com/sp-api/docs/report-type-values-order
# https://developer-docs.amazon.com/sp-api/docs/order-reports-attributes
# 新しい注文 :
# 保留中の注文 :
# 未出荷の注文 :
# End of day Forms :
# 過去の注文 :

# 注文レポートをリクエスト
order_report_response = client.request_order_report(dataStartTime='2024-01-01', dataEndTime='2024-01-31')


# 使用例: AmazonSPAPIClient
# デフォルトのマーケットプレイス (日本) を使用
client_jp = AmazonSPAPIClient()
# 別のマーケットプレイスを指定する場合
client_us = AmazonSPAPIClient(marketplace=Marketplaces.US)

# credentialsを引数として渡す
client = AmazonSPAPIClient(
    marketplace=Marketplaces.JP,
    refresh_token="your_refresh_token",
    lwa_app_id="your_lwa_app_id",
    lwa_client_secret="your_lwa_client_secret",
)

# 使用例: DataConverter
# デフォルトの設定で変換
converter.convert_gzip_to_txt(temp_gzip_file_name, txt_file_name)

# カスタムの設定で変換
custom_encoding = "utf-8"
custom_field_size_limit = 500_000_000
converter.convert_gzip_to_txt(
    temp_gzip_file_name, txt_file_name, encoding=custom_encoding, field_size_limit=custom_field_size_limit
)

# 使用例
client = AmazonSPAPIClient(
    refresh_token="your_refresh_token",
    lwa_app_id="your_lwa_app_id",
    lwa_client_secret="your_lwa_client_secret",
)

temp_gzip_file_name = "temp_report_data.gz"
txt_file_name = "report_data.txt"
temp_directory = "/path/to/temp"  # 一時ディレクトリのパス
delete_original = True  # 元ファイルを削除するかどうか

report_request = client.request_report()
if report_request and "reportId" in report_request:
    report_id = report_request["reportId"]
    report_document_id = client.wait_for_report_to_be_ready(report_id)
    if report_document_id:
        full_temp_gzip_file_path = os.path.join(temp_directory, temp_gzip_file_name)
        if client.download_report_data(report_document_id, full_temp_gzip_file_path):
            # 使用例 : DataConverter
            converter = DataConverter()
            converter.convert_gzip_to_txt(
                full_temp_gzip_file_path,
                os.path.join(temp_directory, txt_file_name),
                temp_directory=temp_directory,
                delete_original=delete_original,
            )
            print("Report downloaded and converted successfully.")
        else:
            print("Failed to download report data.")
    else:
        print("Report was not ready in time or invalid reportDocumentId.")
else:
    print("Failed to request report or get report ID.")