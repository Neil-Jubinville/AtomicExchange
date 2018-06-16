from django.shortcuts import render
from django.views.generic.base import View
from models import Account
from bitcoin.models import Transaction
import traceback
#import boto3


class Home(View):

    def get(self, request, *args, **kwargs):
        allAccounts = Account.objects.filter(visibility="overt");
        return render(request, 'index.html', {'accounts': allAccounts})

class ResetDB(View):

    def get(self, request, *args, **kwargs):

        #delete all the transactions and the covert accounts
        #leave the overt accounts but reset the balances
        Transaction.objects.all().delete()

        Account.objects.filter(visibility='covert').delete()

        #reset the know account balances for the next test round
        allAccounts =  Account.objects.filter(visibility="overt");
        for acc in allAccounts:
            acc.bitcoinBalance = 0.0
            acc.save()

        return render(request, 'index.html', {'accounts': allAccounts})