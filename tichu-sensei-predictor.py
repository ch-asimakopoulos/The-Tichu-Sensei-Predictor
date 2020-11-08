from flask import Flask, request
import sklearn
import json
import pickle
import numpy as np


#assigning values to cards
DOG = 0
JACK = 11
QUEEN = 12
KING = 13
ACE = 14
PHOENIX = 15
DRAGON = 16 




def translate_hand(cards): #translate_hand function which creates a 17-index array which counts how many cards of a kind a player has in his hand.
        hand=[0.0 for x in range(17)]
        for card in cards:
            if (card == 'Dr'):
                hand[DRAGON]=1
            elif (card == 'Ph'):
                hand[PHOENIX]=1
            elif (card == 'Hu'):
                hand[DOG]=1
            elif (card == 'Ma'):
                hand[1]=1
            elif ((card == 'GK') or (card == 'BK') or (card == 'SK') or (card == 'RK')):
                hand[KING]+=0.25
            elif ((card == 'GD') or (card == 'BD') or (card == 'SD') or (card == 'RD')):
                hand[QUEEN]+=0.25
            elif ((card == 'GB') or (card == 'BB') or (card == 'SB') or (card == 'RB')):
                hand[JACK]+=0.25
            elif ((card == 'GA') or (card == 'BA') or (card == 'SA') or (card == 'RA')):
                hand[ACE]+=0.25
            elif ((card == 'G10') or (card == 'B10') or (card == 'S10') or (card == 'R10')):
                hand[10]+=0.25
            elif ((card == 'G9') or (card == 'B9') or (card =='S9') or (card == 'R9')):
                hand[9]+=0.25
            elif ((card == 'G8') or (card == 'B8') or (card == 'S8') or (card == 'R8')):
                hand[8]+=0.25
            elif ((card == 'G7') or (card == 'B7') or (card == 'S7') or (card == 'R7')):
                hand[7]+=0.25
            elif ((card == 'G6') or (card == 'B6') or (card == 'S6') or (card == 'R6')):
                hand[6]+=0.25
            elif ((card == 'G5') or (card == 'B5') or (card == 'S5') or (card == 'R5')):
                hand[5]+=0.25
            elif ((card == 'G4') or (card == 'B4') or (card == 'S4') or (card == 'R4')):
                hand[4]+=0.25
            elif ((card == 'G3') or (card == 'B3') or (card == 'S3') or (card == 'R3')):
                hand[3]+=0.25
            elif ((card == 'G2') or (card == 'B2') or (card == 'S2') or (card == 'R2')):
                hand[2]+=0.25

        # sanity check
        sum=0
        for x in range(17):
            if(x<2 and hand[x] == 1):
                sum=sum+1
            elif(x>ACE and hand[x] ==1):
                sum=sum+1
            elif(hand[x]==0.25):
                sum=sum+1
            elif(hand[x]==0.5):
                sum=sum+2
            elif(hand[x]==0.75):
                sum=sum+3
            elif(hand[x]==1.0 and x>1 and x<PHOENIX):
                sum=sum+4
        return list(hand)

def find_steps(hand): #find_steps function which finds how many consecutive pairs a player has in his hand
    steps=[0.0 for x in range(14)]
    for i in range(13):
        if (hand[i+2] > 0.25 and hand[i+3] > 0.25):
                    steps[i+1] = steps[i]+1 #e.g 2 2 3 3 4 4 will give step[3] = 0+1 = 1 and step[4] = 1+1 = 2 which means I have 2 consecutive pairs below my 4 4 pair.
    for i in range(14):
            steps[i] = round((steps[i] / 3),3) #normalize (/6 when I have all 14 cards, but only /3 now since I have 8 cards available).
    steps.pop(0)   
    return list(steps)

def find_full_houses(hand):
    f_houses=[0.0 for x in range(15)]
    for i in range(13):
        if (hand[i+2] > 0.5):
            for j in range(13):
                if(not(j==i)):
                    if (hand[j+2]>0.25):
                        f_houses[i]=1
                        continue
    return list(f_houses)
        
        
def find_straights(hand): # find_straights function which finds how many straights a player has in his hand
    straights=[0.0 for x in range(11)]
    for i in range(10):
        if (hand[i+1]>0 and hand[i+2]>0 and hand[i+3]>0 and hand[i+4]>0 and hand[i+5]>0):
            straights[i+1] = straights[i]+1 #1 means a 5-straight with highest card equaling the value of the index, 2 means a 6-straight with highest card equaling the value of the index, 3 means a 7-straight and so on.
    for i in range(11):
            straights[i] = round((straights[i] / 4),3) #normalize. (/9 when we have 14 cards, but only /4 now since we have 8 cards.)
    straights.pop(0)   
    return list(straights)

def find_fourofakind(hand): #find_fourofakind function which finds number of four of a kind bombs in hand
    bombcount = 0.0
    for i in range(2,15):
        if(hand[i]>0.75):
            bombcount+=1
    bombcount = bombcount / 2 #normalize (max 3 bombs per hand, but only 2 when calling grand (as we have 8 cards!))
    return bombcount

def find_flushes_and_total_bombcount(cards): #find_flushes function which finds number of same-colored straights with the help of find_straights function and then add the total number of bombs in hand as the last element
    hand = translate_hand(cards)
    S=[0.0 for x in range(17)]
    R=[0.0 for x in range(17)]
    G=[0.0 for x in range(17)]
    B=[0.0 for x in range(17)]
    for card in cards:
                if (card=='SK'):
                    S[KING]+=1
                elif (card=='SD'):
                    S[QUEEN]+=1
                elif (card=='SB'):
                    S[JACK]+=1
                elif (card=='SA'):
                    S[ACE]+=1
                elif (card=='S10'):
                    S[10]+=1
                elif (card=='S9'):
                    S[9]+=1
                elif (card=='S8'):
                    S[8]+=1
                elif (card=='S7'):
                    S[7]+=1
                elif (card=='S6'):
                    S[6]+=1
                elif (card=='S5'):
                    S[5]+=1
                elif (card=='S4'):
                    S[4]+=1
                elif (card=='S3'):
                    S[3]+=1
                elif (card=='S2'):
                    S[2]+=1
                if (card=='RK'):
                    R[KING]+=1
                elif (card=='RD'):
                    R[QUEEN]+=1
                elif (card=='RB'):
                    R[JACK]+=1
                elif (card=='RA'):
                    R[ACE]+=1
                elif (card=='R10'):
                    R[10]+=1
                elif (card=='R9'):
                    R[9]+=1
                elif (card=='R8'):
                    R[8]+=1
                elif (card=='R7'):
                    R[7]+=1
                elif (card=='R6'):
                    R[6]+=1
                elif (card=='R5'):
                    R[5]+=1
                elif (card=='R4'):
                    R[4]+=1
                elif (card=='R3'):
                    R[3]+=1
                elif (card=='R2'):
                    R[2]+=1
                if (card=='GK'):
                    G[KING]+=1
                elif (card=='GK'):
                    G[QUEEN]+=1
                elif (card=='GB'):
                    G[JACK]+=1
                elif (card=='GA'):
                    G[ACE]+=1
                elif (card=='G10'):
                    G[10]+=1
                elif (card=='G9'):
                    G[9]+=1
                elif (card=='G8'):
                    G[8]+=1
                elif (card=='G7'):
                    G[7]+=1
                elif (card=='G6'):
                    G[6]+=1
                elif (card=='G5'):
                    G[5]+=1
                elif (card=='G4'):
                    G[4]+=1
                elif (card=='G3'):
                    G[3]+=1
                elif (card=='G2'):
                    G[2]+=1
                if (card=='BK'):
                    B[KING]+=1
                elif (card=='BD'):
                    B[QUEEN]+=1
                elif (card=='BB'):
                    B[JACK]+=1
                elif (card=='BA'):
                    B[ACE]+=1
                elif (card=='B10'):
                    B[10]+=1
                elif (card=='B9'):
                    B[9]+=1
                elif (card=='B8'):
                    B[8]+=1
                elif (card=='B7'):
                    B[7]+=1
                elif (card=='B6'):
                    B[6]+=1
                elif (card=='B5'):
                    B[5]+=1
                elif (card=='B4'):
                    B[4]+=1
                elif (card=='B3'):
                    B[3]+=1
                elif (card=='B2'):
                    B[2]+=1
    S_flush = find_straights(S)
    G_flush = find_straights(G)
    B_flush = find_straights(B)
    R_flush = find_straights(R)
    total_flush_sum = 0.0
    for i in range(9):
        if (S_flush[i+1] > S_flush[i]):
            total_flush_sum=total_flush_sum+1
        if (G_flush[i+1] > G_flush[i]):
            total_flush_sum=total_flush_sum+1
        if (B_flush[i+1] > B_flush[i]):
            total_flush_sum=total_flush_sum+1
        if (R_flush[i+1] > R_flush[i]):
            total_flush_sum=total_flush_sum+1
    flush_list = (S_flush+G_flush+B_flush+R_flush)
    total_bomb_count=[0.0 for x in range(0,1)]
    total_bomb_count[0] = (total_flush_sum + find_fourofakind(hand))
    return (flush_list+total_bomb_count)

app = Flask(__name__)
app.config['SECRET_KEY'] = "YOUR_SECRET_KEY"
@app.route('/predict/', methods=['GET'])
def predict():
    args = request.args
    apikey = args['apikey']
    payload = args['payload']
    if (apikey != str(app.config['SECRET_KEY'])):
        return str("Oops! Naughty call")       
    grTichuCallInfo = json.loads(payload)
    team_score=grTichuCallInfo["team_score"]
    #normalize scores.
    if (int(team_score) > 1000):
        team_score = str(1.0)
    elif (int(team_score) < -1000):
        team_score = str(0.0)
    elif (int(team_score) == 0):
        team_score = str(0.5)
    elif (int(team_score) < 0):
        team_score = str(round((((int(team_score)/1000) +1)/2),3))
    elif (int(team_score) > 0):
        team_score = str(round((((int(team_score)/1000) +1)/2),3))
    opp_score=grTichuCallInfo["opponent_team_score"]
    #normalize scores.
    if (int(opp_score) > 1000):
        opp_score = str(1.0)
    elif (int(opp_score) < -1000):
        opp_score = str(0.0)
    elif (int(opp_score) == 0):
        opp_score = str(0.5)
    elif (int(opp_score) < 0):
        opp_score = str(round((((int(opp_score)/1000) +1)/2),3))
    elif (int(opp_score) > 0):
        opp_score = str(round((((int(opp_score)/1000) +1)/2),3))
    hand = translate_hand(grTichuCallInfo["cards"]) #translates our cards to create the hand list
    steps = find_steps(hand) #finds consecutive pairs in our hand
    straights = find_straights(hand) #finds straights in our hand
    f_houses = find_full_houses(hand) #finds full houses in our hand
    flushes = find_flushes_and_total_bombcount(grTichuCallInfo["cards"]) #finds flushes  and total bomb count in our hand
    #!!! problem in normalizing bombcount_total, got to ask George! ( think bombcount won't go above 1 at 8 cards though! )
    #creating two files, which will be used to train and test our SVR predictor model.
    features_inplist = hand+steps+straights+f_houses+flushes
    features_inplist.insert(0, opp_score)
    features_inplist.insert(0, team_score)
    with open('svr_pred.pkl', 'rb') as f:
        clf = pickle.load(f) 
        inputdata = np.reshape(features_inplist, (1,98), order='C')
        output = clf.predict(inputdata)
        if(output >= grTichuCallInfo["threshold"]):
            return str("Sensei: YES")
        return str("Sensei: NO")
    return str("Sensei: NO")


if __name__ == 'main':
    app.run()