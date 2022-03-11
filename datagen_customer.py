import faker
from faker import Faker
import random
import numpy as np
import sys
import datetime
from datetime import date
from datetime import timedelta
import fileinput
import random
from collections import defaultdict
import json
from main_config import MainConfig



class Headers(object):
    'Store the headers and print to stdout to pipe into csv'

    def __init__(self):
        self.make_headers()
        self.print_headers()

    def make_headers(self):
        headers = ''
        for h in ['ssn', 'cc_num', 'first', 'last', 'gender', 'street',
                  'city', 'state', 'zip', 'lat', 'long', 'city_pop',
                  'job', 'dob', 'acct_num', 'profile']:
            headers += h + '|'
        self.headers = headers[:-1]

    def print_headers(self):
        print(self.headers)


class Customer(object):
    'Randomly generates all the attirubtes for a customer'

    def __init__(self):
        self.ssn = fake.ssn()
        self.gender, self.dob = self.generate_age_gender()
        self.first = self.get_first_name()
        self.last = fake.last_name()
        self.street = fake.street_address()
        self.addy = self.get_random_location()
        self.job = fake.job()
        self.cc = fake.credit_card_number()
        self.email = fake.email()
        self.account = fake.random_number(digits=12)
        self.profile = self.find_profile()
        self.print_customer()

    def get_first_name(self):
        if self.gender == 'M':
            return fake.first_name_male()
        else:
            return fake.first_name_female()

    def generate_age_gender(self):
        #g_a = age_gender[min([a for a in age_gender if a > np.random.random()])]
        #g_a = age_gender[min(age_gender, key=lambda x:abs(x-random.random()))]

        a = np.random.random()
        c = []
        for b in age_gender.keys():
            if b > a:
                c.append(b)
        g_a = age_gender[min(c)]

        while True:
            dob = fake.date_time_this_century()

            # adjust the randomized date to yield the correct age
            start_age = (date.today() - date(dob.year,
                         dob.month, dob.day)).days / 365.
            dob_year = dob.year - int(g_a[1] - int(start_age))

            # since the year is adjusted, sometimes Feb 29th won't be a day
            # in the adjusted year
            try:
                # return first letter of gender and dob
                return g_a[0][0], date(dob_year, dob.month, dob.day)
            except:
                pass

    # find nearest city
    def get_random_location(self):
        return cities[min(cities, key=lambda x: abs(x - random.random()))]

    def find_profile(self):
        age = (date.today() - self.dob).days / 365.25
        city_pop = float(self.addy.split('|')[-1])

        match = []
        for pro in all_profiles:
            # -1 represents infinity
            if self.gender in all_profiles[pro]['gender'] and \
                age >= all_profiles[pro]['age'][0] and \
                    (age < all_profiles[pro]['age'][1] or
                     all_profiles[pro]['age'][1] == -1) and \
                city_pop >= all_profiles[pro]['city_pop'][0] and \
                    (city_pop < all_profiles[pro]['city_pop'][1] or
                     all_profiles[pro]['city_pop'][1] == -1):
                match.append(pro)
        if match == []:
            match.append('leftovers.json')

        # found overlap -- write to log file but continue
        if len(match) > 1:
            f = open('profile_overlap_warnings.log', 'a')
            output = ' '.join(match) + ': ' + self.gender + ' ' + \
                     str(age) + ' ' + str(city_pop) + '\n'
            f.write(output)
            f.close()
        return match[0]

    def print_customer(self):
        print(str(self.ssn) + '|' +
              str(self.cc) + '|' +
              self.first + '|' +
              self.last + '|' +
              self.gender + '|' +
              self.street + '|' +
              self.addy + '|' +
              self.job + '|' +
              str(self.dob) + '|' +
              str(self.account) + '|' +
              self.profile)

def make_cities():
    cities = {}
    f = open('./data/locations_partitions.csv', 'r').readlines()
    for line in f:
        try:
            cdf, output = line.replace('\n', '').split(',')
            cities[float(cdf)] = output
        # header
        except:
            pass
    return cities


def make_age_gender_dict():
    gender_age = {}
    prev = 0
    f = open('./data/age_gender_demographics.csv', 'r').readlines()
    for line in f:
        l = line.replace('\n', '').split(',')
        if l[3] != 'prop':
            prev += float(l[3])
            gender_age[prev] = (l[2], float(l[1]))
    return gender_age



def validate():
    def print_err(n):
        if n == 1:
            print('Error: invalid number of customers')
        elif n == 2:
            print('Error: invalid (non-integer) random seed')
        else:
            print('Error: main.config could not be opened')

        output = '\nENTER:\n (1) Number of customers\n '
        output += '(2) Random seed (int)\n '
        output += '(3) main_config.json'

        print(output)
        sys.exit(0)

    try:
        num_cust = int(sys.argv[1])
        ## num_cust = 15
    except:
        print_err(1)
    try:
        seed_num = int(sys.argv[2])
        ## seed_num = 4444
    except:
        print_err(2)
    try:
        m = sys.argv[3]
        ## m = 'profiles/main_config.json'
        main = open(m, 'r').read()
    except:
        print_err(3)

    return num_cust, seed_num, main


if __name__ == '__main__':
    # read and validate stdin
    num_customer, seed_num, main = validate()

    # from demographics module
    cities = make_cities()
    age_gender = make_age_gender_dict()

    fake = Faker()
    Faker.seed(seed_num)

    headers = Headers()

    # turn all profiles into dicts to work with
    all_profiles = MainConfig(main).config

    for _ in range(num_customer):
        Customer()
