import time
import pandas as pd
import numpy as np

# CITY_DATA is a dictionary that maps city names to their respective data files.
# Each city name is associated with the name of the CSV file containing the bike-share data.
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def convert_seconds(seconds):
    """
    Converts a given number of seconds into days, hours, minutes, and seconds.

    Args:
        seconds (int): The number of seconds to be converted.

    Returns:
        (str) A formatted string displaying the equivalent time in days, hours, minutes, and seconds.
    """

    # Calculate days, hours, minutes, and remaining seconds
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    # Create a list to hold the time components
    time_components = []

    # Add non-zero components to the list
    if days > 0:
        time_components.append(f"{days} days")
    if hours > 0:
        time_components.append(f"{hours} hours")
    if minutes > 0:
        time_components.append(f"{minutes} minutes")
    if seconds > 0:
        time_components.append(f"{seconds} seconds")

    # Join the components with commas and spaces
    return ", ".join(time_components)


def check_data_entry(prompt, valid_entries):
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()

        while user_input not in valid_entries:
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).strip().lower()

        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input

    except:
        print('Seems like there is an issue with your input')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hi there! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february',
                    'march', 'april', 'may', 'june']
    prompt_month = 'Please choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all', 'monday', 'tuesday', 'wednesday',
                  'thursday', 'friday', 'saturday', 'sunday']
    prompt_day = 'Please choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)

    print('-'*40)
    return city, month, day


def old_get_filters():
    # Valid city options
    valid_cities = ["chicago", "new york city", "washington"]
    # Valid month options
    valid_months = ["all", "january", "february",
                    "march", "april", "may", "june"]
    # Valid day of the week options
    valid_days = ["all", "monday", "tuesday", "wednesday",
                  "thursday", "friday", "saturday", "sunday"]
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        try:
            # Get user input for city (chicago, new york city, washington) and remove leading/trailing spaces
            city = input(
                "Enter a city (Chicago, New York City, Washington): ").strip().lower()

            # Check if the input is valid
            if city in valid_cities:
                break
            else:
                print("Invalid input. Please enter a valid city.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    while True:
        try:
            # Get user input for month (all, january, february, ... , june) and remove leading/trailing spaces
            month = input(
                "Enter a month (January, February, ..., June) or all: ").strip().lower()

            # Check if the input is valid
            if month.isalpha() and (month in valid_months):
                break
            else:
                print("Invalid input. Please enter a valid month.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    while True:
        try:
            # Get user input for day of week (all, monday, tuesday, ... sunday) and remove leading/trailing spaces
            day = input(
                "Enter a day of the week (Monday, Tuesday, ..., Sunday) or all: ").strip().lower()

            # Check if the input is valid
            if day in valid_days:
                break
            else:
                print("Invalid input. Please enter a valid day of the week.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

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

    # Load data from the selected CSV file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # map the day of the week number to its name
    df['day_of_week'] = df['day_of_week'].map({
        0: 'monday',
        1: 'tuesday',
        2: 'wednesday',
        3: 'thursday',
        4: 'friday',
        5: 'saturday',
        6: 'sunday'
    })

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]
    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # try:
    # Display the most common month
    if 'month' in df:
        common_month = df['month'].mode()[0]
        print(f"The most common month for travel is: {common_month}")
    else:
        print("Month data not available in the dataset.")

    # Display the most common day of the week
    if 'day_of_week' in df:
        common_day = df['day_of_week'].mode()[0]
        print(
            f"The most common day of the week for travel is: {common_day}")
    else:
        print("Day of the week data not available in the dataset.")

    #  Display the most common start hour
    if 'Start Time' in df:
        df['hour'] = df['Start Time'].dt.hour
        common_hour = df['hour'].mode()[0]
        print(f"The most common start hour for travel is: {common_hour}")
    else:
        print("Start Time data not available in the dataset.")
    # except Exception as e:
    #     print(f"An error occurred: {str(e)}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # Display most commonly used start station
        if 'Start Station' in df:
            common_start_station = df['Start Station'].mode()[0]
            print(f"The most common start station is: {common_start_station}")
        else:
            print("Start Station data not available in the dataset.")

         # Display most commonly used end station
        if 'End Station' in df:
            common_end_station = df['End Station'].mode()[0]
            print(f"The most common end station is: {common_end_station}")
        else:
            print("End Station data not available in the dataset.")

         # Display most frequent combination of start station and end station trip
        if 'Start Station' in df and 'End Station' in df:
            common_trip = df.groupby(
                ['Start Station', 'End Station']).size().idxmax()
            start_station, end_station = common_trip
            print(
                f"The most frequent combination of start and end station is from '{start_station}' to '{end_station}'")
        else:
            print("Start Station or End Station data not available in the dataset.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        # Display total travel time
        if 'Trip Duration' in df:
            total_travel_time = df['Trip Duration'].sum()
            print(f"Total travel time: {convert_seconds(total_travel_time)}")
        else:
            print("Trip Duration data not available in the dataset.")

         # Display mean travel time
        if 'Trip Duration' in df:
            mean_travel_time = df['Trip Duration'].mean()
            print(f"Mean travel time: {convert_seconds(mean_travel_time)}")
        else:
            print("Trip Duration data not available in the dataset.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        if 'User Type' in df:
            user_types = df['User Type'].value_counts()
            print("Counts of user types: ")
            for user_type, count in user_types.items():
                print(f"{user_type}: {count}")
        else:
            print("User Type data not available in the dataset.")

        # Display counts of gender
        if 'Gender' in df:
            gender_counts = df['Gender'].value_counts()
            print("\nCounts of gender:")
            for gender, count in gender_counts.items():
                print(f"{gender}: {count}")
        else:
            print("\nGender data not available in the dataset.")

        # Display earliest, most recent, and most common year of birth
        if 'Birth Year' in df:
            earliest_birth_year = df['Birth Year'].min()
            most_recent_birth_year = df['Birth Year'].max()
            most_common_birth_year = df['Birth Year'].mode()[0]
            print("\nYear of birth statistics:")
            print(f"Earliest birth year: {int(earliest_birth_year)}")
            print(f"Most recent birth year: {int(most_recent_birth_year)}")
            print(f"Most common birth year: {int(most_common_birth_year)}")
        else:
            print("\nYear of birth data not available in the dataset.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Displays data to the user in chunks of 5 rows at a time.

    Args:
        df (Pandas DataFrame): The DataFrame containing the data to be displayed.
    """
    start_loc = 0

    view_data = input(
        '\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').strip().lower()

    while view_data == 'yes':
        end_loc = start_loc + 5

        # Display the next 5 rows of data
        print(df.iloc[start_loc:end_loc])

        start_loc += 5

        # Ask if the user wants to continue
        view_data = input(
            "Do you wish to continue? Enter yes or no: ").strip().lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.strip().lower() != 'yes':
            break


if __name__ == "__main__":
    main()
