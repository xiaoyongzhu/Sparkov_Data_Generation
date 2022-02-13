#!/bin/bash
python datagen_customer.py 10000 4144 profiles/main_config.json >>./output/customers.csv

python datagen_transaction.py ./output/customers.csv ./profiles/adults_2550_female_rural.json 1-1-2021 12-31-2022 >>./output/adults_2550_female_rural.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/adults_2550_female_urban.json 1-1-2021 12-31-2022 >>./output/adults_2550_female_urban.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/adults_2550_male_rural.json 1-1-2021 12-31-2022 >>./output/adults_2550_male_rural.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/adults_2550_male_urban.json 1-1-2021 12-31-2022 >>./output/adults_2550_male_urban.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/young_adults_female_rural.json 1-1-2021 12-31-2022 >>./output/young_adults_female_rural.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/young_adults_female_urban.json 1-1-2021 12-31-2022 >>./output/young_adults_female_urban.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/young_adults_male_rural.json 1-1-2021 12-31-2022 >>./output/young_adults_male_rural.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/young_adults_male_urban.json 1-1-2021 12-31-2022 >>./output/young_adults_male_urban.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/adults_50up_female_rural.json 1-1-2021 12-31-2022 >>./output/adults_50up_female_rural.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/adults_50up_female_urban.json 1-1-2021 12-31-2022 >>./output/adults_50up_female_urban.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/adults_50up_male_rural.json 1-1-2021 12-31-2022 >>./output/adults_50up_male_rural.csv &
python datagen_transaction.py ./output/customers.csv ./profiles/adults_50up_male_urban.json 1-1-2021 12-31-2022 >>./output/adults_50up_male_urban.csv &
