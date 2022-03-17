import time,datetime
import pandas as pd
import numpy as np
import calendar
import seaborn as sns
import matplotlib.pyplot as plt

#some lists/dictionaries we will use
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
DATE_MONTH = ['January','February','March','April','May','June','No']
DATE_DAY = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Fridday','Saturday','No']

def get_filters():
    """
    Asks user to specify a city, month, and day then returns a 
    dictionary with the specified data.

    Arguments: None

    Returns Dict ==> {'city':city,'month': month,'day': day}
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'No' to apply no month filter
        (str) day - name of the day of week to filter by, or 'No' to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    flag = True
    while(flag):
        try:
            city = input("""Please input the city you want to view: \n
            chicago, new york city or washington \n
            type 'exit' to exit \n""").lower()
            if city == 'exit':
                return 0
            if city in CITY_DATA.keys():
                flag = False
            else:
                print("we're sorry, your requested city is not in our list, please try again")
        except:
            print('wrong input, please try again')

    # get user input for month (all, january, february, ... , june)
    flag = True
    while(flag):
        try:
            month = input("""Please input the month you want to view: \n
            'January','February','March','April','May' or 'June' \n
             'No'= No filter (all months)
             type 'exit' to exit \n""").capitalize()
            if month == 'exit':
                return 0
            if month in DATE_MONTH:
                flag = False
            else:
                print("wrong input, please try again")
        except:
            print('wrong input, please try again')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    flag = True
    while(flag):
        try:
            day = input("""Please input the day you want to view: \n
            'Sunday','Monday','Tuesday','Wednesday','Thursday','Fridday' or 'Saturday'\n
             'No' = No filter (all days) \n
             type 'exit' to exit \n""").capitalize()
            if day == 'exit':
                return 0
            if day in DATE_DAY:
                flag = False
            else:
                print("wrong input, please try again")
        except:
            print('wrong input, please try again')

    print('-'*40)
    return {'city':city,'month': month,'day': day} #<=== Return of get_filters()

def load_data(request):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Argument 1 'request': {'city':city,'month': month,'day': day}
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    Returns (1 of 2):
        0  - exit
        df - filtered city Pandas dataframe
    """
    #exit
    if request == 0:
        return 0
    
    print("reading file and applying some changes, please wait... \n")
    start_time = time.time()
    
    #load dataframe
    df = pd.read_csv(CITY_DATA[request['city']])
    
    
    #Change Start Time column values for easier handling
    df['Datetime'] = pd.to_datetime(df['Start Time'])

    #add new columns with 'month' and 'day' names to data
    df['month'] = df['Datetime'].dt.month_name()
    df['day'] = df['Datetime'].dt.day_name()
    
    print("file: ",CITY_DATA[request['city']], "\n")
    print("Filters Applied: ")
    
    #filter month
    if request['month'] != 'No':
        df = df[df.month == (request['month'])]
        print("Month = " + request['month'])
    else:
        print("Month = Any")

    #filter day
    if request['day'] != 'No':
        df = df[df.day == request['day']]
        print("Day = " + request['day'])
    else:
        print("Day = Any")
    print("\n Results found :",len(df))
    
    #timestamp calculation
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return df


def time_stats(df,request):
    """Displays statistics on the most frequent times of travel.
    
    Arguments: 2
    request -- dictionary that contains information the user specified about the data
    df -- filtered Pandas dataframe  

    Returns: None"""

    #create table column 'hour'
    print("adding modifications to the table...")
    df['hour'] = df['Datetime'].dt.hour

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if request['month'] == 'No':
        print("Most common Month :", df.month.mode()[0])
        sns.countplot(x = df.month, data = df,order=DATE_MONTH[:-1])
        plt.show()
    else:
        print("The data only contains month '{}'.".format(request['month']))


    # display the most common day of week
    if request['day'] == 'No':
        print("Most common day of the week :", df.day.mode()[0])
        sns.countplot(x = df.day, data = df, order=DATE_DAY[:-1])
        plt.show()
    else:
        print("The data only contains day '{}'.".format(request['day']))  



    # display the most common start hour
    print("Most common start hour",df['hour'].mode()[0])
    plt.xticks([0,3,6,9,12,15,18,21,24])
    sns.kdeplot(x='hour',data=df)
    plt.show()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.    
    
    Arguments: 1
    df -- filtered Pandas dataframe  

    Returns: None"""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("Most common 'Start Station' :",start_station,". Count: ",len(df[df['Start Station'] == start_station]['Start Station']))

    order = df['Start Station'].value_counts().iloc[:10].index
    sns.countplot(y='Start Station',data=df,order=order).set(title='Top 10 most common start stations')
    plt.show()

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("Most common 'End Station' :",end_station,". Count: ",len(df[df['End Station'] == end_station]['End Station']))

    order = df['End Station'].value_counts().iloc[:10].index
    sns.countplot(y='End Station',data=df,order=order).set(title='Top 10 most common end stations')
    plt.show()

    # display most frequent combination of start station and end station trip
    df['Route'] = 'FROM ' + "'" +df['Start Station'] + "'" + ' TO ' + "'" + df['End Station'] + "'"
    route = df['Route'].mode()[0]
    print("Most common Route: ",route,". Count: ",len(df[df['Route'] == route]['Route']))
    
    order = df['Route'].value_counts().iloc[:10].index
    sns.countplot(y='Route',data=df,order=order).set(title='Top 10 most common routes')
    plt.show()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.    
    
    Arguments: 1
    df -- filtered Pandas dataframe  

    Returns: None"""

    print('\nCalculating Trip Duration,please wait...\n')
    start_time = time.time()

    # display total travel time
    df['End Datetime'] = pd.to_datetime(df['End Time'])
    df['Total Travel Time'] = df['End Datetime'] - df['Datetime']
    df['Total Travel Time'] /= np.timedelta64(1,'m')
    
    hours = round(df['Total Travel Time'].sum()/60)
    avg = df['Total Travel Time'].mean()
    avg_minutes = int(avg)
    avg_seconds = int((avg - avg_minutes) * 60)
    print("total Travel time is around {} hrs.".format(hours)," Average Travel time: {} minutes and {} seconds.".format(avg_minutes,avg_seconds))
    
    sns.kdeplot(x='Total Travel Time',data = df).set(title='Travel Time in minutes')
    plt.xlim(0,90)
    plt.show()
    
    # display mean travel time
    #print("average Travel time: ",total_travel_time.mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,request):
    """Displays statistics on bikeshare users.    
    
    Arguments: 1
    df -- filtered Pandas dataframe  

    Returns: None"""

    print('\nCalculating User Stats...\n')
    start_time = time.time() #start timestamp

    # Display counts of user types
    try: 
        print("User types and their respective counts: \n",df['User Type'].value_counts())
        sns.countplot(x = 'User Type',data = df)
        plt.show()
    except: 
        print("dataset {} doesn't have column 'User Type'.".format(CITY_DATA[request['city']]))
    
    # Display counts of gender
    try: 
        print("Genders and their respective counts: \n",df['Gender'].value_counts())
    except: 
        print("dataset {} doesn't have column 'Gender'.".format(CITY_DATA[request['city']]))

    #graph for User Type / Gender
    try:
        sns.countplot(x='User Type',hue='Gender',data=df).set(title = 'User Types (male/Female)')
        plt.legend(loc='upper center')
        plt.show()
    except: 
        print("dataset {} doesn't have column (s) 'User Type' or 'gender'.".format(CITY_DATA[request['city']]))

    # Display earliest, most recent, and most common year of birth
    try:
        print("Most recent year of birth: ",int(df['Birth Year'].max()))
        print("Earliest year of birth: ",int(df['Birth Year'].min()))
        print("Most common year of birth: ",int(df['Birth Year'].mode()[0]))
    
        sns.kdeplot(x='Birth Year',data=df).set(title='Dates of birth')
        plt.show()

    except: 
        print("dataset {} doesn't have column 'Birth Year'.".format(CITY_DATA[request['city']]))
    

    #timestamp calculation
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        
        results = get_filters() #get_filters() returns a dictionary or 0

        if results == 0: #exit
            return 0

        df = load_data(results) #load dataframe

        #display 5 rows
        size = len(df)
        row = 0
        while True:
            try:
                choice = input("""would you like to see 5 new lines of data ? \n
                type 'yes' to view, or anything to continue...
                type 'exit' to exit \n""").lower()

                if choice == 'exit':
                    return 0

                elif choice in ['yes','y']:
                    if row >= size:
                        print("we're sorry, but you already viewed all available data.\n Lets view some statistics instead !")
                        break
                    print(df[row:row+5])
                    row += 5
                else:
                    break
            except:
                print("Wrong input, please try again.")

        while True:
            print("Please choose the statistic you want to see")
            choice = input("time \n station \n duration \n user \n exit \n"+("="*5)).lower()
            if choice in ['time','station','duration','user','exit']:
                if choice == 'time':
                    time_stats(df,results)
                elif choice == 'station':
                    station_stats(df)
                elif choice == 'duration':
                    trip_duration_stats(df)
                elif choice == 'user':
                    user_stats(df,results)
                elif choice == 'exit':
                    break
                else:
                    print("(Dev message) Error in main block 'choice'")
            else:
                print("we're sorry, your input does not match any of the suggested choices, please try again.")
                continue
        
        #restart
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes','y']:
            break


if __name__ == "__main__":
	main()