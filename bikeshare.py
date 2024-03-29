import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
                'new york': 'new_york_city.csv',
                'washington': 'washington.csv' }
MONTHS = {	'january': 1,
		'february': 2,
		'march': 3,
		'april': 4,
		'may': 5,
		'june': 6,
		'july': 7,
		'august': 8,
		'september': 9,
		'october': 10,
		'november': 11,
		'december': 12	}
current_row = {'row':0}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - number of the day of week (sunday = 1, saturday = 7) to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city=''
    while city not in CITY_DATA:
        city = input("Would like to see the data for Chicago, New York or Washington?\n").lower()
        if city not in CITY_DATA:
            print('Unavalible city')

    # get user input for month (all, january, february, ... , june)
    month=''
    while month not in MONTHS:
        month = input("\nWould like to filter the data by month?\nType a month (january, february, ...), or type all for no filter: ").lower()
        if month == 'all':
            break
        if month not in MONTHS:
            print('Invalid month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=0
    while day < 1 or day > 7:
        day=input('\nWould like to filter the data by day?\nType a number representing the day of the week (Sunday = 1), or type all for no filter: ')
        if day == 'all':
            break
        else:
            try:
                day=int(day)
            except:
                print('Invalid input')
                day = 0
                continue
        if day < 1 or day > 7:
            print('Invalid day')
    if(day!='all'):
        day=(day+7-2)%7
    print('-'*100)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - number of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    current_row['row']=0
    f=open(CITY_DATA[city],'r')
    df=f.read()
    df=df.split('\n')
    tempdf=[]
    finaldf=[]
    for i in range(1,len(df)-1):
        tempdf.append(df[i].split(','))
    for item in tempdf:
        item[1]=dt.datetime.strptime(item[1][2:],'%y-%m-%d %H:%M:%S')
        item[2]=dt.datetime.strptime(item[2][2:],'%y-%m-%d %H:%M:%S')
        x=item[1]
        if(day!='all' and month!='all'):
            if int(x.month)==MONTHS[month] and int(x.weekday())==day:
                finaldf.append(item)
        elif day!='all':
            if int(x.weekday())==day:
                finaldf.append(item)
        elif month!='all':
            if int(x.month)==MONTHS[month]:
                finaldf.append(item)
        else:
            finaldf.append(item)
    return finaldf


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    days_of_week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    mon_dic={}
    day_dic={}
    hour_dic={}
    for record in df:
        t=record[1]
        m=str(t.month)
        if m not in mon_dic:
            mon_dic[m]=1
        else:
            mon_dic[m]+=1
        w=str(t.weekday())
        if w not in day_dic:
            day_dic[w]=1
        else:
            day_dic[w]+=1
        h=str(t.hour)
        if h not in hour_dic:
            hour_dic[h]=1
        else:
            hour_dic[h]+=1

    # display the most common month
    x=0
    most_common_month=0
    for month,num in mon_dic.items():
        if num > x:
            x=num
            most_common_month = month
    for key,val in MONTHS.items():
        if val == int(most_common_month):
            most_common_month=key
            break
    print('The most common month:',most_common_month)

    # display the most common day of week
    x=0
    most_common_day=0
    for day,num in day_dic.items():
        if num > x:
            x=num
            most_common_day = day
    print('The most common day of week:',days_of_week[int(most_common_day)])

    # display the most common start hour
    x=0
    most_common_hour=0
    for hour,num in hour_dic.items():
        if num > x:
            x=num
            most_common_hour = hour
    most_common_hour = int(most_common_hour)
    if most_common_hour == 0:
        most_common_hour = '12 AM'
    elif most_common_hour == 12:
        most_common_hour = '12 PM'
    elif most_common_hour < 12:
        most_common_hour = str(most_common_hour)+' AM'
    else:
        most_common_hour = str(most_common_hour%12)+' PM'
    print('The most common starting hour:',most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    start_station={}
    end_station={}
    comb={}
    x=0
    most_common_start=''
    most_common_end=''
    most_common_comb=''
    for record in df:
        if record[4] in start_station.keys():
            start_station[record[4]]+=1
        else:
            start_station[record[4]]=1
        if record[5] in end_station.keys():
            end_station[record[5]]+=1
        else:
            end_station[record[5]]=1
        s = str(record[4])+','+str(record[5])
        if s in comb.keys():
            comb[s]+=1
        else:
            comb[s]=1
    
    # display most commonly used start station
    for station,num in start_station.items():
        if num > x:
            x=num
            most_common_start = station
    print('Most common start station:',most_common_start)

    # display most commonly used end station
    x=0
    for station,num in end_station.items():
        if num > x:
            x=num
            most_common_end = station
    print('\nMost common end station:',most_common_end)

    # display most frequent combination of start station and end station trip
    x=0
    for station,num in comb.items():
        if num > x:
            x=num
            most_common_comb = str(station).split(',')
    print('\nMost frequent combination of start and end stations:',most_common_comb[0],'and',most_common_comb[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    t = 0
    avg = 0
    total_trips = 0
    time_in_sec = 0
    for record in df:
        total_trips+=1
        time_in_sec+=float(record[3])
    print("Total travel time: ",dt.timedelta(seconds=int(time_in_sec)))
    
    # display mean travel time
    if(total_trips>0):
        avg=time_in_sec/total_trips
    avg=dt.timedelta(seconds=int(avg))
    print("Mean travel time: ",avg)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subscriber = 0
    customer = 0
    for record in df:
        if record[6]=='Subscriber':
            subscriber+=1
        elif record[6] =='Customer':
            customer+=1
    print('User Type Stats')
    print('Subscribers:',subscriber)
    print('Customers:',customer)

    # Display counts of gender
    if city!='washington':
        male = 0
        female = 0
        for record in df:
            if record[7]=='Male':
                male+=1
            elif record[7] =='Female':
                female+=1
        print('\nGender Stats')
        print('Male users:',male)
        print('Female users:',female)

    # Display earliest, most recent, and most common year of birth
    if city!='washington':
        years={}
        min_year = 3000
        max_year = 0
        most_ferquent=''
        t = 0
        for record in df:
            try:
                x=int(float(record[8]))
            except:
                continue
            if x in years.keys():
                years[x]+=1
            else:
                years[x]=1
            min_year=min(x,min_year)
            max_year=max(x,max_year)
        for year,num in years.items():
            if num > t:
                t=num
                most_ferquent=year
        print('\nYear Of Birth Stats')
        print('Earliest year of birth:',min_year)
        print('Most recent year of birth:',max_year)
        print('Most common year of birth:',most_ferquent)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

def set_len(s,x):
    while len(s) < x:
        s+=' '
    return s


def display_5_rows(df,row,city):
    """Displays 5 individual records from the requested data"""
    if row >= len(df):
        print('All records have been displayed')
        return True
    key = ''
    space = 52
    if city=='new york':
        space = 35
    elif city=='chicago':
        space = 45
    a=set_len('Start Time',21)
    b=set_len('End Time',21)
    c=set_len('Duartion',10)
    d=set_len('Start Station',space)
    e=set_len('End Station',space)
    f=set_len('User Type',12)
    g=set_len('Gender',8)
    h=set_len('Year',4)
    key=set_len('',7)+a+b+c+d+e+f
    if city!='washington':
        key+=g+h
    print(key)
    data_row = ''
    for i in range(row,min(row+5,len(df))):
        record = df[i]
        index = set_len(str(i+1),7)
        start_time = set_len(str(record[1]),21)
        end_time = set_len(str(record[2]),21)
        duration = set_len(str(dt.timedelta(seconds=int(float(str(record[3]))))),10)
        start_station = set_len(record[4],space)
        end_station = set_len(record[5],space)
        user = set_len(record[6],12)
        gender = set_len('Null',8)
        year = set_len('Null',4)
        data_row = index+start_time+end_time+duration+start_station+end_station+user
        if city != 'washington':
            if record[7] !='':
                gender = set_len(record[7],8)
            if record[8] !='':
                year = set_len(str(int(float(record[8]))),4)
            data_row+=gender+year
        print(data_row)
    row+=5
    return False


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        if len(df)>0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)

            while True:
                display = input('\nWould you like to display 5 individual trips? Enter yes or no.\n')
                if display.lower() != 'yes' or display_5_rows(df,current_row['row'],city):
                    break
                else:
                    current_row['row'] = current_row['row'] + 5
        else:
            print('No trips are recorded given the current filters')
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
