import random
import pandas as pd
import math
from time import time as current_seed


def tt(sec=0,min=0,hour=0,day=0,month=0): #convert time to second
    tot_sec = sec + min*60 + hour*3600 + day*3600*24 + month*3600*24*30
    return tot_sec
'''def tt_inv(tot_sec):                #last function inverse 
    month=tot_sec//(3600*24*30)
    tot_sec=tot_sec%(3600*24*30)
    day=tot_sec//(3600*24)
    tot_sec=tot_sec%(3600*24)
    hour=tot_sec//(3600)
    tot_sec=tot_sec%(3600)
    min=tot_sec//(60)
    sec=tot_sec%(60)
    return sec,min,hour,day,month
'''
def expo_random(mean):                      #generate a random number by exponential distribution with a average equal to "mean"
    probability=random.random()
    return -mean*math.log(1-probability, math.e)

def uni_random(a,b):                        #generate a random number by uniform distribution between "a" and "b"
    probability = random.random()
    return min(a,b)+probability*(max(a,b)-min(a,b))

def discrete_random(a,b=0):
    probability = random.random()           #generate a random number by dosceret distribution between "a" and "b"
    generated_no=math.floor(probability*(max(a,b)-min(a,b)+1))+min(a,b)
    return generated_no


class Person:                               #for attribute and stats of each customer
    def __init__(self, index,arrival_time):
        self.i = index
        self.arrival_time = arrival_time    #when a customer call
        if random.random()<0.4:             #changed fro, 0.3 to 0.4
            A1=1                            # is this customer a VIP or not
        else:
            A1=0
        if random.random() < 0.5:
            A2 = 1                          # may this customer choose call-back option (it isn't needed any more)
        else:
            A2 = 0
        if random.random() < 0.15:
            A3 = 1                          # may this customer end (cancel) call in queue
        else:
            A3 = 0
        if random.random() < 0.15:          # does this customer need technical support
            A4 = 1
        else:
            A4 = 0
        self.type = A1
        self.call_back = A2
        self.impatient = A3
        self.tech_need = A4
        self.service_start_time = None      # when first (Expert/Beginner) clerk answer customer's call
        self.service_end_time = None
        self.leaving_queue_time = None      # time of cancel call by customer
        self.tech_service_start_time = None # technician answer customer's call
        self.tech_service_end_time = None
        self.did_left_queue = None          # did the customer cancel the call
        self.did_choose_call_back = None    # did the customer choose to call back
        self.first_queue = None             # first queue that customer stayed in
        self.second_queue = None            # thecnician queue that the customer stayed in


def starting_state(Expert_mean_service_time = tt(min= 3), Beginner_mean_service_time = tt(min= 7) ,max_Experts = 2 , max_Technician = 2 , max_Beginner = 3): #inputs for sensitivity analysis

    # State variables
        # Queue Length
    state = dict()
    state['max_Experts'] = max_Experts                              # for sensitivity analysis
    state['Expert_mean_service_time'] = Expert_mean_service_time
    state['Beginner_mean_service_time'] = Beginner_mean_service_time    # for sensitivity analysis
    state['max_Technician'] = max_Technician                        # for sensitivity analysis
    state['max_Beginner'] = max_Beginner
    state['VIP Queue Length'] = 0                   #QL1
    state['Normal Queue Length'] = 0                #QL2
    state['VIP call-back Queue Length'] = 0         #QL3
    state['Normal call-back Queue Length'] = 0      #QL4
    state['VIP technician Queue Length'] = 0        #QL5
    state['Normal technician Queue Length'] = 0     #QL6
        # Busy Operators
    state['Busy Beginners']=0       #BB: number of busy beginner operators      0,1,2,3
    state['Busy Experts'] = 0       #BE: number of busy EXPERT operators        0,1,2
    state['Busy Technicians'] = 0   #BT: number of busy technicians             0,1,2
        #other variables
    ### state['Work Shift'] = 1         #Sh: 1,2,3
    ### state['Network Error'] = 0      #NE: 0,1

    # Data: will save everything
    data = dict()
    data['Customer_number'] = 1 #to handle cold-start
    data['No3000_time'] = None
    data['Customers'] = dict()  # To track each customer, saving their arrival time, time service begins, etc.
    data['Last Time Queue1 Length Changed'] = 0     # Needed to calculate area under queue1 length curve
    data['Last Time Queue2 Length Changed'] = 0     # Needed to calculate area under queue2 length curve
    ##data['Last Time Queue3 Length Changed'] = 0     # Needed to calculate area under queue3 length curve
    ##data['Last Time Queue4 Length Changed'] = 0     # Needed to calculate area under queue4 length curve
    data['Last Time Queue5 Length Changed'] = 0     # Needed to calculate area under queue5 length curve
    data['Last Time Queue6 Length Changed'] = 0     # Needed to calculate area under queue6 length curve
    data['Queue1 Customers'] = dict()   # VIP Customer: Arrival Time, used to find first customer in queue
    data['Queue2 Customers'] = dict()   # Normal Customer: Arrival Time, used to find first customer in queue
    ##data['Queue3 Customers'] = dict()   # VIP call-back Customer: Arrival Time, used to find first customer in queue
    ##data['Queue4 Customers'] = dict()   # Normal call-back Customer: Arrival Time, used to find first customer in queue
    data['Queue5 Customers'] = dict()   # VIP technician Customer: Arrival Time, used to find first customer in queue
    data['Queue6 Customers'] = dict()   # Normal technician Customer: Arrival Time, used to find first customer in queue

    # Cumulative Stats
    data['Cumulative Stats'] = dict()
    data['Cumulative Stats']['In-system VIP Time'] = 0              #duration of time that a VIP (all kind) stay in system (not for customers who chooses call-back)
    data['Cumulative Stats']['In-system VIP no-tech-need Time'] = 0 #duration of time that a VIP (who doesn't need technical support) stay in system (not for customers who chooses call-back)
    data['Cumulative Stats']['In-system VIP tech-need Time'] = 0    #duration of time that a VIP (who needs technical support) stay in system (not for customers who chooses call-back)


    data['Cumulative Stats']['No waiting no-tech-need VIP'] = 0      # number of VIP customers (who doesn't need technical support) that didn't stay in queue at all
    data['Cumulative Stats']['No waiting tech-need VIP'] = 0        # number of VIP customers (who needs technical support) that didn't stay in queue at all



    data['Cumulative Stats']['Max QL1'] = 0         #max value af QL1
    data['Cumulative Stats']['Max QL2'] = 0         #max value af QL2
    ##data['Cumulative Stats']['Max QL3'] = 0         #max value af QL3
    ##data['Cumulative Stats']['Max QL4'] = 0         #max value af QL4
    data['Cumulative Stats']['Max QL5'] = 0         #max value af QL5
    data['Cumulative Stats']['Max QL6'] = 0         #max value af QL6

    data['Cumulative Stats']['Area Under Queue1 Length Curve'] = 0      #it's obvious
    data['Cumulative Stats']['Area Under Queue2 Length Curve'] = 0
    ##data['Cumulative Stats']['Area Under Queue3 Length Curve'] = 0
    ##data['Cumulative Stats']['Area Under Queue4 Length Curve'] = 0
    data['Cumulative Stats']['Area Under Queue5 Length Curve'] = 0
    data['Cumulative Stats']['Area Under Queue6 Length Curve'] = 0

    data['Cumulative Stats']['Queue2 Waiting Times list'] = list()
    data['Cumulative Stats']['Queue1 Waiting Time'] = 0 #total time of customers' wait in Queue1 (it calculates when a clerk answer them)
    data['Cumulative Stats']['Queue1 Finishers'] = 0    #count of customers who wait in Queue1
    data['Cumulative Stats']['Queue2 Waiting Time'] = 0 #total time of customers' wait in Queue2 (it calculates when a clerk answer them)
    data['Cumulative Stats']['Queue2 Finishers'] = 0    #count of customers who wait in Queue2
    ##data['Cumulative Stats']['Queue3 Waiting Time'] = 0 #total time of customers' wait in Queue3 (it calculates when a clerk answer them)
    ##data['Cumulative Stats']['Queue3 Finishers'] = 0    #count of customers who wait in Queue3
    ##data['Cumulative Stats']['Queue4 Waiting Time'] = 0 #total time of customers' wait in Queue4 (it calculates when a clerk answer them)
    ##data['Cumulative Stats']['Queue4 Finishers'] = 0    #count of customers who wait in Queue4
    data['Cumulative Stats']['Queue5 Waiting Time'] = 0 #total time of customers' wait in Queue5 (it calculates when a clerk answer them)
    data['Cumulative Stats']['Queue5 Finishers'] = 0    #count of customers who wait in Queue5
    data['Cumulative Stats']['Queue6 Waiting Time'] = 0 #total time of customers' wait in Queue6 (it calculates when a clerk answer them)
    data['Cumulative Stats']['Queue6 Finishers'] = 0    #count of customers who wait in Queue6

    data['Cumulative Stats']['Normal Finishers'] = 0            #Number of tech-need Normal customers who recieve service
    data['Cumulative Stats']['VIP Finishers'] = 0               #Number of tech-need Normal customers who recieve service
    ##data['Cumulative Stats']['Normal call-back Finishers'] = 0  #Number of tech-need Normal customers who recieve service
    ##data['Cumulative Stats']['VIP call-back Finishers'] = 0     #Number of tech-need Normal customers who recieve service
    data['Cumulative Stats']['Normal tech-need Finishers'] = 0  #Number of tech-need Normal customers who recieve service
    data['Cumulative Stats']['VIP tech-need Finishers'] = 0     #Number of tech-need Normal customers who recieve service


    data['Cumulative Stats']['Beginner Busy Time'] = 0          #sum of time that Biginners are busy
    data['Cumulative Stats']['Expert Busy Time'] = 0            #sum of time that Expert are busy
    data['Cumulative Stats']['Technician Busy Time'] = 0        #sum of time that Technician are busy


    data['Cumulative Stats']['ended-call by VIP'] = 0           #Number of VIP customers who cancel the call
    data['Cumulative Stats']['ended-call by Normal'] = 0        #Number of Normal customers who cancel the call

    # for distributions validation
    # data['count'] ={}
    # data['count']['no-tech-need VIP'] = 0
    # data['count']['no-tech-need Normal'] = 0
    # data['count']['tech-need VIP'] = 0
    # data['count']['tech-need Normal'] = 0
    # data['time'] = {'interval':{1:dict() , 2:dict() , 3:dict() }}
    # data['time']['interval'][1][0] = list()
    # data['time']['interval'][2][0] = list()
    # data['time']['interval'][3][0] = list()
    # data['time']['interval'][1][1] = list()
    # data['time']['interval'][2][1] = list()
    # data['time']['interval'][3][1] = list()
    # data['service time']={}
    # data['service time']['Beginner'] = []
    # data['service time']['Expert'] = []
    # data['service time']['Technician'] = []






    # Starting FEL  (obvious)
    future_event_list = list()
    future_event_list.append({'Event Type': 'Arrival', 'Event Time': 0, 'Customer': 'C1'})
    ##fel_maker(future_event_list, 'Change work shift', 0, state, data)
    ##fel_maker(future_event_list,'Start of Network Error',0,state,data)
    ##fel_maker(future_event_list, 'Change month', 0, state, data)

    return state, future_event_list, data


def fel_maker(future_event_list, event_type, clock, state ,data, customer=None):
    # we input event type (and customer) and it determines the time of event and adds it to FEL

    event_time = 0
    ##WS = state['Work Shift']
    ##NE = state['Network Error']
    if event_type == 'Arrival':                 #determine that when next customer arrives
        event_time = clock + expo_random(66)
        '''if WS==1 and NE==0:
            event_time = clock + expo_random (180)
        elif WS==2 and NE==0:
            event_time = clock + expo_random(60)
        elif WS==3 and NE==0:
            event_time = clock + expo_random(120)
        elif WS==1 and NE==1:
            event_time = clock + expo_random(120)
        elif WS==2 and NE==1:
            event_time = clock + expo_random(30)
        elif WS==3 and NE==1:
            event_time = clock + expo_random(60)'''
        # data['time']['interval'][WS][NE].append(event_time- clock)
    elif event_type == 'End of Service by Beginner':
        event_time = clock + expo_random(state['Beginner_mean_service_time'])
        # data['service time']['Beginner'].append(event_time- clock)
    elif event_type == 'End of Service by Expert':
        event_time = clock + expo_random(state['Expert_mean_service_time'])
        # data['service time']['Expert'].append(event_time- clock)
    elif event_type == 'End of Service by Technician':
        event_time = clock + expo_random(600)
        # data['service time']['Technician'].append(event_time - clock)
    ## elif event_type == 'Change work shift':
    ##     event_time = clock + tt(hour=8)
    ## elif event_type == 'Change month':
    ##     event_time = clock + tt(month=1)
    elif event_type == 'End call by customer':
        if data['Customers'][customer].type==1:
            event_time = clock + uni_random(300, max(tt(min=25), tt(min=state['VIP Queue Length'])))
        else:
            event_time = clock + uni_random(300, max(tt(min=25), tt(min=state['Normal Queue Length'])))
    ##elif event_type == 'Start of Network Error':
    ##    event_time = clock + tt(day=discrete_random(29))
    ##elif event_type == 'End of Network Error':
    ##    event_time = clock + tt(day=1)


    new_event = {'Event Type': event_type, 'Event Time': event_time, 'Customer': customer}
    future_event_list.append(new_event)

'''def change_shift(future_event_list, state, clock, data):  #makes needed changes when "change shift event" happens
    last_shift = state['Work Shift']
    if last_shift==1:
        state['Work Shift'] = 2
    elif last_shift==2:
        state['Work Shift'] = 3
    else:
        state['Work Shift'] = 1
    fel_maker(future_event_list,'Change work shift',clock,state,data)

def change_month(future_event_list, state, clock, data):    # determine day of network error in new month
    fel_maker(future_event_list,'Start of Network Error',clock,state,data)
    fel_maker(future_event_list,'Change month',clock,state,data)

def start_network_error(future_event_list, state, clock, data): #changes NE to 1 and makes end of network error event
    state['Network Error']=1
    fel_maker(future_event_list,'End of Network Error',clock,state,data)
def end_network_error(future_event_list, state, clock, data):   #changes NE to 0
    state['Network Error']=0'''


def arrival(future_event_list, state, clock, data, customer):
    index=int(customer[1:])
    data['Customers'][customer] = Person(index,clock)           #create customer class


    # for distributions validation
    # if data['Customers'][customer].type == 1 and data['Customers'][customer].tech_need == 0:
    #     data['count']['no-tech-need VIP']+=1
    # elif data['Customers'][customer].type == 0 and data['Customers'][customer].tech_need == 0:
    #     data['count']['no-tech-need Normal']+=1
    # elif data['Customers'][customer].type == 1 and data['Customers'][customer].tech_need == 1:
    #     data['count']['tech-need VIP']+=1
    # elif data['Customers'][customer].type == 0 and data['Customers'][customer].tech_need == 1:
    #     data['count']['tech-need Normal']+=1
    if data['Customers'][customer].type == 1:                   #if a VIP customer calls
        if state['Busy Experts'] <state['max_Experts']:                            #if we have idle Expert
            data['Customers'][customer].service_start_time=clock
            state['Busy Experts']+=1
            if data['Customer_number']>3000:
                data['Cumulative Stats']['Queue1 Finishers'] += 1
            fel_maker(future_event_list,'End of Service by Expert',clock,state,data,customer)
        else:                                                   #if we don't have idle Expert
            ## if data['Customers'][customer].call_back==1 and state['VIP Queue Length']>4:      #dose customer choose call-back
            ##     data['Cumulative Stats']['Area Under Queue3 Length Curve'] += ((clock - data['Last Time Queue3 Length Changed'])*state['VIP call-back Queue Length'])
            ##     data['Last Time Queue3 Length Changed'] = clock
            ##     state['VIP call-back Queue Length']+=1
            ##     data['Cumulative Stats']['Max QL3'] = max(data['Cumulative Stats']['Max QL3'] , state['VIP call-back Queue Length'])
            ##     data['Customers'][customer].did_choose_call_back = 1
            ##     data['Queue3 Customers'][customer]=clock
            ##     data['Customers'][customer].first_queue = 3
            ## else:                                               #when VIP customer stay in Queue1
            if data['Customer_number'] > 3000:
                data['Cumulative Stats']['Area Under Queue1 Length Curve'] += ((clock - data['Last Time Queue1 Length Changed']) * state['VIP Queue Length'])
                data['Last Time Queue1 Length Changed'] = clock
                data['Cumulative Stats']['Max QL1'] = max(data['Cumulative Stats']['Max QL1'] , state['VIP Queue Length'])
            state['VIP Queue Length'] += 1
            data['Customers'][customer].did_choose_call_back = 0
            data['Queue1 Customers'][customer] = clock
            data['Customers'][customer].first_queue = 1
            if data['Customers'][customer].impatient==1:    #create end call by customer event if customer is impatient
                fel_maker(future_event_list,'End call by customer',clock,state,data,customer)
    else:                                                       #if a Normal customer calls
        if state['Busy Beginners']<state['max_Beginner']:                           #if we have idle Beginner
            data['Customers'][customer].service_start_time=clock
            if data['Customer_number'] > 3000:
                data['Cumulative Stats']['Queue2 Finishers'] += 1
                data['Cumulative Stats']['Queue2 Waiting Times list'].append(0)
            state['Busy Beginners']+=1
            fel_maker(future_event_list,'End of Service by Beginner',clock,state,data,customer)
        else:
            if state['Busy Experts'] < state['max_Experts']:                       #if we have idle Expert
                data['Customers'][customer].service_start_time = clock
                state['Busy Experts']+=1
                fel_maker(future_event_list, 'End of Service by Expert', clock, state, data, customer)
            else:
                '''if data['Customers'][customer].call_back==1 and state['Normal Queue Length']>4:     #does customer choose call-back?
                    data['Cumulative Stats']['Area Under Queue4 Length Curve'] += ((clock - data['Last Time Queue4 Length Changed']) * state['Normal call-back Queue Length'])
                    data['Last Time Queue4 Length Changed'] = clock
                    state['Normal call-back Queue Length']+=1
                    data['Cumulative Stats']['Max QL4'] = max(data['Cumulative Stats']['Max QL4'],state['Normal call-back Queue Length'])
                    data['Customers'][customer].did_choose_call_back = 1
                    data['Queue4 Customers'][customer] = clock
                    data['Customers'][customer].first_queue = 4
                else:                                              #when Normal customer stay in Queue2'''
                if data['Customer_number'] > 3000:
                    data['Cumulative Stats']['Area Under Queue2 Length Curve'] += ((clock - data['Last Time Queue2 Length Changed']) * state['Normal Queue Length'])
                    data['Last Time Queue2 Length Changed'] = clock
                    data['Cumulative Stats']['Max QL2'] = max(data['Cumulative Stats']['Max QL2'],state['Normal Queue Length'])
                state['Normal Queue Length'] += 1
                data['Customers'][customer].did_choose_call_back = 0
                data['Queue2 Customers'][customer] = clock
                data['Customers'][customer].first_queue = 2
                if data['Customers'][customer].impatient == 1:
                    fel_maker(future_event_list, 'End call by customer', clock, state, data, customer)

    next_customer = 'C' + str(int(customer[1:]) + 1)                #make arrival event for next customer
    fel_maker(future_event_list, 'Arrival', clock, state, data, next_customer)



def end_service_by_beginner(future_event_list, state, clock, data, customer):
    # calculate stats
    ##if data['Customers'][customer].did_choose_call_back == 1:
    ##    data['Cumulative Stats']['Normal call-back Finishers'] +=1
    ##else:
    if data['Customer_number'] > 3000:
        data['Cumulative Stats']['Normal Finishers'] +=1
    data['Customers'][customer].service_end_time = clock
    if data['Customer_number'] > 3000:
        data['Cumulative Stats']['Beginner Busy Time'] += (clock -data['Customers'][customer].service_start_time )

    # connect current customer to tech department or finish call
    if data['Customers'][customer].tech_need == 1:
        if state['Busy Technicians'] < state['max_Technician']:
            state['Busy Technicians']+=1
            data['Customers'][customer].tech_service_start_time = clock
            fel_maker(future_event_list,'End of Service by Technician',clock,state,data,customer)
        else:
            if data['Customer_number'] > 3000:
                data['Cumulative Stats']['Area Under Queue6 Length Curve'] += ((clock - data['Last Time Queue6 Length Changed']) * state['Normal technician Queue Length'])
                data['Last Time Queue6 Length Changed'] = clock
                data['Cumulative Stats']['Max QL6'] = max(data['Cumulative Stats']['Max QL6'], state['Normal technician Queue Length'])
            state['Normal technician Queue Length'] += 1
            data['Customers'][customer].second_queue = 6
            data['Queue6 Customers'][customer] = clock

    #   select new customer to answer
    if state['Normal Queue Length'] > 0:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Area Under Queue2 Length Curve'] += ((clock - data['Last Time Queue2 Length Changed']) * state['Normal Queue Length'])
            data['Last Time Queue2 Length Changed'] = clock
        state['Normal Queue Length'] -= 1
        next_customer = min(data['Queue2 Customers'], key=data['Queue2 Customers'].get)
        data['Queue2 Customers'].pop(next_customer)
        data['Customers'][next_customer].service_start_time = clock
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Queue2 Waiting Times list'].append(clock - data['Customers'][next_customer].arrival_time )
            data['Cumulative Stats']['Queue2 Waiting Time'] += (clock - data['Customers'][next_customer].arrival_time )
            data['Cumulative Stats']['Queue2 Finishers'] +=1
        fel_maker(future_event_list, 'End of Service by Beginner', clock, state, data, next_customer)
        if data['Customers'][next_customer].impatient == 1: #if we made a event for end call by customer, now we delete it.
            data['Customers'][next_customer].did_left_queue = 0
            del future_event_list[future_event_list.index(next(item for item in future_event_list if item["Customer"] == next_customer and item['Event Type']=='End call by customer'))]
    else: #if it isn't first shift, start calling-back to customers
        '''if state['Work Shift']>1 and state['Normal call-back Queue Length']>0:
            data['Cumulative Stats']['Area Under Queue4 Length Curve'] += ((clock - data['Last Time Queue4 Length Changed']) * state['Normal call-back Queue Length'])
            data['Last Time Queue4 Length Changed'] = clock
            state['Normal call-back Queue Length'] -= 1
            next_customer = min(data['Queue4 Customers'], key=data['Queue4 Customers'].get)
            data['Queue4 Customers'].pop(next_customer)
            data['Customers'][next_customer].service_start_time = clock
            data['Cumulative Stats']['Queue4 Waiting Time'] += (clock - data['Customers'][next_customer].arrival_time)
            data['Cumulative Stats']['Queue4 Finishers'] += 1
            fel_maker(future_event_list, 'End of Service by Beginner', clock, state, data, next_customer)
        else: #if there is no Normal customer in Queue, then we have one more idle Beginner'''
        state['Busy Beginners'] -=1



def end_service_by_expert(future_event_list, state, clock, data, customer):
    #like begginer but for Expert we check Queue of Normal and VIP both.
    if data['Customers'][customer].type == 1:
        ##if data['Customers'][customer].did_choose_call_back == 1:
        ##    data['Cumulative Stats']['VIP call-back Finishers'] += 1
        ##else:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['VIP Finishers'] += 1
    else:
        ##if data['Customers'][customer].did_choose_call_back == 1:
        ##    data['Cumulative Stats']['Normal call-back Finishers'] += 1
        ##else:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Normal Finishers'] += 1
    data['Customers'][customer].service_end_time = clock
    if data['Customer_number'] > 3000:
        data['Cumulative Stats']['Expert Busy Time'] += (clock - data['Customers'][customer].service_start_time)
    if data['Customers'][customer].tech_need == 1 :
        if state['Busy Technicians'] < state['max_Technician']:
            state['Busy Technicians']+=1
            data['Customers'][customer].tech_service_start_time = clock
            fel_maker(future_event_list,'End of Service by Technician',clock,state,data,customer)
        else:
            if data['Customers'][customer].type == 1:
                if data['Customer_number'] > 3000:
                    data['Cumulative Stats']['Area Under Queue5 Length Curve'] += ((clock - data['Last Time Queue5 Length Changed']) * state['VIP technician Queue Length'])
                    data['Last Time Queue5 Length Changed'] = clock
                    data['Cumulative Stats']['Max QL5'] = max(data['Cumulative Stats']['Max QL5'],state['VIP technician Queue Length'])
                state['VIP technician Queue Length'] += 1
                data['Queue5 Customers'][customer] = clock
                data['Customers'][customer].second_queue = 5
            else:
                if data['Customer_number'] > 3000:
                    data['Cumulative Stats']['Area Under Queue6 Length Curve'] += ((clock - data['Last Time Queue6 Length Changed']) * state['Normal technician Queue Length'])
                    data['Last Time Queue6 Length Changed'] = clock
                    data['Cumulative Stats']['Max QL6'] = max(data['Cumulative Stats']['Max QL6'],state['Normal technician Queue Length'])
                state['Normal technician Queue Length'] += 1

                data['Queue6 Customers'][customer] = clock
                data['Customers'][customer].second_queue = 6
    else:
        if data['Customers'][customer].type == 1 and data['Customers'][customer].did_choose_call_back != 1:
            if data['Customer_number'] > 3000:
                data['Cumulative Stats']['In-system VIP Time'] += (clock -data['Customers'][customer].arrival_time )
                data['Cumulative Stats']['In-system VIP no-tech-need Time'] += (clock - data['Customers'][customer].arrival_time)

        if  data['Customers'][customer].type == 1 and data['Customers'][customer].first_queue == None :
            if data['Customer_number'] > 3000:
                data['Cumulative Stats']['No waiting no-tech-need VIP'] +=1

    if state['VIP Queue Length'] > 0:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Area Under Queue1 Length Curve'] += ((clock - data['Last Time Queue1 Length Changed']) * state['VIP Queue Length'])
            data['Last Time Queue1 Length Changed'] = clock
        state['VIP Queue Length'] -= 1
        next_customer = min(data['Queue1 Customers'], key=data['Queue1 Customers'].get)
        data['Queue1 Customers'].pop(next_customer)
        data['Customers'][next_customer].service_start_time = clock
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Queue1 Waiting Time'] += (clock - data['Customers'][next_customer].arrival_time )
            data['Cumulative Stats']['Queue1 Finishers'] +=1
        fel_maker(future_event_list, 'End of Service by Expert', clock, state, data, next_customer)
        if data['Customers'][next_customer].impatient == 1:
            data['Customers'][next_customer].did_left_queue = 0
            del future_event_list[future_event_list.index(next(item for item in future_event_list if item["Customer"] == next_customer and item['Event Type'] == 'End call by customer'))]
    else:
        if state['Normal Queue Length'] > 0:
            if data['Customer_number'] > 3000:
                data['Cumulative Stats']['Area Under Queue2 Length Curve'] += ((clock - data['Last Time Queue2 Length Changed']) * state['Normal Queue Length'])
                data['Last Time Queue2 Length Changed'] = clock
            state['Normal Queue Length'] -= 1
            next_customer = min(data['Queue2 Customers'], key=data['Queue2 Customers'].get)
            data['Queue2 Customers'].pop(next_customer)
            data['Customers'][next_customer].service_start_time = clock
            if data['Customer_number'] > 3000:
                data['Cumulative Stats']['Queue2 Waiting Times list'].append(clock - data['Customers'][next_customer].arrival_time)
                data['Cumulative Stats']['Queue2 Waiting Time'] += (clock - data['Customers'][next_customer].arrival_time)
                data['Cumulative Stats']['Queue2 Finishers'] +=1
            fel_maker(future_event_list, 'End of Service by Expert', clock, state, data, next_customer)
            if data['Customers'][next_customer].impatient == 1:
                data['Customers'][next_customer].did_left_queue = 0
                del future_event_list[future_event_list.index(next(item for item in future_event_list if item["Customer"] == next_customer and item['Event Type']=='End call by customer'))]
        else:
            '''if state['Work Shift']>1 :
                if state['VIP call-back Queue Length']>0:
                    data['Cumulative Stats']['Area Under Queue3 Length Curve'] += ((clock - data['Last Time Queue3 Length Changed']) * state['VIP call-back Queue Length'])
                    data['Last Time Queue3 Length Changed'] = clock
                    state['VIP call-back Queue Length'] -= 1
                    next_customer = min(data['Queue3 Customers'], key=data['Queue3 Customers'].get)
                    data['Queue3 Customers'].pop(next_customer)
                    data['Customers'][next_customer].service_start_time = clock
                    data['Cumulative Stats']['Queue3 Waiting Time'] += (clock - data['Customers'][next_customer].arrival_time)
                    data['Cumulative Stats']['Queue3 Finishers'] += 1
                    fel_maker(future_event_list, 'End of Service by Expert', clock, state, data, next_customer)
                else:
                    if state['Normal call-back Queue Length']>0:
                        data['Cumulative Stats']['Area Under Queue4 Length Curve'] += ((clock - data['Last Time Queue4 Length Changed']) * state['Normal call-back Queue Length'])
                        data['Last Time Queue4 Length Changed'] = clock
                        state['Normal call-back Queue Length'] -= 1
                        next_customer = min(data['Queue4 Customers'], key=data['Queue4 Customers'].get)
                        data['Queue4 Customers'].pop(next_customer)
                        data['Customers'][next_customer].service_start_time = clock
                        data['Cumulative Stats']['Queue4 Waiting Time'] += (clock - data['Customers'][next_customer].arrival_time)
                        data['Cumulative Stats']['Queue4 Finishers'] += 1
                        fel_maker(future_event_list, 'End of Service by Expert', clock, state, data, next_customer)
                    else:
                        state['Busy Experts'] -=1

            else:'''
            state['Busy Experts'] -=1



def end_service_by_technician(future_event_list, state, clock, data, customer):
    #it's like what was for Beginner or Expert but fot Technician call finishes for all customers and only tech-need Queues are checked.
    if data['Customers'][customer].type == 1:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['VIP tech-need Finishers'] += 1
    else:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Normal tech-need Finishers'] += 1
    if data['Customers'][customer].type == 1 and data['Customers'][customer].first_queue == None and data['Customers'][customer].second_queue == None:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['No waiting tech-need VIP'] +=1
    data['Customers'][customer].tech_service_end_time = clock
    if data['Customer_number'] > 3000:
        data['Cumulative Stats']['Technician Busy Time'] += (clock - data['Customers'][customer].tech_service_start_time)
    if data['Customers'][customer].type == 1 and data['Customers'][customer].did_choose_call_back != 1:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['In-system VIP tech-need Time'] +=(clock -  data['Customers'][customer].arrival_time)
            data['Cumulative Stats']['In-system VIP Time'] += (clock - data['Customers'][customer].arrival_time)

    if state['VIP technician Queue Length']>0:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Area Under Queue5 Length Curve'] += ((clock - data['Last Time Queue5 Length Changed']) * state['VIP technician Queue Length'])
            data['Last Time Queue5 Length Changed'] = clock
        state['VIP technician Queue Length']-=1
        next_customer = min(data['Queue5 Customers'], key=data['Queue5 Customers'].get)
        data['Queue5 Customers'].pop(next_customer)
        data['Customers'][next_customer].tech_service_start_time = clock
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Queue5 Waiting Time'] += (clock - data['Customers'][next_customer].arrival_time )
            data['Cumulative Stats']['Queue5 Finishers'] += 1
        fel_maker(future_event_list, 'End of Service by Technician', clock, state, data, next_customer)
    else:
        if state['Normal technician Queue Length']>0:
            if data['Customer_number'] > 3000:
                data['Cumulative Stats']['Area Under Queue6 Length Curve'] += ((clock - data['Last Time Queue6 Length Changed']) * state['Normal technician Queue Length'])
                data['Last Time Queue6 Length Changed'] = clock
            state['Normal technician Queue Length']-=1
            next_customer = min(data['Queue6 Customers'], key=data['Queue6 Customers'].get)
            data['Customers'][next_customer].tech_service_start_time = clock
            data['Queue6 Customers'].pop(next_customer)
            if data['Customer_number'] > 3000:
                data['Cumulative Stats']['Queue6 Waiting Time'] += (clock - data['Customers'][next_customer].arrival_time)
                data['Cumulative Stats']['Queue6 Finishers'] += 1
            fel_maker(future_event_list, 'End of Service by Technician', clock, state, data, next_customer)
        else:
            state['Busy Technicians']-=1

def end_call_by_customer(future_event_list, state, clock, data, customer):
    #it is for impatient customers who ends call after a while
    #calculate some stats
    if data['Customers'][customer].type ==1:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['ended-call by VIP'] +=1
    else:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['ended-call by Normal'] +=1
    #record some data for the customer
    data['Customers'][customer].leaving_queue_time = clock
    data['Customers'][customer].did_left_queue = 1
    #calculate some stats and remove customer from Queue
    if data['Customers'][customer].type == 1:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Area Under Queue1 Length Curve'] += ((clock - data['Last Time Queue1 Length Changed']) * state['VIP Queue Length'])
            data['Last Time Queue1 Length Changed'] = clock
        state['VIP Queue Length'] -= 1
        data['Queue1 Customers'].pop(customer)
    else:
        if data['Customer_number'] > 3000:
            data['Cumulative Stats']['Area Under Queue2 Length Curve'] += ((clock - data['Last Time Queue2 Length Changed']) * state['Normal Queue Length'])
            data['Last Time Queue2 Length Changed'] = clock
        state['Normal Queue Length'] -= 1
        data['Queue2 Customers'].pop(customer)



def create_row(step, current_event, state, data, future_event_list):
    # This function will create a list, which will eventually become a row of the output Excel file

    sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'])

    # What should this row contain?
    # 1. Step, Clock, Event Type and Event Customer
    if current_event['Customer'] is not None:
        row = [step, current_event['Event Time'], current_event['Event Type'], current_event['Customer']+', '+str(data['Customers'][current_event['Customer']].type) +', '+str(data['Customers'][current_event['Customer']].call_back) +', '+str(data['Customers'][current_event['Customer']].impatient) +', '+str(data['Customers'][current_event['Customer']].tech_need) ]
    else:
        row = [step, current_event['Event Time'], current_event['Event Type'], current_event['Customer'] ]

    # 2. All state variables
    row.extend(list(state.values()))
    # 3. All Cumulative Stats
    row.extend(list(data['Cumulative Stats'].values()))

    # 4. All events in fel ('Event Time', 'Event Type' & 'Event Customer' for each event)
    for event in sorted_fel:
        row.append(event['Event Time'])
        row.append(event['Event Type'])
        row.append(event['Customer'])
    return row






def excel_header(state,data):
    # 1. Step, Clock, Event Type and Event Customer
    header = ['Step', 'Clock', 'Event Type', 'Event Customer']
    # 2. Names of the state variables
    header.extend(list(state.keys()))
    # 3. Names of the cumulative stats
    header.extend(list(data['Cumulative Stats'].keys()))
    return header




def get_col_widths(dataframe):
    # Copied from https://stackoverflow.com/questions/29463274/simulate-autofit-column-in-xslxwriter
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]



def justify(table):
    # This function adds blanks to short rows in order to match their lengths to the maximum row length

    # Find maximum row length in the table
    row_max_len = 0
    for row in table:
        if len(row) > row_max_len:
            row_max_len = len(row)

    # For each row, add enough blanks
    for row in table:
        row.extend([""] * (row_max_len - len(row)))


def create_main_header(state, data):
    # This function creates the main part of header (returns a list)
    # A part of header which is used for future events will be created in create_excel()

    # Header consists of ...
    # 1. Step, Clock, Event Type and Event Customer
    header = ['Step', 'Clock', 'Event Type', 'Event Customer']
    # 2. Names of the state variables
    header.extend(list(state.keys()))
    # 3. Names of the cumulative stats
    header.extend(list(data['Cumulative Stats'].keys()))
    return header

def create_excel(table, header):
    # This function creates and fine-tunes the Excel output file

    # Find length of each row in the table
    row_len = len(table[0])

    # Find length of header (header does not include cells for fel at this moment)
    header_len = len(header)

    # row_len exceeds header_len by (max_fel_length * 3) (Event Type, Event Time & Customer for each event in FEL)
    # Extend the header with 'Future Event Time', 'Future Event Type', 'Future Event Customer'
    # for each event in the fel with maximum size
    i = 1
    for col in range((row_len - header_len) // 3):
        header.append('Future Event Time ' + str(i))
        header.append('Future Event Type ' + str(i))
        header.append('Future Event Customer ' + str(i))
        i += 1

    # Dealing with the output
    # First create a pandas DataFrame
    df = pd.DataFrame(table, columns=header, index=None)

    # Create a handle to work on the Excel file
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

    # Write out the Excel file to the hard drive
    df.to_excel(writer, sheet_name='Output', header=False, startrow=1, index=False)

    # Use the handle to get the workbook (just library syntax, can be found with a simple search)
    workbook = writer.book

    # Get the sheet you want to work on
    worksheet = writer.sheets['Output']

    # Create a cell-formatter object (this will be used for the cells in the header, hence: header_formatter!)
    header_formatter = workbook.add_format()

    # Define whatever format you want
    header_formatter.set_align('center')
    header_formatter.set_align('vcenter')
    header_formatter.set_font('Times New Roman')
    header_formatter.set_bold('True')

    # Write out the column names and apply the format to the cells in the header row
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_formatter)

    # Auto-fit columns
    # Copied from https://stackoverflow.com/questions/29463274/simulate-autofit-column-in-xslxwriter
    for i, width in enumerate(get_col_widths(df)):
        worksheet.set_column(i - 1, i - 1, width)

    # Create a cell-formatter object for the body of excel file
    main_formatter = workbook.add_format()
    main_formatter.set_align('center')
    main_formatter.set_align('vcenter')
    main_formatter.set_font('Times New Roman')

    # Apply the format to the body cells
    for row in range(1, len(df) + 1):
        worksheet.set_row(row, None, main_formatter)

    # Save your edits
    writer.save()




def simulation(simulation_time , Expert_mean_service_time = tt(min= 3), Beginner_mean_service_time = tt(min= 7),max_Experts = 2 , max_Technician = 2,max_Beginner =3):
    seed = int(current_seed())
    random.seed(seed)

    state, future_event_list, data = starting_state( Expert_mean_service_time,Beginner_mean_service_time  ,max_Experts, max_Technician , max_Beginner)
    clock = 0
    records=[]   #for record stats and FEL and current event in each step
    step=1
    future_event_list.append({'Event Type': 'End of Simulation', 'Event Time': simulation_time, 'Customer': None})
    while clock < simulation_time :
        future_event_list.sort(key=lambda x:x['Event Time'])        #for taking earliest event from FEL
        # for k in future_event_list:
        #     print(k)
        current_event=future_event_list.pop(0)
        event_type=current_event['Event Type']
        customer = current_event['Customer']
        clock = current_event['Event Time']
        if clock < simulation_time:                                 #run the related function considering type of the event
            if event_type == 'Arrival':
                data['Customer_number'] += 1
                if data['Customer_number'] ==3000:
                    data['No3000_time'] = clock
                arrival(future_event_list,state,clock,data,customer)
            elif event_type == 'End of Service by Beginner':
                end_service_by_beginner(future_event_list,state,clock,data,customer)
            elif event_type == 'End of Service by Expert':
                end_service_by_expert(future_event_list,state,clock,data,customer)
            elif event_type == 'End of Service by Technician':
                end_service_by_technician(future_event_list,state,clock,data,customer)
            ##elif event_type == 'Change work shift':
            ##    change_shift(future_event_list,state,clock,data)
            ##elif event_type == 'Change month':
            ##    change_month(future_event_list,state,clock,data)
            elif event_type == 'End call by customer':
                end_call_by_customer(future_event_list,state,clock,data,customer)
            ##elif event_type == 'Start of Network Error':
            ##    start_network_error(future_event_list,state,clock,data)
            ##elif event_type == 'End of Network Error':
            ##    end_network_error(future_event_list,state,clock,data)
        else:
            future_event_list.clear()
        records.append(create_row(step, current_event, state, data, future_event_list))
        step += 1

    # add last part of area under curve
    data['Cumulative Stats']['Area Under Queue1 Length Curve'] += ((clock - data['Last Time Queue1 Length Changed']) * state['VIP Queue Length'])
    data['Cumulative Stats']['Area Under Queue2 Length Curve'] += ((clock - data['Last Time Queue2 Length Changed']) * state['Normal Queue Length'])
    ##data['Cumulative Stats']['Area Under Queue3 Length Curve'] += ((clock - data['Last Time Queue3 Length Changed']) * state['VIP call-back Queue Length'])
    ##data['Cumulative Stats']['Area Under Queue4 Length Curve'] += ((clock - data['Last Time Queue4 Length Changed']) * state['Normal call-back Queue Length'])
    data['Cumulative Stats']['Area Under Queue5 Length Curve'] += ((clock - data['Last Time Queue5 Length Changed']) * state['VIP technician Queue Length'])
    data['Cumulative Stats']['Area Under Queue6 Length Curve'] += ((clock - data['Last Time Queue6 Length Changed']) * state['Normal technician Queue Length'])

    #create a dictionary for reporting KPIs by recorded stats
    KPI=dict()
    KPI['Queue2 Waiting Times list'] = data['Cumulative Stats']['Queue2 Waiting Times list'].copy()
    KPI['VIP In-system time'] = dict()
    KPI['No waiting VIP'] = dict()
    KPI['Queue stats'] = {'max length':dict(), 'average length':dict(), 'average waiting time':dict()}
    KPI['Efficiency'] = dict()
    KPI['end-call stats'] = dict()

    KPI['VIP In-system time']['tech-need'] = data['Cumulative Stats']['In-system VIP tech-need Time']/ data['Cumulative Stats']['VIP tech-need Finishers']
    KPI['VIP In-system time']['no-tech-need'] = data['Cumulative Stats']['In-system VIP no-tech-need Time'] / (data['Cumulative Stats']['VIP Finishers'])
    KPI['VIP In-system time']['total'] = data['Cumulative Stats']['In-system VIP Time'] /(data['Cumulative Stats']['VIP Finishers'] + data['Cumulative Stats']['VIP tech-need Finishers'])

    KPI['No waiting VIP']['tech-need'] = data['Cumulative Stats']['No waiting tech-need VIP']/ data['Cumulative Stats']['VIP tech-need Finishers']
    KPI['No waiting VIP']['no-tech-need'] = data['Cumulative Stats']['No waiting no-tech-need VIP'] / data['Cumulative Stats']['VIP Finishers']
    KPI['No waiting VIP']['total'] = (data['Cumulative Stats']['No waiting tech-need VIP'] + data['Cumulative Stats']['No waiting no-tech-need VIP'])/ (data['Cumulative Stats']['VIP Finishers'] + data['Cumulative Stats']['VIP tech-need Finishers'])

    KPI['Queue stats']['max length'][1] = data['Cumulative Stats']['Max QL1']
    KPI['Queue stats']['max length'][2] = data['Cumulative Stats']['Max QL2']
    ##KPI['Queue stats']['max length'][3] = data['Cumulative Stats']['Max QL3']
    ##KPI['Queue stats']['max length'][4] = data['Cumulative Stats']['Max QL4']
    KPI['Queue stats']['max length'][5] = data['Cumulative Stats']['Max QL5']
    KPI['Queue stats']['max length'][6] = data['Cumulative Stats']['Max QL6']
    KPI['Queue stats']['average length'][1] = data['Cumulative Stats']['Area Under Queue1 Length Curve']/(simulation_time-data['No3000_time'])
    KPI['Queue stats']['average length'][2] = data['Cumulative Stats']['Area Under Queue2 Length Curve']/(simulation_time-data['No3000_time'])
    ##KPI['Queue stats']['average length'][3] = data['Cumulative Stats']['Area Under Queue3 Length Curve']/(simulation_time-data['No3000_time'])
    ##KPI['Queue stats']['average length'][4] = data['Cumulative Stats']['Area Under Queue4 Length Curve']/(simulation_time-data['No3000_time'])
    KPI['Queue stats']['average length'][5] = data['Cumulative Stats']['Area Under Queue5 Length Curve']/(simulation_time-data['No3000_time'])
    KPI['Queue stats']['average length'][6] = data['Cumulative Stats']['Area Under Queue6 Length Curve']/(simulation_time-data['No3000_time'])
    KPI['Queue stats']['average waiting time'][1] = data['Cumulative Stats']['Queue1 Waiting Time']/ (data['Cumulative Stats']['Queue1 Finishers'] + 0.0000001)
    KPI['Queue stats']['average waiting time'][2] = data['Cumulative Stats']['Queue2 Waiting Time']/ (data['Cumulative Stats']['Queue2 Finishers']+ 0.0000001)
    ##KPI['Queue stats']['average waiting time'][3] = data['Cumulative Stats']['Queue3 Waiting Time']/ (data['Cumulative Stats']['Queue3 Finishers']+ 0.0000001)
    ##KPI['Queue stats']['average waiting time'][4] = data['Cumulative Stats']['Queue4 Waiting Time']/ (data['Cumulative Stats']['Queue4 Finishers']+ 0.0000001)
    KPI['Queue stats']['average waiting time'][5] = data['Cumulative Stats']['Queue5 Waiting Time']/ (data['Cumulative Stats']['Queue5 Finishers']+ 0.0000001)
    KPI['Queue stats']['average waiting time'][6] = data['Cumulative Stats']['Queue6 Waiting Time']/ (data['Cumulative Stats']['Queue6 Finishers']+ 0.0000001)

    KPI['Efficiency']['Beginners'] = data['Cumulative Stats']['Beginner Busy Time'] / ((simulation_time-data['No3000_time'])*max_Beginner)
    KPI['Efficiency']['Experts'] = data['Cumulative Stats']['Expert Busy Time'] / ((simulation_time-data['No3000_time'])*max_Experts)
    KPI['Efficiency']['Technician'] = data['Cumulative Stats']['Technician Busy Time'] / ((simulation_time-data['No3000_time'])*max_Technician)

    KPI['end-call stats']['VIP'] = data['Cumulative Stats']['ended-call by VIP'] / data['Cumulative Stats']['Queue1 Finishers']
    KPI['end-call stats']['Normal'] = data['Cumulative Stats']['ended-call by Normal'] / data['Cumulative Stats']['Queue2 Finishers']
    print('-------------------------------------------------------------------------------------------------')
    print(f'seed = {seed}')
    print("\nVIP average In-system time (sec):")
    print('\ttech-need = %.3f' % KPI['VIP In-system time']['tech-need'])
    print('\tno-tech-need = %.3f' %KPI['VIP In-system time']['no-tech-need'])
    print('\ttotal  = %.3f' %KPI['VIP In-system time']['total'])

    print("\nNo waiting VIP percentage:")
    print('\ttech-need = %.3f' % KPI['No waiting VIP']['tech-need'])
    print('\tno-tech-need = %.3f' % KPI['No waiting VIP']['no-tech-need'])
    print('\ttotal  = %.3f' % KPI['No waiting VIP']['total'])

    print("\nQueue stats")
    print('\tmax length:')
    for i in range(1,7):
        if i in (3,4):
            continue
        print('\t\tQueue %i= %i' % (i,KPI['Queue stats']['max length'][i]))
    print('\taverage length:')
    for i in range(1, 7):
        if i in (3,4):
            continue
        print('\t\tQueue %i= %.3f' % (i, KPI['Queue stats']['average length'][i]))
    print('\taverage waiting time (sec):')
    for i in range(1, 7):
        if i in (3,4):
            continue
        print('\t\tQueue %i= %.3f' % (i, KPI['Queue stats']['average waiting time'][i]))

    print("\nEfficiency:")
    print('\tBeginners = %.3f' % KPI['Efficiency']['Beginners'])
    print('\tExperts = %.5f' % KPI['Efficiency']['Experts'])
    print('\tTechnician  = %.3f' % KPI['Efficiency']['Technician'])

    print("\nend-call stats:")
    print('\tVIP = %.3f' % KPI['end-call stats']['VIP'])
    print('\tNormal = %.5f' % KPI['end-call stats']['Normal'])
    # excel_main_header = create_main_header(state, data)
    # justify(table=records)
    # create_excel(records, excel_main_header)

    print('FINISH')
    return KPI ,seed



# cold-start analysis
dict_of_time_lists = {}
min_length = math.inf
ss=pd.DataFrame()
for i in range(20):
    KPI, seed = simulation(tt(month=1), Expert_mean_service_time=tt(min=3), Beginner_mean_service_time=tt(min=7),
                       max_Experts=2, max_Technician=2, max_Beginner=3)
    new=pd.DataFrame({i:KPI['Queue2 Waiting Times list']})
    ss = pd.concat([ss,new],axis=1)
    min_length = min(min_length , len(KPI['Queue2 Waiting Times list']))
print(min_length)
ss=ss[:min_length]
ss['mean'] = list(ss.mean(axis=1))
ss['std'] = ss.std(axis=1)

from scipy.stats import t
t_s = abs(t.ppf(0.05/2,19))
rad20 = math.sqrt(20)
ss['mean - H']=ss['mean'] - ss['std']*t_s/rad20
ss['mean + H']=ss['mean'] + ss['std']*t_s/rad20
ss.to_excel(f'cold-start.xlsx')


# for comparison of two system by independent Sampling
sys1=[]
sys2=[]
for i in range(50):
    KPI, seed = simulation(tt(month=2), Expert_mean_service_time=tt(min=3), Beginner_mean_service_time=tt(min=7),
                           max_Experts=2, max_Technician=2, max_Beginner=3)
    sys1.append(KPI['Queue stats']['average waiting time'][2])
    KPI, seed = simulation(tt(month=2), Expert_mean_service_time=tt(sec=162), Beginner_mean_service_time=tt(sec=348),
                           max_Experts=2, max_Technician=2, max_Beginner=2)
    sys2.append(KPI['Queue stats']['average waiting time'][2])
ss=pd.DataFrame({'sys 1 average waiting time in Q2':sys1 , 'sys 2 average waiting time in Q2':sys2 })
ss.to_excel(f'independent_sampling.xlsx')


# for comparison of two system by independent Sampling (full version)
AVT1_1=[]
AVT1_2=[]
AVT2_1=[]
AVT2_2=[]
Beginner_Efficiency_1=[]
Beginner_Efficiency_2=[]
Expert_Efficiency_1=[]
Expert_Efficiency_2=[]
end_call_VIP_1=[]
end_call_VIP_2=[]
end_call_Normal_1=[]
end_call_Normal_2=[]
max_QL_1_1=[]
max_QL_2_1=[]
max_QL_1_2=[]
max_QL_2_2=[]

for i in range(50):
    KPI1, seed1 = simulation(tt(month=2), Expert_mean_service_time=tt(min=3), Beginner_mean_service_time=tt(min=7),
                           max_Experts=2, max_Technician=2, max_Beginner=3)
    KPI2, seed2 = simulation(tt(month=2), Expert_mean_service_time=tt(sec=162), Beginner_mean_service_time=tt(sec=348),
                           max_Experts=2, max_Technician=2, max_Beginner=2)
    AVT1_1.append(KPI1['Queue stats']['average waiting time'][1])
    AVT1_2.append(KPI2['Queue stats']['average waiting time'][1])
    AVT2_1.append(KPI1['Queue stats']['average waiting time'][2])
    AVT2_2.append(KPI2['Queue stats']['average waiting time'][2])
    Beginner_Efficiency_1.append(KPI1['Efficiency']['Beginners'])
    Beginner_Efficiency_2.append(KPI2['Efficiency']['Beginners'])
    Expert_Efficiency_1.append(KPI1['Efficiency']['Experts'])
    Expert_Efficiency_2.append(KPI2['Efficiency']['Experts'])
    end_call_VIP_1.append(KPI1['end-call stats']['VIP'])
    end_call_VIP_2.append(KPI2['end-call stats']['VIP'])
    end_call_Normal_1.append(KPI1['end-call stats']['Normal'])
    end_call_Normal_2.append(KPI2['end-call stats']['Normal'])
    max_QL_1_1.append(KPI1['Queue stats']['max length'][1])
    max_QL_1_2.append(KPI2['Queue stats']['max length'][1])
    max_QL_2_1.append(KPI1['Queue stats']['max length'][2])
    max_QL_2_2.append(KPI2['Queue stats']['max length'][2])

ss=pd.DataFrame({'sys 1 average waiting time in Q1':AVT1_1 , 'sys 2 average waiting time in Q1':AVT1_2,
                 'sys 1 average waiting time in Q2':AVT2_1 ,'sys 2 average waiting time in Q2':AVT2_2 ,
                 'sys 1 Beginner Efficiency':Beginner_Efficiency_1 ,'sys 2 Beginner Efficiency':Beginner_Efficiency_2 ,
                 'sys 1 Expert Efficiency':Expert_Efficiency_1 ,'sys 2 Expert Efficiency':Expert_Efficiency_2 ,
                 'sys 1 end call VIP':end_call_VIP_1 ,'sys 2 end call VIP':end_call_VIP_2 ,
                 'sys 1 end call Normal':end_call_Normal_1 ,'sys 2 end call Normal':end_call_Normal_2 ,
                 'sys 1 max QL1':max_QL_1_1 ,'sys 2 max QL1':max_QL_1_2 ,
                 'sys 1 max QL2':max_QL_2_1 ,'sys 2 max QL2':max_QL_2_2 })

ss.to_excel(f'independent_sampling_full_version.xlsx')
