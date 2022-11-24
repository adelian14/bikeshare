import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
                'new york': 'new_york_city.csv',
                'washington': 'washington.csv' }
MONTHS = {	'janauary': 1,
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

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city=''
    while city not in CITY_DATA:
        city = input("Enter city (Chicago, New York or Washington): ").lower()
        if city not in CITY_DATA:
            print('Unavalible city')

    # get user input for month (all, january, february, ... , june)
    month=''
    while month not in MONTHS:
        month = input("Enter month (january, february, ...) or type all for no filter: ").lower()
        if month == 'all':
            break
        if month not in MONTHS:
            print('Invalid month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=0
    while day < 1 or day > 7:
        day=input('Enter a day(a number from 1 to 7, Sunday = 1), or type all for no filter: ')
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
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
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
        x=item[2]
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

    # display the most common month


    # display the most common day of week


    # display the most common start hour


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time


    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


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
    print('Subscribers: {0}, Customers: {1}'.format(subscriber,customer))

    # Display counts of gender
    if city!='washington':
        male = 0
        female = 0
        for record in df:
            if record[7]=='Male':
                male+=1
            elif record[7] =='Female':
                female+=1
        print('Males: {0}, Females: {1}'.format(male,female))

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
        print('Earliest year of birth: {0}, Most recent year of birth: {1}, Most common year of birth: {2}'.format(min_year,max_year,most_ferquent))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #time_stats(df)
        #station_stats(df)
        #trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()