# Author: Neil Jubinville

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.base import View
from django.shortcuts import render
from AtomicExchange.settings import BASE_DIR
import simplejson as json
from models import Transaction
from AtomicExchange.models import Account
from django.contrib.auth.models import User
from django.db.models import Count, Min, Max, Sum, Avg
import BitcoinManager
import traceback
from django.core import serializers


class ListsinceblockView(View):

    def get(self, request, *args, **kwargs):
        # load the json output examples and process them.

        # In order to simulate the RPC call properly  we need to manage a
        # processed flag because depending on how the block gets assembled, some
        # transactions will appear in both listsinceblock calls.
        # This is properly simulated by making the manager update the balances
        # the tx processing flag after each simulated rpc call.



        # insert / save the first set
        fileTx1 =  open(BASE_DIR + '/data/transactions-1.json')
        fileString = fileTx1.read()
        txSet1 = json.loads(fileString)
        storeTransactions(txSet1['transactions'])

        BitcoinManager.validateSinceBlock()

        # insert / save the second set
        fileTx2 = open(BASE_DIR + '/data/transactions-2.json')
        fileString = fileTx2.read()
        txSet2 = json.loads(fileString)
        storeTransactions(txSet2['transactions'])

        BitcoinManager.validateSinceBlock()


        #sanity check, run a quick test to see how many txs come duplicated in the sequential call
        # compare the difference to the db total and json obj total
        #for tx2 in txSet2['transactions']:
            #for tx in txSet1['transactions']:
                #if ( tx['txid'] == tx2['txid']):
                    #print "TX: " +tx['txid']
        #allTx = Transaction.objects.all()
        #print "The total tx in the DB is " + str(len(allTx))

        ##---------------   All good - build up a summary struct for display -----------

        # get the data for the summary
        knownAccounts = Account.objects.filter(visibility="overt")
        unknownAccounts = Account.objects.filter(visibility="covert")

        # get the deposit count of the unknown valid transactions, easy.
        unknownValidTxSet = Transaction.objects.filter(category='receive', target=User.objects.filter(username='admin'),
                                                       processed=True)

        unknownValidTxCount = unknownValidTxSet.count()
        unknownValidAmount = unknownValidTxSet.aggregate(Sum('amount'))
        print "Unkown Valid Sum " + str(unknownValidAmount['amount__sum'])

        # smallest valid deposit including all known and unknown
        validTx = Transaction.objects.filter(processed=True, category='receive')

        print "The number of valid confirmed transactions in total is " + str(len(validTx))

        for n in validTx:
            if n.amount == 0:
                print "A ZERO TRANSFER really? yep, TXID" + n.txid

        smallestTransaction = validTx.aggregate(Min('amount'))['amount__min']
        largestTransaction = validTx.aggregate(Max('amount'))['amount__max']

        print "The smallest Tx is : " + str(smallestTransaction)
        print "The largest Tx is : " + str(largestTransaction)

        summary = {
            'knownAccounts':knownAccounts,
            'unknownValidTxCount': unknownValidTxCount,
            'unknownValidAmount' : unknownValidAmount['amount__sum'],
            'smallestTransaction': smallestTransaction,
            'largestTransaction': largestTransaction,
        }






        return render(request, 'listsinceblock.html', { 'summary':summary})


# utility function
def storeTransactions( jsonTxs):
    # avoid serializers for now since all the blockchains will be nuanced and transaction mappings are
    # likely to differ.
    #print "Set Size: " + str(len(jsonTxs))
  try:
    for tx in jsonTxs:

        #---------NEW ACCOUNT TEST ----------
        # check if we have an account registered with the address
        querySet = Account.objects.filter(bitcoinAddress=tx['address'])
        owner =None

        if (len(querySet) == 0):
            print('About to add a covert account for address: ' + tx['address'])
            # store the address as a 'covert' account
            acc = Account()
            acc.owner = User.objects.filter(username="admin")[0]
            acc.bitcoinAddress = tx['address']
            acc.bitcoinBalance = 0.0
            acc.ethereumAddress = "TBA"
            acc.ethereumBalance = 0.0
            acc.pendingTx = "[]"
            acc.latestTx = "[]"
            acc.save()

            owner = acc.owner
        else:
            owner = querySet.first().owner



        # -----------------------------------

        transaction = Transaction()
        transaction.target=owner
        transaction.involvesWatchonly = tx['involvesWatchonly']
        transaction.account = tx['account']
        transaction.address = tx['address']
        transaction.category = tx['category']
        transaction.amount = tx['amount']
        transaction.label = tx['label']
        transaction.confirmations = tx['confirmations']
        transaction.blockhash = tx['blockhash']
        transaction.blockindex = tx['blockindex']
        transaction.blocktime = tx['blocktime']
        transaction.txid = tx['txid']
        transaction.vout = tx['vout']
        transaction.walletconflicts = tx['walletconflicts']
        transaction.time = tx['time']
        transaction.timereceived = tx['timereceived']
        transaction.bip125replaceable = tx['bip125-replaceable']
        transaction.save()


        # since this is getting more interesting,  let's store the unknown accounts as well
        # even though the addresses may not be part of the exchange it can infer balances
        # and patterns in the future an discovery services! :)



  except:
    print traceback.print_exc()
