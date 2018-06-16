
#Authors:  Neil Jubinville

# v0 - Just messing with Bitcoin here... a separate analysis will occur later to determine
#      inheritance and object similarity to other blockchain tx props like ETH

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import AtomicExchange
from AtomicExchange.models import Account
from django.contrib.auth.models import User

# TX Model JSON Structure from bitcoind example
"""
{
	"involvesWatchonly": true,
	"account": "",
	"address": "mmFFG4jqAtw9MoCC88hw5FNfreQWuEHADp",
	"category": "receive",
	"amount": 8,
	"label": "",
	"confirmations": 1,
	"blockhash": "3125fc0ebdcbdae25051f0f5e69ac2969cf910bdf5017349ef55a0ef9d76d591",
	"blockindex": 28,
	"blocktime": 1524913087278,
	"txid": "146df95d04dc205f10cbb07d4a55d0ed924056a6a4c8873823fd09811b76387e",
	"vout": 32,
	"walletconflicts": [],
	"time": 1524913064422,
	"timereceived": 1524913064422,
	"bip125-replaceable": "no"
}
"""

class Transaction(models.Model):
    target = models.ForeignKey(User, related_name='transactions', default=None)
    involvesWatchonly = models.BooleanField()
    account = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    category = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=16, decimal_places=8)
    label = models.TextField(blank=True)
    confirmations = models.IntegerField()
    blockhash = models.CharField(max_length=64)
    blockindex = models.BigIntegerField()
    blocktime = models.BigIntegerField()
    txid = models.CharField(primary_key=True, max_length=64)
    vout = models.BigIntegerField()
    walletconflicts = models.TextField()
    time = models.BigIntegerField()
    timereceived = models.BigIntegerField()
    bip125replaceable = models.CharField(max_length=30)
    processed = models.BooleanField(default=False)

    def __unicode__(self):
        return  "[ BTC : "+ str(self.amount) +" ]"+self.txid +" [ Confirmations: " + str(self.confirmations) +"]"









