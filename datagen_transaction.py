import random
import pandas as pd
import sys
import datetime
from datetime import date
from random import randint
from faker import Faker
import numpy as np

import profile_weights

def get_user_input():
    # convert date to datetime object
    def convert_date(d):
        for char in ['/', '-', '_', ' ']:
            if char in d:
                d = d.split(char)
                try:
                    return date(int(d[2]), int(d[0]), int(d[1]))
                except:
                    error_msg(3)
        error_msg(3)

    # error handling for CL inputs
    def error_msg(n):
        if n == 1:
            print('Could not open customers file\n')
        elif n == 2:
            print('Could not open main config json file\n')
        else:
            print('Invalid date (MM-DD-YYYY)')
        output = 'ENTER:\n(1) Customers csv file\n'
        output += '(2) profile json file\n'
        output += '(3) Start date (MM-DD-YYYY)\n'
        output += '(4) End date (MM-DD-YYYY)\n'
        print(output)
        sys.exit(0)

    try:
        customers = open(sys.argv[1], 'r').readlines()

    except:
        error_msg(1)
    try:
        m = str(sys.argv[2])
        pro_name = m.split('profiles')[-1]
        pro_name = pro_name[1:]
        parse_index = m.index('profiles') + 9
        m_fraud = m[:parse_index] + 'fraud_' + m[parse_index:]

        pro = open(m, 'r').read()

        pro_fraud = open(m_fraud, 'r').read()

        pro_name_fraud = 'fraud_' + pro_name
        # fix for windows file paths

    except:
        error_msg(2)
    try:
        startd = convert_date(sys.argv[3])
    except:
        error_msg(3)
    try:
        endd = convert_date(sys.argv[4])
    except:
        error_msg(4)

    return customers, pro, pro_fraud, pro_name, pro_name_fraud, startd, endd, m


def create_header(line):
    headers = line.split('|')
    headers[-1] = headers[-1].replace('\n', '')
    headers.extend(['trans_num', 'trans_date', 'trans_time', 'unix_time',
                   'category', 'amt', 'is_fraud', 'merchant', 'merch_lat', 'merch_long'])
    print(''.join([h + '|' for h in headers])[:-1])
    return headers


class Customer(object):
    def __init__(self, customer, profile):
        self.customer = customer
        self.attrs = self.clean_line(self.customer)
        self.fraud_dates = []

    def print_trans_and_append_df(self, trans, is_fraud, fraud_dates):
        global global_transaction_df_in_store
        is_traveling = trans[1]
        travel_max = trans[2]

        for i, t in enumerate(trans[0]):
            # Get transaction location details to generate appropriate merchant record
            cust_state = cust.attrs['state']
            groups = t.split('|')
            trans_cat = groups[4]
            merch_filtered = merch[merch['category'] == trans_cat]
            random_row = merch_filtered.loc[random.sample(
                list(merch_filtered.index), 1)]
            # sw added list
            chosen_merchant = random_row.iloc[0]['merchant_name']

            cust_lat = cust.attrs['lat']
            cust_long = cust.attrs['long']

            if is_traveling:
                # hacky math.. assuming ~70 miles per 1 decimal degree of lat/long
                # sorry for being American, you're on your own for kilometers.
                rad = (float(travel_max) / 100) * 1.43

                # geo_coordinate() uses uniform distribution with lower = (center-rad), upper = (center+rad)
                merch_lat = fake.coordinate(center=float(cust_lat), radius=rad)
                merch_long = fake.coordinate(
                    center=float(cust_long), radius=rad)
            else:
                # otherwise not traveling, so use 1 decimial degree (~70mile) radius around home address
                rad = 1
                merch_lat = fake.coordinate(center=float(cust_lat), radius=rad)
                merch_long = fake.coordinate(
                    center=float(cust_long), radius=rad)

            if is_fraud == 0 and groups[1] not in fraud_dates:
                # if cust.attrs['profile'] == "male_30_40_smaller_cities.json":
                print_str = self.customer.replace('\n', '') + '|' + t + '|' + str(
                    chosen_merchant) + '|' + str(merch_lat) + '|' + str(merch_long)
                # print(print_str)
                df = pd.DataFrame({'temp_str': [print_str]})
                df[['ssn', 'cc_num', 'first', 'last', 'gender', 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop', 'job', 'dob', 'acct_num', 'profile', 'trans_num',
                    'trans_date', 'trans_time', 'unix_time', 'category', 'amt', 'is_fraud', 'merchant', 'merch_lat', 'merch_long']] = df['temp_str'].str.split('|', 0, expand=True)
                df.drop(["temp_str"], inplace=True, axis=1)
                df['recent_visited_states'] = [[fake.state_abbr() for _ in range(randint(1,4))]]
                global_transaction_df_in_store = pd.concat(
                    [global_transaction_df_in_store, df], ignore_index=True, axis=0)

            if is_fraud == 1:
                print_str = self.customer.replace('\n', '') + '|' + t + '|' + str(
                    chosen_merchant) + '|' + str(merch_lat) + '|' + str(merch_long)
                df = pd.DataFrame({'temp_str': [print_str]})
                df[['ssn', 'cc_num', 'first', 'last', 'gender', 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop', 'job', 'dob', 'acct_num', 'profile', 'trans_num',
                    'trans_date', 'trans_time', 'unix_time', 'category', 'amt', 'is_fraud', 'merchant', 'merch_lat', 'merch_long']] = df['temp_str'].str.split('|', 0, expand=True)
                df.drop(["temp_str"], inplace=True, axis=1)
                df['recent_visited_states'] = [[fake.state_abbr() for _ in range(randint(1,4))]]
                global_transaction_df_in_store = pd.concat(
                    [global_transaction_df_in_store, df], ignore_index=True, axis=0)

            # else:
                # pass


    def print_trans_and_append_df_online(self, trans, is_fraud, fraud_dates):
        global global_transaction_df_online
        is_traveling = trans[1]
        travel_max = trans[2]

        for i, t in enumerate(trans[0]):
            # Get transaction location details to generate appropriate merchant record
            cust_state = cust.attrs['state']
            groups = t.split('|')
            trans_cat = groups[4]
            merch_filtered = merch[merch['category'] == trans_cat]
            random_row = merch_filtered.loc[random.sample(
                list(merch_filtered.index), 1)]
            # sw added list
            chosen_merchant = random_row.iloc[0]['merchant_name']

            cust_lat = cust.attrs['lat']
            cust_long = cust.attrs['long']

            if is_traveling:
                # hacky math.. assuming ~70 miles per 1 decimal degree of lat/long
                # sorry for being American, you're on your own for kilometers.
                rad = (float(travel_max) / 100) * 1.43

                # geo_coordinate() uses uniform distribution with lower = (center-rad), upper = (center+rad)
                merch_lat = fake.coordinate(center=float(cust_lat), radius=rad)
                merch_long = fake.coordinate(
                    center=float(cust_long), radius=rad)
            else:
                # otherwise not traveling, so use 1 decimial degree (~70mile) radius around home address
                rad = 1
                merch_lat = fake.coordinate(center=float(cust_lat), radius=rad)
                merch_long = fake.coordinate(
                    center=float(cust_long), radius=rad)

            # if cust.attrs['profile'] == "male_30_40_smaller_cities.json":
            print_str = self.customer.replace('\n', '') + '|' + t + '|' + str(
                chosen_merchant) + '|' + str(merch_lat) + '|' + str(merch_long)
            # print(print_str)
            df = pd.DataFrame({'temp_str': [print_str]})
            df[['ssn', 'cc_num', 'first', 'last', 'gender', 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop', 'job', 'dob', 'acct_num', 'profile', 'trans_num',
                'trans_date', 'trans_time', 'unix_time', 'category', 'amt', 'is_fraud', 'merchant', 'merch_lat', 'merch_long']] = df['temp_str'].str.split('|', 0, expand=True)
            df['ip_address'] = fake.ipv4()
            global_transaction_df_online = pd.concat(
                [global_transaction_df_online, df], ignore_index=True, axis=0)



    def clean_line(self, line):
        # separate into a list of attrs
        cols = [c.replace('\n', '') for c in line.split('|')]
        # create a dict of name:value for each column
        attrs = {}
        for i in range(len(cols)):
            attrs[headers[i].replace('\n', '')] = cols[i].replace('\n', '')
        return attrs


if __name__ == '__main__':
    # read user input into Inputs object
    # to prepare the user inputs
    # curr_profile is female_30_40_smaller_cities.json , for fraud as well as non fraud
    # profile_name is ./profiles/fraud_female_30_40_bigger_cities.json for fraud.
    customers, pro, pro_fraud, curr_profile, curr_fraud_profile, start, end, profile_name = get_user_input()

    headers = create_header(customers[0])

    # generate Faker object to calc merchant transaction locations
    fake = Faker()

    column_names = ['ssn', 'cc_num', 'first', 'last', 'gender', 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop', 'job', 'dob', 'acct_num',
                    'profile', 'trans_num', 'trans_date', 'trans_time', 'unix_time', 'category', 'amt', 'is_fraud', 'merchant', 'merch_lat', 'merch_long']

    global_transaction_df_in_store = pd.DataFrame(columns=column_names)

    online_purchase_column_names = ['ssn', 'cc_num', 'first', 'last', 'gender', 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop', 'job', 'dob', 'acct_num',
                    'profile', 'trans_num', 'trans_date', 'trans_time', 'unix_time', 'category', 'amt', 'is_fraud', 'merchant', 'merch_lat', 'merch_long']

    global_transaction_df_online = pd.DataFrame(columns=online_purchase_column_names)
    # for each customer, if the customer fits this profile
    # generate appropriate number of transactions
    for line in customers[1:]:
        profile = profile_weights.Profile(pro, start, end)
        cust = Customer(line, profile)

        if cust.attrs['profile'] == curr_profile:
            merch = pd.read_csv('data/merchants.csv', sep='|')
            is_fraud = 0

            # set fraud flag here, as we either gen real or fraud, not both for
            fraud_flag = randint(0, 100)
            # the same day.
            fraud_dates = []

            # decide if we generate fraud or not
            if fraud_flag < 99:  # 11->25
                fraud_interval = randint(1, 1)  # 7->1
                inter_val = (end-start).days-7
                # rand_interval is the random no of days to be added to start date
                rand_interval = randint(1, inter_val)
                # random start date is selected
                newstart = start + datetime.timedelta(days=rand_interval)
                # based on the fraud interval , random enddate is selected
                newend = newstart + datetime.timedelta(days=fraud_interval)
                # we assume that the fraud window can be between 1 to 7 days #7->1
                profile = profile_weights.Profile(pro_fraud, newstart, newend)
                cust = Customer(line, profile)
                merch = pd.read_csv('data/merchants.csv', sep='|')
                is_fraud = 1
                temp_tx_data = profile.sample_from(is_fraud)
                fraud_dates = temp_tx_data[3]
                cust.print_trans_and_append_df(
                    temp_tx_data, is_fraud, fraud_dates)
                #parse_index = m.index('profiles/') + 9
                #m = m[:parse_index] +'fraud_' + m[parse_index:]

            # we're done with fraud (or didn't do it) but still need regular transactions
            # we pass through our previously selected fraud dates (if any) to filter them
            # out of regular transactions
            profile = profile_weights.Profile(pro, start, end)
            merch = pd.read_csv('data/merchants.csv', sep='|')
            is_fraud = 0
            temp_tx_data = profile.sample_from(is_fraud)
            cust.print_trans_and_append_df(temp_tx_data, is_fraud, fraud_dates)
            cust.print_trans_and_append_df_online(temp_tx_data, is_fraud, fraud_dates)


            # we also generate online transactions here. Assuming the online transactions don't have labels for fraud

    global_transaction_df_in_store['payment_type']='in_store'
    global_transaction_df_in_store.to_csv(
        "./output/in_store_transaction.csv", sep='|', header=True, index=False)
    global_transaction_df_in_store.to_parquet("./output/in_store_transaction.parquet")

    global_transaction_df_online['payment_type']='online'
    global_transaction_df_online.drop(["temp_str", 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop',  'profile','is_fraud','merch_lat','merch_long'], inplace=True, axis=1)
    global_transaction_df_online.to_csv(
        "./output/online_transaction.csv", sep='|', header=True, index=False)
    global_transaction_df_online.to_parquet("./output/online_transaction.parquet")


    # generate fake embeddings
    user_embedding_df = pd.DataFrame(columns=["ssn", "embedding"])
    unique_ssn = global_transaction_df_in_store['ssn'].unique()
    for ssn in unique_ssn:
        df = pd.DataFrame({'ssn': ssn, "embedding": [np.random.random((5,5)).tolist()] })
        user_embedding_df = pd.concat(
            [user_embedding_df, df], ignore_index=True, axis=0)
    user_embedding_df.to_csv(
        "./output/user_embedding.csv", sep='|', header=True, index=False)
    user_embedding_df.to_parquet("./output/user_embedding.parquet")
