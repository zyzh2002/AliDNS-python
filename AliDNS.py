
#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
import requests


def getIdAndValue(response):
    import json

    DomainRecords = json.loads(
        str(response, encoding='utf-8'))['DomainRecords']['Record']

    for record in DomainRecords:
        if record['RR'] == RR and record['Type'] == RRtype:
            return {'id': record['RecordId'], 'value': record['Value']}


def getSystemIP6():
    return requests.get('https://v6.ident.me').text


domainName = ''
RR = ''
RRtype = ''
keyId = ''
keySecret = ''
location = 'cn-hangzhou'

client = AcsClient(keyId, keySecret, location)

request = DescribeDomainRecordsRequest()
request.set_accept_format('json')
request.set_DomainName(domainName)
response = client.do_action_with_exception(request)

IdV = getIdAndValue(response)
sysIP = getSystemIP6()

request = UpdateDomainRecordRequest()
request.set_accept_format('json')
request.set_RecordId(IdV['id'])
request.set_RR(RR)
request.set_Type(RRtype)
request.set_Value(sysIP)

if IdV['value'] != sysIP:
    try:
        response = client.do_action_with_exception(request)
        print('Address updated.')
    except:
        print('An error has occurred.')
        print(response)
else:
    print('Address unchanged.')
