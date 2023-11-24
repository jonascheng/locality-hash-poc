# import the required libraries
import pandas as pd
import sys
from pandas import read_csv
from pyLSHash import FuzzyHash, SimHash, hamming

fuzzy_hash = FuzzyHash()
sim_hash = SimHash()


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

        # Update the row in the dataframe
        data.loc[index] = row

    # Drop the columns fuzzy_hash
    data = data.drop(columns=['fuzzy_hash'])

    # Print the dataframe
    # print(data)

    # Return the dataframe with fuzzy hash
    return data


# Compare fuzzy hash of dataframe against an input fuzzy hash
def compare_fuzzy_hash_without_apps(data, hash: str):
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


# Compare sim hash of dataframe against an input sim hash
def compare_sim_hash(data, hash: int):
    # Create a new column sim_hash with empty string
    data['corr_sim_hash'] = ''

    # Convert the numpy.uint64 to int
    hash = int(hash)

    # Iterate through the dataframe
    for index, row in data.iterrows():
        row['corr_sim_hash'] = 1 - hamming(hash, int(row['sim_hash'])) / sim_hash.len_hash

        # Update the row in the dataframe
        data.loc[index] = row

    # Drop the columns sim_hash
    data = data.drop(columns=['sim_hash'])

    # Print the dataframe
    # print(data)

    # Return the dataframe with sim hash
    return data


# Compare sim hash of dataframe against an input sim hash
def compare_sim_hash_without_apps(data, hash: int):
    # Create a new column sim_hash with empty string
    data['corr_sim_hash_without_apps'] = ''

    # Convert the numpy.uint64 to int
    hash = int(hash)

    # Iterate through the dataframe
    for index, row in data.iterrows():
        row['corr_sim_hash_without_apps'] = corr = 1 - hamming(hash, int(row['sim_hash_without_apps'])) / sim_hash.len_hash

        # Update the row in the dataframe
        data.loc[index] = row

    # Drop the columns sim_hash_without_apps
    data = data.drop(columns=['sim_hash_without_apps'])

    # Print the dataframe
    # print(data)

    # Return the dataframe with sim hash
    return data


# Create a main function to run the program
def main(input_file, n):
    # Read the agent-telemetry.csv file
    agent_apps = load_data(input_file)

    # Drop the columns apps
    # agent_apps = agent_apps.drop(columns=['apps'])

    # Compare the sim hash of the dataframe against an input sim hash
    agent_apps = compare_sim_hash(agent_apps, agent_apps['sim_hash'][n - 1])

    # Compare the sim hash of the dataframe against an input sim hash
    agent_apps = compare_sim_hash_without_apps(agent_apps, agent_apps['sim_hash_without_apps'][n - 1])

    # Compare the fuzzy hash of the dataframe against an input fuzzy hash
    agent_apps = compare_fuzzy_hash(agent_apps, agent_apps['fuzzy_hash'][n - 1])

    # Compare the fuzzy hash of the dataframe against an input fuzzy hash
    agent_apps = compare_fuzzy_hash_without_apps(agent_apps, agent_apps['fuzzy_hash_without_apps'][n - 1])

    # Sort by column corr_fuzzy_hash_without_apps, corr_sim_hash_without_apps, corr_fuzzy_hash, corr_sim_hash
    # agent_apps = agent_apps.sort_values(by=['corr_fuzzy_hash_without_apps', 'corr_sim_hash_without_apps', 'corr_fuzzy_hash', 'corr_sim_hash'], ascending=False)

    # Sort by column corr_sim_hash_without_apps, corr_fuzzy_hash_without_apps, corr_sim_hash, corr_fuzzy_hash
    agent_apps = agent_apps.sort_values(by=['corr_sim_hash_without_apps', 'corr_fuzzy_hash_without_apps', 'corr_sim_hash', 'corr_fuzzy_hash'], ascending=False)

    # Move columns apps to the last column
    cols_at_end = ['apps']
    agent_apps = agent_apps[[c for c in agent_apps if c not in cols_at_end] + [c for c in cols_at_end if c in agent_apps]]

    # Output file name
    output_file = input_file.split('.')[0] + '-similarity.csv'

    # Write the new dataframe to corr_fuzzy_hash.csv file
    agent_apps.to_csv(output_file, index=False)


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
