# import the required libraries
import pandas as pd
from pandas import read_csv
from pyLSHash import FuzzyHash, SimHash, hamming

fuzzy_hash = FuzzyHash()


# Create a function to read the csv file and return a dataframe
def load_data(filename):
    df = read_csv(filename)
    return df


# Calculate the fuzzy hash of the dataframe, and return the dataframe with fuzzy hash
def fuzzy_hash_data(data):
    # Create a new column fuzzy_hash with empty string
    data['fuzzy_hash'] = ''
    data['fuzzy_hash_without_apps'] = ''

    # Iterate through the dataframe
    for index, row in data.iterrows():
        # Concatenate the columns cpuname,oscaption,osversion,cpucaption,osarchitecture,cpuarchitecture,apps and convert all columns to string
        stmt = str(row['cpuname']) + '|' + str(row['oscaption']) + '|' + str(row['osversion']) + '|' + str(row['cpucaption']) + '|' + str(row['osarchitecture']) + '|' + str(row['cpuarchitecture']) + '|' + str(row['apps'])
        hash = fuzzy_hash.get_hash(stmt.encode('utf-8'))
        # Convert the hash to hex string
        row['fuzzy_hash'] = hash.hex()

        # Concatenate the columns cpuname,oscaption,osversion,cpucaption,osarchitecture,cpuarchitecture and convert all columns to string
        stmt = str(row['cpuname']) + '|' + str(row['oscaption']) + '|' + str(row['osversion']) + '|' + str(row['cpucaption']) + '|' + str(row['osarchitecture']) + '|' + str(row['cpuarchitecture'])
        hash = fuzzy_hash.get_hash(stmt.encode('utf-8'))
        # Convert the hash to hex string
        row['fuzzy_hash_without_apps'] = hash.hex()

        # Update the row in the dataframe
        data.loc[index] = row

    # Print the dataframe
    print(data)

    # Return the dataframe with fuzzy hash
    return data


# Create a function to concatenate the columns caption,name,vendor with same guid
# The sample input dataframe is as follows
# ```
# serverguid,guid,caption,identifyingnumber,name,skunumber,vendor,version,installlocation
# 00eb13f0-bd54-11ed-9290-00155da02f20,02031215-83d1-49dc-bcd0-786341a6bf8a,StellarProtect,{8D895A2C-B3C5-4BE6-A0FC-A482452AA970},StellarProtect,,TXOne,2.1.0.1048,C:\Program Files\TXOne\StellarProtect\
# 00eb13f0-bd54-11ed-9290-00155da02f20,02031215-83d1-49dc-bcd0-786341a6bf8a,7-Zip 22.01 (x64 edition),{23170F69-40C1-2702-2201-000001000000},7-Zip 22.01 (x64 edition),,Igor Pavlov,22.01.00.0,
# fa6d6daa-2512-11ec-8635-005056b2d3e3,fcdace51-8abb-40b4-ad36-932925130403,,{F0C3E5D1-1ADE-321E-8167-68EF0DE699A5}.KB2467173,,,,,
# fa6d6daa-2512-11ec-8635-005056b2d3e3,fcdace51-8abb-40b4-ad36-932925130403,Intel(R) Chipset Device Software,{f2fa2583-cd6d-4da1-803c-2983cc6f7791},Intel(R) Chipset Device Software,,Intel(R) Corporation,10.1.2.10,
# ```
# The sample output dataframe is as follows, and serverguid should be preserved in the output dataframe
# ```
# serverguid,guid,caption,apps
# 00eb13f0-bd54-11ed-9290-00155da02f20,02031215-83d1-49dc-bcd0-786341a6bf8a,StellarProtect|StellarProtect|TXOne|7-Zip 22.01 (x64 edition)|7-Zip 22.01 (x64 edition)|Igor Pavlov
# fa6d6daa-2512-11ec-8635-005056b2d3e3,fcdace51-8abb-40b4-ad36-932925130403,Intel(R) Chipset Device Software|Intel(R) Chipset Device Software|Intel(R) Corporation
# ```
def merge_sw_by_serverguid_guid(data):
    # Drop the columns identifyingnumber,skunumber,version,installlocation
    data = data.drop(columns=['identifyingnumber', 'skunumber', 'version', 'installlocation'])

    # Select distinct tuple (serverguid, guid) from input dataframe and insert into new dataframe
    df = data[['serverguid', 'guid']].drop_duplicates()
    # Create a new column apps with empty string
    df['apps'] = ''

    # Iterate through the new dataframe
    for index, row in df.iterrows():
        # Select the rows from the input dataframe where serverguid and guid are same as the new dataframe
        subset_data = data[(data['serverguid'] == row['serverguid']) & (data['guid'] == row['guid'])]
        # Drop the columns serverguid and guid
        subset_data = subset_data.drop(columns=['serverguid', 'guid'])
        # Drop the duplicate rows
        subset_data = subset_data.drop_duplicates()

        # Print the subset dataframe
        # print(subset_data)

        # Create an empty array of string for concatenation
        apps = []

        # Iterate through the subset dataframe
        for index1, row1 in subset_data.iterrows():
            # Skip the row if caption,name,vendor are null
            if pd.isnull(row1['caption']) or pd.isnull(row1['name']) or pd.isnull(row1['vendor']):
                continue
            # Concatenate the columns caption,name,vendor with same guid, and convert all columns to string
            apps.append(str(row1['caption']) + '|' + str(row1['name']) + '|' + str(row1['vendor']))

        # Concatenate the array of string with pipe delimiter
        row['apps'] = '|'.join(apps)

        # Update the row in the new dataframe
        df.loc[index] = row

        # Print the row
        # print(row)

    # Print new dataframe
    # print(df)

    # Write the new dataframe to apps.csv file
    # df.to_csv('apps.csv', index=False)

    return df


# Create a function to merge two input dataframes by serverguid and guid
# The sample input dataframes are as follows
# ```
# serverguid,guid,cpuname,oscaption,osversion,cpucaption,osarchitecture,cpuarchitecture
# 00eb13f0-bd54-11ed-9290-00155da02f20,006437bb-46a9-4fbb-bf45-ef921cdf25bd,,Microsoft Windows 10 企業版 LTSC,10.0.17763,,64 位元,
# 00eb13f0-bd54-11ed-9290-00155da02f20,02031215-83d1-49dc-bcd0-786341a6bf8a,,Microsoft Windows 7 專業版 ,6.1.7601,,64-bit,
# ```
# ```
# serverguid,guid,apps
# 00eb13f0-bd54-11ed-9290-00155da02f20,006437bb-46a9-4fbb-bf45-ef921cdf25bd,app1|app2|app3
# 00eb13f0-bd54-11ed-9290-00155da02f20,02031215-83d1-49dc-bcd0-786341a6bf8a,application1|application2|application3
# ```
# The sample output dataframe is as follows, and serverguid should be preserved in the output dataframe
# ```
# serverguid,guid,cpuname,oscaption,osversion,cpucaption,osarchitecture,cpuarchitecture,apps
# 00eb13f0-bd54-11ed-9290-00155da02f20,006437bb-46a9-4fbb-bf45-ef921cdf25bd,,Microsoft Windows 10 企業版 LTSC,10.0.17763,,64 位元,,app1|app2|app3
# 00eb13f0-bd54-11ed-9290-00155da02f20,02031215-83d1-49dc-bcd0-786341a6bf8a,,Microsoft Windows 7 專業版 ,6.1.7601,,64-bit,,application1|application2|application3
# ```
def merge_by_serverguid_guid(data1, data2):
    # Merge two dataframes by serverguid and guid
    df = pd.merge(data1, data2, on=['serverguid', 'guid'], how='outer')

    # Drop the rows where apps is null
    df = df.dropna(subset=['apps'])

    # Print the new dataframe
    print(df)

    return df


# Create a main function to run the program
def main():
    # Read the agent-telemetry.csv file
    agents = load_data('metabase/agent-telemetry.csv')

    # Read the agent-sw-telemetry.csv file
    sw = load_data('metabase/agent-sw-telemetry.csv')

    # Merge the application data
    apps = merge_sw_by_serverguid_guid(sw)

    # Merge the agent data and application data
    agent_apps = merge_by_serverguid_guid(agents, apps)

    # Calculate the fuzzy hash of the dataframe, and return the dataframe with fuzzy hash
    agent_apps = fuzzy_hash_data(agent_apps)

    # Write the output to agent-apps-{serverguid}.csv file, and group by serverguid into different files
    for serverguid in agent_apps['serverguid'].unique():
        # Output file name is agent-apps-{serverguid}.csv
        output_file = f'agent-apps-{serverguid}.csv'
        agent_apps[agent_apps['serverguid'] == serverguid].to_csv(output_file, index=False)


# Call the main function
if __name__ == '__main__':
    main()
