# import the required libraries
import pandas as pd
import sys
from pandas import read_csv
from pyLSHash import FuzzyHash, SimHash, hamming

fuzzy_hash = FuzzyHash()


# Create a function to read the csv file and return a dataframe
def load_data(filename):
    df = read_csv(filename)
    return df


# Compare fuzzy hash of dataframe against an input fuzzy hash
def compare_fuzzy_hash(data, hash: str):
    # Create a new column fuzzy_hash with empty string
    data['corr_fuzzy_hash'] = ''

    # Convert hex string to bytes
    hash = bytes.fromhex(hash)
    # print(hash)

    # Iterate through the dataframe
    for index, row in data.iterrows():
        row['corr_fuzzy_hash'] = fuzzy_hash.compare(hash, bytes.fromhex(row['fuzzy_hash']))
        # print('corr = {}%'.format(row['corr_fuzzy_hash']))

        # Update the row in the dataframe
        data.loc[index] = row

    # Drop the columns fuzzy_hash
    data = data.drop(columns=['fuzzy_hash'])

    # Print the dataframe
    # print(data)

    # Return the dataframe with fuzzy hash
    return data


# Compare fuzzy hash of dataframe against an input fuzzy hash
def compare_fuzzy_hash_without_apps(data, hash):
    # Create a new column fuzzy_hash with empty string
    data['corr_fuzzy_hash_without_apps'] = ''

    # Convert hex string to bytes
    hash = bytes.fromhex(hash)
    # print(hash)

    # Iterate through the dataframe
    for index, row in data.iterrows():
        row['corr_fuzzy_hash_without_apps'] = fuzzy_hash.compare(hash, bytes.fromhex(row['fuzzy_hash_without_apps']))

        # Update the row in the dataframe
        data.loc[index] = row

    # Drop the columns fuzzy_hash_without_apps
    data = data.drop(columns=['fuzzy_hash_without_apps'])

    # Print the dataframe
    # print(data)

    # Return the dataframe with fuzzy hash
    return data


# Create a main function to run the program
def main(input_file, n):
    # Read the agent-telemetry.csv file
    agent_apps = load_data(input_file)

    # Drop the columns apps
    agent_apps = agent_apps.drop(columns=['apps'])

    # Get the fuzzy hash of the dataframe from n-th row
    fuzzy_hash = agent_apps['fuzzy_hash'][n - 1]

    # Compare the fuzzy hash of the dataframe against an input fuzzy hash
    agent_apps = compare_fuzzy_hash(agent_apps, fuzzy_hash)

    # Get the fuzzy hash of the dataframe from n-th row
    fuzzy_hash_without_apps = agent_apps['fuzzy_hash_without_apps'][n - 1]

    # Compare the fuzzy hash of the dataframe against an input fuzzy hash
    agent_apps = compare_fuzzy_hash_without_apps(agent_apps, fuzzy_hash_without_apps)

    # Sort by column corr_fuzzy_hash_without_apps and corr_fuzzy_hash
    agent_apps = agent_apps.sort_values(by=['corr_fuzzy_hash_without_apps', 'corr_fuzzy_hash'], ascending=False)

    # Write the new dataframe to corr_fuzzy_hash.csv file
    agent_apps.to_csv('corr_fuzzy_hash.csv', index=False)


# Call the main function
if __name__ == '__main__':
    # The script support two arguments
    # 1. input file name
    # 2. input n-th row to compare with the rest of the dataframe

    # Get first argument as input file name
    input_file = sys.argv[1]
    # Get second argument as n-th row to compare with the rest of the dataframe
    n = int(sys.argv[2])

    main(input_file, n)
