import pandas as pd
import matplotlib.pyplot as plt
import datetime


def fetch_data(csv_file_name):
    '''
    fetch_data(csv_file_name) function fetches the csv file, the file should be enclosed within quotes and also placed,
    in the same folder as the python file.
    '''

    data = pd.read_csv(csv_file_name)
    data_columns = data.columns
    print(data_columns)

    return data

def plot_time_series(data):
    '''
    plot_time_series(data) will take the fetched data as an input and plot the graph for the following:
        1. Take the subscription Date and plot with the Customer Id, so we will know when customer subscribed to the website.
    '''
    plt.scatter(x=data['Subscription Date'], y=data['Customer Id'])
    plt.xlabel('Subscription Date')
    plt.ylabel('Customer Id')

    return plt.show()

def check_ssl(data):
    '''
    check_ssl funciton will take the data as input and check the website columns, 
    it will check whether the website is ssl certified or not, that means the website should contain the https rather than http and gives the result.
    '''

    ssl_data = list(data['Website'])
    http = []
    https = []
    for website in ssl_data:
        if website.startswith('https'):
            https.append(website)
        else:
            http.append(website)
    
    lenth_of_http = len(http)
    length_of_https = len(https)
    
    return f"Number of http: {lenth_of_http}", f"Number of https: {length_of_https}"

def check_age_of_websites(data):
    '''
    check_age_of_websites function will take the data as input and take time column and check how old is the each website.
    '''
    subscription_date = data['Subscription Date']
    list_of_ages = []
    for date in subscription_date:
        age = datetime.datetime.today() - datetime.datetime.strptime(date, '%Y-%m-%d')
        list_of_ages.append(age)
    
    return list_of_ages
    


df = fetch_data("customers-1000.csv")
# print(df)
# print(check_ssl(df)) 
list_of_ages =  check_age_of_websites(df)
df['age'] = list_of_ages
print(df)