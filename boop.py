import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


ACCESS_KEY = ''
SECRET_KEY = ''


dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY,
                          region_name='us-west-2'
                         )

table = dynamodb.Table('ost_data')


response = table.scan(FilterExpression=Key('time').between('2018-10-01T01',
                                                           '2018-10-01T05'))
data = response['Items']

while response.get('LastEvaluatedKey'):
    response = table.scan(
        FilterExpression=Key('time').between('2018-10-01T01',
                                             '2018-10-01T05'),
        ExclusiveStartKey=response['LastEvaluatedKey'])

    data.extend(response['Items'])


# get specific elements from data
for i in data:
    if 'o3' in i:
        print (i['o3'])

# Use this code to get all dev IDs from current table in timeframe
# dev_ids = []
# for i in data:
#     if i['dev_id'] not in dev_ids:
#         dev_ids.append(i['dev_id'])
#
#
# for i in dev_ids:
#     print (i)



