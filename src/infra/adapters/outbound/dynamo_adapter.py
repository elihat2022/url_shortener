import time
import boto3
from boto3.dynamodb.conditions import Attr
from src.application.ports.url_repository import URL_Repository
from src.domain.url import Url

class DynamoAdapter(URL_Repository):
    def __init__(self, table_name: str = 'urls'):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def save_url(self, url: str) -> int:
        new_id = int(time.time() * 1000)
        self.table.put_item(
            Item={
                'id': new_id,
                'url_link': url,
                'aliases': ''
            }
        )
        return new_id
    
    def update_url_alias(self, url_id: int, alias: str) -> None:
        self.table.update_item(
            Key={
                'id': url_id
            },
            UpdateExpression = 'SET aliases= :val',
            ExpressionAttributeValues = {':val': alias}
        )

    def get_url_by_alias(self, alias: str) -> Url | None:
        response = self.table.scan(
            FilterExpression=Attr('aliases').eq(alias)
        )
        items = response.get('Items', [])
        
        if items:
            row = items[0]

            return Url(url_link=row['url_link'], aliases=row['aliases'])
        
        return None