#Authors:  Neil Jubinville
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    owner = models.ForeignKey(User)
    visibility = models.CharField(max_length=30, default="covert")
    bitcoinAddress = models.CharField(max_length=64)
    bitcoinBalance = models.DecimalField(max_digits=16, decimal_places=8)
    ethereumAddress = models.CharField(max_length=64)
    ethereumBalance = models.DecimalField(max_digits=16, decimal_places=8)
    depositCount = models.BigIntegerField(default=0)
    pendingTx = models.TextField()
    latestTx = models.TextField()

    def __unicode__(self):
        return  self.owner.username +" -----  Bitcoin: " + str(self.bitcoinBalance)
