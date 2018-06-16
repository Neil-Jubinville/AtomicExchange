from models import Account

def getBitcoinAccount(hex):
    #print "return account " + hex
    return Account.objects.filter(bitcoinAddress=hex).first()