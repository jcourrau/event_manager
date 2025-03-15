from datetime import datetime


''' Test Cases'''
test_cases = {
    # Test Case 1:
    "Adding a new weekly event on Mondays":
        {
            "name": "Monday Sync",
            "start_date": datetime(2024, 3, 4),
            "recurrent_type": "n-weekly",
            "interval": 1,
            "days_of_week": [0]
        },

    # Test Case 2:
    "Adding a new bi-weekly event on Wednesdays":
        {
            "name": "Bi-Weekly Stand-up",
            "start_date": datetime(2024, 3, 6),
            "recurrent_type": "n-weekly",
            "interval": 2,
            "days_of_week": [2]
        },

    # Test Case 3:
    "Adding a new monthly event on the 15th":
        {
            "name": "Mid-Month Review",
            "start_date": datetime(2024, 3, 15),
            "recurrent_type": "monthly",
            "days_of_month": [15]
        },

    # Test Case 4:
    "Adding a weekly event overlapping multiple existing events":
        {
            "name": "Busy Monday",
            "start_date": datetime(2024, 3, 4),
            "recurrent_type": "n-weekly",
            "interval": 1,
            "days_of_week": [0, 3]
        },

    # Test Case 5:
    "Adding an event far into the future":
        {
            "name": "Yearly Review",
            "start_date": datetime(2025, 3, 1),
            "recurrent_type": "monthly",
            "days_of_month": [1]
        },

    # Test Case 6:
    "Weekly Salary Deposit":
        {
            "name": "Weekly Salary",
            "start_date": datetime(2024, 3, 1),
            "recurrent_type": "n-weekly",
            "interval": 1,
            "days_of_week": [4]
        },

    # Test Case 7:
    "Bi-weekly Grocery Shopping":
        {
            "name": "Grocery Shopping",
            "start_date": datetime(2024, 3, 3),
            "recurrent_type": "n-weekly",
            "interval": 2,
            "days_of_week": [6]
        },

    # Test Case 8:
    "Monthly Rent Payment":
        {
            "name": "Rent",
            "start_date": datetime(2024, 3, 1),
            "recurrent_type": "monthly",
            "days_of_month": [1]
        },

    # Test Case 9:
    "Electric Bill Payment":
        {
            "name": "Electric Bill",
            "start_date": datetime(2024, 3, 15),
            "recurrent_type": "monthly",
            "days_of_month": [15]
        },

    # Test Case 10:
    "One-time Medical Expense":
        {
            "name": "Medical Check-up",
            "start_date": datetime(2024, 4, 5),
            "end_date": datetime(2024, 4, 5)
        },

    # Test Case 11:
    "Monthly Savings Contribution":
        {
            "name": "Savings Contribution",
            "start_date": datetime(2024, 3, 10),
            "recurrent_type": "monthly",
            "days_of_month": [10]
        },

    # Test Case 12:
    "Bi-weekly Transport Card Recharge":
        {
            "name": "Transport Card Recharge",
            "start_date": datetime(2024, 3, 7),
            "recurrent_type": "n-weekly",
            "interval": 2,
            "days_of_week": [3]
        },

    # Test Case 13:
    "Annual Insurance Payment":
        {
            "name": "Annual Insurance",
            "start_date": datetime(2024, 3, 20),
            "recurrent_type": "monthly",
            "days_of_month": [20]
        }

}

if __name__ == "__main__":
    import pandas as pd
    from event_class import count_weekly_events, summary_weekly_events
    from test import existing_events

    ''' Generate Dates '''
    n = 1
    test_cases_df = pd.DataFrame()
    test_tittles_dic = {}

    # Test Results.
    for tittle, new_event_data in test_cases.items():

        # Summary
        print(f"Test Case {n}: {tittle}")
        scenario = count_weekly_events(new_event_data, existing_events)
        print(summary_weekly_events(scenario),"\n")

        # Add test data to dataframe
        temp_df = pd.DataFrame(list(scenario.items()), columns=["Date", "Value"])
        temp_df["Test Number"] = n
        test_cases_df = pd.concat([test_cases_df, temp_df], ignore_index=True)

        # Test tittle data
        #test_tittles_dic[n] = tittle

        n += 1


    #test_tittles_df = pd.DataFrame(list(test_tittles_dic.items()), columns=['Test case', 'Test Number'])

    ''' Export Test Cases Data '''
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(test_cases, orient='index')

    # Reset index to include case names and add case numbers
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'case_description'}, inplace=True)
    df.insert(0, 'case_number', range(1, len(df) + 1))

    # Export data
    print(test_cases_df.head(5))
    #print(test_tittles_df.head(5))
    print(df.head(5))
    #test_cases_df.to_csv(f"test_cases {datetime.now().strftime("%m%d%Y-%H%M%S")}.csv")
    #test_cases_df.to_csv(f"test_cases {datetime.now().strftime("%m%d%Y-%H%M%S")}.csv")


