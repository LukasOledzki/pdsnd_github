import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
        city = str(input('Chosse the city (chicago, new york city, washington):').lower())
        if city not in CITY_DATA:
            print('Really, you only have these cities to choose from (chicago, new york city, washington)')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('Chosse the month (january, february, march, april, may, june) or all:').lower())
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        if month not in months:
            print('You seem to be trying to enter a different month. Try again.')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = str(input('Chosse day of week (monday, tuesday, wednesday, thursday, friday, saturday, sunday) or all:').lower())
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
            if day not in days:
                print('Something went wrong. Try typing again.')
            else:
                break

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
    # load data file:
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""   
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print('Most common day of week:', popular_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour   
    popular_hour = df['hour'].mode()[0]
    print('Most common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations_counter = df['Start Station'].value_counts()
    most_common_start_station = start_stations_counter.idxmax()
    print('The most commonly used start station: ', most_common_start_station)

    # display most commonly used end station
    end_stations_counter = df['End Station'].value_counts()
    most_common_end_station = end_stations_counter.idxmax()
    print('The most commonly used end station: ', most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' -> ' + df['End Station']
    most_common_trip = df['Trip'].value_counts().index[0]
    print('Most frequent combination of start station and end station trip: ', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total trip duration: ', total_trip_duration)
    
    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print('Average trip duration: ', mean_trip_duration)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types: ', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("Counts of gender: \n", gender_count)
    else:
        print("This city does not have this data.")


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('Earliest year of birth {}, most recent year of birth {}, most common year of birth {}'.format(earliest_year, recent_year, common_year))
    else:
        print("This city does not have this data.")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        i = 0
        while True:
            raw_data = input('do you want to see 5 raw data rows? yes or no.')
            if raw_data.lower() == 'yes':
                print(df.iloc[i:i+5])
                i += 5
            elif raw_data.lower() == 'no':
                break
            else:
                print('Please try again with yes or no.')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()