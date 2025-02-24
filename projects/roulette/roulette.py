#
# A simulation of Rhett's roulette strategy
#

import random
import pylab

def getOutcome():
    """
    Determines whether you win (13-36) or lose
    """
    #38 pockets (37 = 00)
    winner = random.randint(0,38)
    #print "winner: ",winner
    if winner >= 13 and winner <= 36:
        return 1
    else:
        return 0
                
def calcWin(wager):
    """
    Takes a wager amount, calls getOutcome and returns approprate loss/winnings
    """
    o = getOutcome()
    if o == 0:
        return -wager
    else:
        #print "winner!", (.5)*wager
        return ((36.0/24.0)-1.0)*wager
                
def playRounds(rounds,wallet,wager):
    """
    Takes int for number of rounds to play, starting amount of money, and wager
    amount, returns list of remaining money on each round
    """
    walletList = []
    #print "starting simulation..."
    while rounds > 0 and wallet >= wager:
        #print "round ",rounds," starting with ",wallet
        wallet += calcWin(wager)
        #print "new wallet", wallet
        walletList.append(wallet)
        rounds -= 1
    return walletList
        
#def graphSimulation(list):
        
def runSimulation(trials,rounds,wallet,wager):
    """
    Given ints/floats of trials (times to run simulation), rounds, a staring 
    amount of money, and a wager amount, returns a list average winnings per rounds over 
    all trials
    
    """
    origTrials = trials
    origWallet = wallet
    
    allWalletList = []
    for i in range(rounds):
        allWalletList.append(0.0)
    #print "walletList: ",allWalletList
    
    
    #endList = []
    #successes = 0.0
    #losses = 0.0
    #winningsList = []
    while trials > 0:
        tempList = playRounds(rounds,wallet,wager)
        #print "length",len(tempList)
        
        for i in range(len(tempList)):
            allWalletList[i]+=tempList[i]
        #print "printing",allWalletList
        
        
        #last = tempList[len(tempList)-1]
        #endList.append(last)
        #if last > origWallet:
        #    successes += 1
        #elif last < origWallet:
        #    losses += 1
        #winningsList.append(last)
        trials -=1
    #winnings = 0
    #for w in winningsList:
    #    winnings += w
        
    allWalletListAvg = []
    for i in range(len(allWalletList)):
        allWalletListAvg.append(allWalletList[i]/float(origTrials))
        
    #return endList, successes/float(origTrials), losses/float(origTrials), winnings-origTrials*origWallet,allWalletListAvg
    return allWalletListAvg
        
def producePlot(list):
    """
    Given a list of rounds of roulette (from runSimulation, presumably), produces graph
    """
    pylab.figure(1)
    pylab.plot(range(1,len(list)+1),list)
    pylab.title("Roulette using the 2/3 strategy")
    pylab.xlabel('round')
    pylab.ylabel('remaining funds')
    pylab.xlim([1,len(list)+1])
    pylab.show()        


#print playRounds(5,100,15)
producePlot(runSimulation(5000,1000,60,15))
