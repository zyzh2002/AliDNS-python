#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
import json
import os
import requests


def getIdAndValue(response):
    import json

    DomainRecords = json.loads(str(response, encoding='utf-8'))
    DomainRecords = DomainRecords['DomainRecords']
    DomainRecords = DomainRecords['Record']

    recLenth = len(DomainRecords) - 1

    i = 0
    while i <= recLenth:
        record = DomainRecords[i]
        if record['RR'] == RR:
            if record['Type'] == RRtype:
                recordId = record['RecordId']
                recordValue = record['Value']
                break
        i = i + 1
    return {'id': recordId, 'value': recordValue}


def getSystemIP6():
    text = requests.get('https://v6.ident.me').text
    return text


domainName = 'name'
RR = 'rr'
RRtype = 'type'
keyId = 'id'
keySecret = 'sec'
location = 'loc'

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
