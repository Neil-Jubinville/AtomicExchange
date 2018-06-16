#Author:  Neil Jubinville

from models import Transaction
from AtomicExchange import AccountManager
from AtomicExchange.models import Account
from django.contrib.auth.models import User



def validateSinceBlock():
    print "---------------  listssinceblock verification -----------------"
    # get all the transactions with greater that 6 confirmations
    txs = Transaction.objects.filter(confirmations__gte = 6, category='receive')

    for t in txs:
        #print t.confirmations
        if( not t.processed):
            account = AccountManager.getBitcoinAccount(t.address)
            #print "account: " + str(account)
            balancePrior = account.bitcoinBalance
            newBalance = balancePrior + t.amount # this handles decreases as well adding the negatives
            account.bitcoinBalance = newBalance
            t.processed = 1
            account.depositCount = account.depositCount + 1
            account.save()
            t.save()













