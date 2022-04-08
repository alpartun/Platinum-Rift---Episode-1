import sys
import math
import operator
import random
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# player_count: the amount of players (2 to 4)
# my_id: my player ID (0, 1, 2 or 3)
# zone_count: the amount of zones on the map
# link_count: the amount of links between all zones
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]
platinum_count = dict() # Create dict for calculating platinum points for each zones
for i in range(zone_count):
    # zone_id: this zone's ID (between 0 and zoneCount-1)
    # platinum_source: the amount of Platinum this zone can provide per game turn
    zone_id, platinum_source = [int(j) for j in input().split()]
    platinum_count[zone_id] = platinum_source #Adding each zones and each zones for platinum points to dict

linked_zones = dict()# Create dict for our zones connection
for i in range(link_count):
    zone_1, zone_2 = [int(j) for j in input().split()]
    if zone_1 in linked_zones :
        linked_zones[zone_1].append(zone_2) # if zone_1 is exists then add zone_2 bc they are connected
    else :
        linked_zones[zone_1] = [zone_2] # if zone_1 is not exists then create zone_1 and add zone_2 to our path
    if zone_2 in linked_zones :
        linked_zones[zone_2].append(zone_1) # same for zone_2
    else :
        linked_zones[zone_2] = [zone_1]

# game loop
control = 0

while True:
    platinum = int(input())  # my available Platinum
    my_states = set() #Create set for states that belongs to us.
    states = dict() #Create dict for zones and owner and pods.
    modify_platinum_count = {}

    for i in range(zone_count):
        # z_id: this zone's ID
        # owner_id: the player who owns this zone (-1 otherwise)
        # pods_p0: player 0's PODs on this zone
        # pods_p1: player 1's PODs on this zone
        # pods_p2: player 2's PODs on this zone (always 0 for a two player game)
        # pods_p3: player 3's PODs on this zone (always 0 for a two or three player game)
        z_id, owner_id, pods_p0, pods_p1, pods_p2, pods_p3 = [int(j) for j in input().split()]
        states[z_id] = [owner_id,pods_p0,pods_p1,pods_p2,pods_p3]#Adding zoneowners and pods that in states to dictionary.
        if owner_id == my_id : 
            my_states.add(z_id) # Adding zones that belongs to us to my_states
    
    if control > 3 :
        for z_id in states :
            owner_id,pods_p0,pods_p1,pods_p2,pods_p3 = states[z_id]

            if owner_id in (-1, my_id):
                m = linked_zones[z_id]
                for n in m :
                    if states[n][0] not in (-1,my_id):
                        modify_platinum_count[z_id] = (4+platinum_count[z_id])*3
                    else :
                        modify_platinum_count[z_id] = platinum_count[z_id]

            else :
                modify_platinum_count[z_id] = platinum_count[z_id] // 2



    control = control + 1
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    #Movement

    move = "" # Create empty move string
    for zone in my_states: # Looking for our zones
        next_zone = zone
        for adj in linked_zones[zone]: #looking for adjacent zones to our zone
            #next_zone = adj #next_zone becomes our adjacent zone
            if states[adj][0] != my_id :#if we have adjacent zone that not belongs to us then we should go and take there
                next_zone = adj
                break
            else :
                n = len(linked_zones[zone])
                m = random.randint(0,n-1)

                next_zone = linked_zones[zone][m]

        if next_zone != zone : #if initial zone (zone) is not equal to next_zone
            move = move + str(1) +" "+ str(zone) + " " + str (next_zone) + " " #we can add path zone to next_zone
    if not move : # If we have empty move string at the end
        print("WAIT") # we are going to wait
    else :        # if it is not empty 
        print(move) #then move !

    #Purchasement
    purchase = ""
    count = 0
    count2 = 0
    if control <= 3 :
        sorted_PC = sorted(platinum_count.items(), key = operator.itemgetter(1))#sorting our platinum_count dict  by items
    else :
        sorted_PC = sorted(modify_platinum_count.items(),key=operator.itemgetter(1))
    while platinum >= 20 and len(sorted_PC)>0: #if we have enough platinum and our sorted_PC is not empty we can purchase pods
        place_pod=sorted_PC.pop()[0] #we catch the zone that has higher platinum value
        if states[place_pod][0] in (-1, my_id) and count == 0: #we are looking for that zone (belong to us or nobody)
            platinum = platinum - 40 #then we can buy using platinum
            purchase = purchase + str(2) + " " + str(place_pod) + " " #so we can add that zone in our purchase string
            count = count + 1

        elif states[place_pod][0] in (-1, my_id) :
            if platinum > 40 :
                platinum = platinum - 40
                purchase = purchase + str(2)+ " " + str(place_pod)
            elif platinum < 40 :
                platinum = platinum - 20
                purchase = purchase + str(1) + " " + str(place_pod)
            


            

    if not purchase : # if purchase string is empty(we have no platinum or no place or the other places are taken) :(
        print("WAIT") # we must wait
    else :
        print(purchase) #purchase!!


    # first line for movement commands, second line for POD purchase (see the protocol in the statement for details)
