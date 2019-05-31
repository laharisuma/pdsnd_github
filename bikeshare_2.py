import time
import pandas as pd
import numpy as np

#the csv files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
Months = ['january', 'february', 'march', 'april', 'may', 'june']

Days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to           handle invalid inputs
    city_input = ''
    while city_input.lower() not in CITY_DATA:
        city_input = input('Which city would you like to explore? Chicago, New York City or Washington? \n').lower()
        if city_input.lower() in CITY_DATA:
            #We were able to get the name of the city to analyze data.
            city = CITY_DATA[city_input.lower()]
        else:
            print("Please choose between Chicago, New York City or Washington.")
 
        #gets month to filter the data by 
    month_input = ''
    while month_input.lower() not in Months:
        month_input=input("Which month would you like to explore? January, February, March, April, May or June? \n").lower()
        if month_input.lower() in Months:
            #We were able to get the name of the month to analyze data.
            month = month_input.lower()
        else:
            print("Sorry that month is not recognized. Please enter a valid month.")
        #gets the day to filter the data by
    day_input = ''
    while day_input.lower() not in Days:
        day_input = input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday. \n')
        if day_input.lower() in Days:
            day = day_input.lower()
        else:
            print("That day is not recognized. Please enter a valid day.")
    
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
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is: " +  Months[common_month].title())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most popular day of the week is: "+ common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("The most popular start hour is: ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most frequently used start station :", common_start_station)
    
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most frequently used start station :", common_end_station)

    # display most frequent combination of start station and end station trip
    common_trip = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most frequently used start station and end station : {}, {}"\
            .format(common_trip[0], common_trip[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time   
    travel_time = df['Trip Duration'].sum()
    print('Total Travel time: ', travel_time)

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average Travel time:', avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user = df['User Type'].value_counts()
    print('User type:\n' , user)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("Gender:\n", gender)
    except:
        print('There is no gender data for this city.')

    # Display earliest, most recent, and most common year of birth
    try: 
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("\nThe oldest registered person was born in: ", oldest)
        print("\nThe youngest registered person was born in:", youngest)
        print("\nThe most common birth year is: ", most_common)
    except:
        print("There is no birth year information for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
   
def display_raw_data(df):
    #displays raw data if asked by the user and continues to do so until user says 'no'
    row = 0
    raw = input("Would you like to see the raw data used to calculate this information. Enter yes or no. \n")
    while True:
        if raw == 'no':
            return
        if raw == 'yes':
            print(df[row: row + 5])
            row= row + 5
        raw = input("Would you like to see more raw data? Enter yes or no. \n")
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
