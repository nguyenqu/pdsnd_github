""" I added the comments separately """
import os, sys
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

answerList = ['yes', 'no']
cityList = ['chicago', 'new york city', 'washington']
MonthList = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
weekdayList = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def clear_screen():
    try:
        s = sys.winver
        os.system("cls")
    except:
        os.system("clear") 

def check_entry(entryStr, dataList):
    """
    Check whether the entry is in the list provided
    
    Args:
      entryStr: Input data
      dataList: Data list
    Return:
      (boolean) bCheck : True or False
    """
    bCheck = False
    if entryStr in dataList:
        bCheck = True
    else:
        print('Wrong entry !!!')
    
    return bCheck

def display_of_raw_data(df):
    """ Display the raw data """
    cNumberOfLines=5 # Constant: Number of lines to be shown
    
    # 1st data block
    i=0
    y=i+cNumberOfLines
    
    while y <= len(df):
        
        # Output of the raw data block on the screen
        print('\n')
        print(df[i:y])
        
        bOK = False
        while bOK == False:
            sNext = input("\nDo you want to see the next " + str(cNumberOfLines) + " raw data? Enter yes or no. ").lower()
            bOK = check_entry(sNext, answerList)

        # fix the next block as long as the length of the data list has not yet been reached    
        if sNext == 'yes':
            i = i + cNumberOfLines
            y = y + cNumberOfLines
            if y > len(df):
                y=len(df)
        else:
            break

                  
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    
    # To Do: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    bOK = False
    while bOK == False:
        city = input('Enter the city ' + str(cityList) + ' : ').lower()
        bOK = check_entry(city, cityList)
    
    # TO Do: get user input for month (all, january, february, ... , june)
    bOK = False
    while bOK == False:
        month = input('Enter a month ' + str(MonthList) + ' : ').lower()
        bOK = check_entry(month, MonthList)
 
    # TO DO: get user input for day of week (all, monday, tuesday, ..., sunday)
    bOK = False
    while bOK == False:
        day = input('Enter a weekday ' + str(weekdayList) + ' : ').lower()
        bOK = check_entry(day, weekdayList)
    
    print('-'*80)
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
    df=pd.read_csv(CITY_DATA[city])
    
    # convert the Start/End Time Column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name    
    df['hour'] = df['Start Time'].dt.hour
    df['StartEndStationTrip'] = df['Start Station'] + ' TO ' + df['End Station']
    
    # use the index of the months list to get the corresponding int
    monthNr = MonthList.index(month)
    
    # filter by month if applicable
    if month != MonthList[0]:  # != 'all'
        # filter by month to create the new dataframe
        df = df[df['month'] == monthNr]

    # filter by day of week if applicable
    if day != weekdayList[0]:   # != 'all'
        # filter by day of week to create the new dataframe
        df = df[df['weekday'] == day.title()] 
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popularMonth = df['month'].mode()[0]
    print('Most month: ', MonthList[popularMonth].title())

    # TO DO: display the most common day of week
    popularWeekday = df['weekday'].mode()[0]
    print('Most day of week: ', popularWeekday)

    # TO DO: display the most common start hour
    # find the most common hour (from 0 to 23)
    popularHour = df['hour'].mode()[0]
    print('Most frequenz Start Hour: ', popularHour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popularStartStation = df['Start Station'].mode()[0]
    print("Most used start station: '" + popularStartStation + "'")

    # TO DO: display most commonly used end station
    popularEndStation = df['End Station'].mode()[0]
    print("Most used end station: '" + popularEndStation + "'")

    # TO DO: display most frequent combination of start station and end station trip
    popularStartEndStationTrip = df['StartEndStationTrip'].mode()[0]
    sStartStation , sEndStation = popularStartEndStationTrip.split(' TO ')
    print("Most used start and end station trip: From '" + sStartStation + "' TO '" + sEndStation + "'")
  
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    totalTravelTime = sum(df['Trip Duration'])
    print("\nTotal travel time (in seconds): ", totalTravelTime)
    
    # TO DO: display mean travel time
    meanTravelTime = totalTravelTime / len(df['Trip Duration'])
    print("\nMean travel time (in seconds): ", meanTravelTime)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("\nNumber of empty User Type = " + str(df['User Type'].isnull().sum()))
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    # Only available for Chicago and NYC!!
    if 'Gender' in df:
        print("\nNumber of empty gender = " + str(df['Gender'].isnull().sum())) 
        print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    # Only available for Chicago and NYC!!
    if 'Birth Year' in df:
        # Display earliest year of birth
        earliestBirthyear = df['Birth Year'].min()
        print("\nEarliest year of birth: ", int(earliestBirthyear))
    
        # Display most recent year of birth
        mosRecentBirthyear = df['Birth Year'].max()
        print("\nMost recent  year of birth: ", int(mosRecentBirthyear))

        # Display most common year of birth
        mostCommonBirthyear = df['Birth Year'].mode()[0]
        print("\nMost common year of birth: ", int(mostCommonBirthyear))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def main():
    clear_screen()  # Clear screen
    while True:
        bOK = False
        while bOK == False:
            sView = input("\nDo you want to see the data for Chicago, New York or Washington? Enter yes or no. ").lower()
            bOK = check_entry(sView, answerList)
        
        if sView != 'yes':
            break
                      
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        bOK = False
        while bOK == False:
            sView = input("\nDo you want to see the raw data for the city '" + city + "' in month '" + month + "' and weekday '" + day + "'? Enter yes or no. ").lower()
            bOK = check_entry(sView, answerList)

        if sView == 'yes':
            display_of_raw_data(df)
                  
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        bOK = False
        while bOK == False:
            restart = input('\nWould you like to restart? Enter yes or no. ').lower()
            bOK = check_entry(restart, answerList)
        
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
