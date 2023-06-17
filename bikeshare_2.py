import time
import pandas as pd
import numpy as np
from datetime import datetime
import statistics
from statistics import mode

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
city = ''
month = ''
day=''
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
    
    while True:
        city_input = input(
            'Would you like to see data for Chicago, New York or Washington? ')
        if city_input.lower() not in ('chicago', 'new york', 'washington'):
            print('Please only choose one of these: Chicago, New York, Washington')
        else:
            city = city_input
            break
 
    # get user input for month day or not  at all
    while True:
        month_or_day = input('Would you like to filter by month or day, or  not at all? ').lower()
        if month_or_day in ['month', 'day','not at all']:
            break
        else:
            print('Please only select:month, day, not at all')
    day = ''
    month=''
    
    if month_or_day == 'not at all':
        while True:
            break
     # get user input for month   
    if month_or_day == 'month':
        while True:
            month = input(
                'Which month - January, February, March, April, May, June or all?').lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june','all']:
                break
            else:
                print('Is that a typo? Please type the months in full and in proper spelling')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if month_or_day == 'day':
        while True:
            day = input(
                'Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?').lower()
            if day in ['all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
                break 
            else:
                print(
                    'Is that a typo? Please type the days in full and in proper spelling')
    
    
    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    #Loading data based on selections
    if city in CITY_DATA:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month']= df['Start Time'].dt.strftime('%B')
        df['day']= df['Start Time'].dt.strftime('%A')
        if df['month'].eq(month.title()).any():
            df = df[df['month'] == month.title()]
        elif df['day'].eq(day.title()).any():
            df = df[df['day'] == day.title()]
        else:
            df
    # Prompting the user if user wants to see raw data based on their selection
    
    currplace = 0
    while currplace < len(df):
        see_raw_data = input("You've selected your filters! Would you like to see the data based on your selection?")
        if see_raw_data == 'yes':
             currplace += 5
             print(df.head(currplace))
             pd.set_option('display.max_columns', 200)
             continue
        elif see_raw_data == 'no':
            break
            
     
    return df
       
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
     c  (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month to travel is:',mode(df['month']))

    # display the most common day of week
    print('The most common day to travel is:',mode(df['day']))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour to travel is:', mode(df['hour']),'00 hrs')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is ',mode(df['Start Station']))

    # display most commonly used end station
    print('The most commonly used end station is ',mode(df['End Station']))

    # display most frequent combination of start station and end station trip
    df['Start & End Station'] = df['Start Station'] + ' to ' + df['End Station']
    print('The most commonly used start and end station is ', mode(df['Start & End Station']))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate total travel time
    df['Total Time'] = (df['End Time'] - df['Start Time']).sum()
    total_time = df['Total Time'].iloc[0].total_seconds()


    # calculate mean travel time
    avg_time = total_time/len(df)
    
    #convert seconds to hours, minutes and seconds
    t_hours = total_time / 3600
    t_minutes = (total_time % 3600) / 60
    t_seconds = total_time % 60
    a_hours = avg_time / 3600
    a_minutes = (avg_time % 3600) / 60
    a_seconds = avg_time % 60
    print('The total travel time is', round(t_hours),'hrs', round(t_minutes),'mins', round(t_seconds), 'seconds')
    print('The average travel time is', round(a_hours),'hrs', round(a_minutes),'mins', round(a_seconds), 'seconds')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    print("City",df)
    start_time = time.time()

    # Display counts of user types
    print('User Types:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('Count of gender:', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print('Earliest year of birth: ', round(df['Birth Year'].min()))
    print('Recent year of birth: ', round(df['Birth Year'].max()))   
    print('Common year of birth: ', round(mode(df['Birth Year']))) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if set(['Gender','Birth Year']).issubset(df.columns):
            user_stats(df)
        else:
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
