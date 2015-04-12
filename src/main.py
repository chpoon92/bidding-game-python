#!/usr/local/bin/python

import os
import random
import re
import sys

class Bidder:
    def __init__(self, id, bid):
        self.id = id
        self.bid = bid

def count_rounds():
    global current_round
    current_round = 1
    with open('result.txt', 'r') as input:
        input_str = input.readline().strip()
        while input_str:
            while not(input_str.startswith('end')):
                input_str = input.readline().strip()
            input_str = input.readline().strip()
            input_str = input.readline().strip()
            current_round += 1

def find_highest_bid_except_given_name(bidders, name):
    if len(bidders) == 0:
        return 0.0
    if len(bidders) == 1:
        return bidder.bid
    else:
        max_bid = -sys.maxint - 1
        for bidder in bidders:
            if bidder.bid > max_bid and bidder.id != name:
                max_bid = bidder.bid
        return max_bid

def find_highest_bid(bidders):
    max_bid = -sys.maxint - 1
    for bidder in bidders:
        if bidder.bid > max_bid:
            max_bid = bidder.bid
    return max_bid

def calculateBin():
    highest = find_highest_bid(last_last_bidders)
    for i in range(len(last_bidders)):
        last_bidders[i].bIn = last_bidders[i].bid - highest

def calculateBEx():
    for i in range(len(last_bidders)):
        last_bidders[i].bEx = last_bidders[i].bid - find_highest_bid_except_given_name(last_last_bidders, last_bidders[i].id)

def are_same(a, b):
    return abs(a - b) < 0.00001

def is_input_allowable(input):
    for i in range(len(bids)):
        if are_same(input, bids[i]):
            return i
    return -1

def initialize():
    global bidders_num
    global has_random_bidder
    global rounds
    global all_bids_are_announced
    global are_discrete_bids
    global bids
    with open('setup.txt', 'r') as input:
        bidders_num = input.readline().strip()
        has_random_bidder = (input.readline().strip() == '1')
        rounds = input.readline().strip()
        all_bids_are_announced = (input.readline().strip() == '1')
        bids_string = input.readline().strip()
        are_discrete_bids = bool(re.compile('^\{.+\}$').match(bids_string))
    bids = bids_string[1:len(bids_string)-1].split(',')
    for i in range(len(bids)):
        if re.compile('^\d+\/\d+$').match(bids[i]):
            bids[i] = float(bids[i].split('/')[0]) / float(bids[i].split('/')[1])
        bids[i] = float(bids[i])
    bids.sort()

def read_previous_rounds():
    global last_bidders
    global last_last_bidders
    last_bidders = []
    last_last_bidders = []
    with open('result.txt', 'r') as input:
        if current_round == 2:
            input_str = input.readline().strip()
            input_str = input.readline().strip()
            while not(input_str.startswith('end')):
                if not(input_str == '-'):
                    input_list = input_str.split(', ')
                    if input_list[1] == '-' or input_list[1] == '-1':
                        last_bidders.append(Bidder(input_list[0], float(0)))
                    else:
                        last_bidders.append(Bidder(input_list[0], float(input_list[1])))
                    input_str = input.readline().strip()
        elif current_round > 2:
            counter = 1
            input_str = input.readline().strip()
            while input_str and (counter != (current_round - 2)):
                while not(input_str.startswith('end')):
                    input_str = input.readline().strip()
                input_str = input.readline().strip()
                input_str = input.readline().strip()
                counter += 1
            input_str = input.readline().strip()
            while not(input_str.startswith('end')):
                if not(input_str == '-'):
                    input_list = input_str.split(', ')
                    if input_list[1] == '-' or input_list[1] == '-1':
                        last_last_bidders.append(Bidder(input_list[0], float(0)))
                    else:
                        last_last_bidders.append(Bidder(input_list[0], float(input_list[1])))
                input_str = input.readline().strip()
            input_str = input.readline().strip()
            input_str = input.readline().strip()
            input_str = input.readline().strip()
            while not(input_str.startswith('end')):
                if not(input_str == '-'):
                    input_list = input_str.split(', ')
                    if input_list[1] == '-' or input_list[1] == '-1':
                        last_bidders.append(Bidder(input_list[0], float(0)))
                    else:
                        last_bidders.append(Bidder(input_list[0], float(input_list[1])))
                input_str = input.readline().strip()

def bid():
    my_name = os.path.basename(__file__)[:len(os.path.basename(__file__)) - 3]
    if not has_random_bidder:
        if not are_discrete_bids:
            if current_round == 1:
                print bids[0] + 0.1 * (bids[1] - bids [0])
            elif current_round == 2:
                print min(find_highest_bid_except_given_name(last_bidders, my_name) + 0.05 * (bids[1] - bids [0]), 1)
            else:
                calculateBin()
                calculateBEx()
                max_bIn = -sys.maxint - 1
                for bidder in last_bidders:
                    if bidder.bIn > max_bIn:
                        max_bIn = bidder.bIn
                max_bEx = -sys.maxint - 1
                for bidder in last_bidders:
                    if bidder.bEx > max_bEx:
                        max_bEx = bidder.bEx
                max_b = max(max_bIn, max_bEx)
                if random.random() < 0.2:
                    if all_bids_are_announced:
                        print max(find_highest_bid_except_given_name(last_bidders, my_name) - 0.2 * (bids[1] - bids [0]), 0)
                    else:
                        if last_bidders[0].id == my_name:
                            print min(max(find_highest_bid_except_given_name(last_bidders, my_name) + max_b - 0.2 * (bids[1] - bids [0]), 0), 1)
                        else:
                            print find_highest_bid(last_bidders)
                else:
                    if all_bids_are_announced:
                        print min(find_highest_bid_except_given_name(last_bidders, my_name) + max_b + 0.05 * (bids[1] - bids [0]), 1)
                    else:
                        if last_bidders[0].id == my_name:
                            print min(find_highest_bid_except_given_name(last_bidders, my_name) + max_b + 0.05 * (bids[1] - bids [0]), 1)
                        else:
                            print find_highest_bid(last_bidders)
        else:
            if current_round == 1:
                print min(bids)
            else:
                if is_input_allowable(find_highest_bid_except_given_name(last_bidders, my_name)) != -1:
                    if random.random() < 0.2:
                        print bids[max(is_input_allowable(find_highest_bid_except_given_name(last_bidders, my_name)) - 1, 0)]
                    else:
                        print find_highest_bid_except_given_name(last_bidders, my_name)
                else:
                    print min(bids)
    else:
        if not are_discrete_bids:
            print random.uniform((bids[1] - bids[0]) / 2, bids[1])
        else:
            print bids[random.randint(len(bids) / 2, len(bids)) - 1]

def main():
    initialize()
    count_rounds()
    read_previous_rounds()
    bid()

if __name__ == '__main__':
    main()
