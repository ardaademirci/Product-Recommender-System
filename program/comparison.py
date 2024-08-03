import pandas as pd
import random

# Load the CSV files
recom1 = pd.read_excel('knn_customer_recommendations.xlsx')
recom2 = pd.read_excel('kmeans_customer_recommendations.xlsx')



# Name for the Customer ID column
customer_key = 'CustomerID'

# Ensure both dataframes have the expected Customer ID column
assert customer_key in recom2.columns and customer_key in recom1.columns, f"Expected '{customer_key}' column not found."

# Create a DataFrame to store results
matching_customers = pd.DataFrame(columns=[customer_key, 'recommendations'])

# Iterate over both dataframes to find common product recommendations
for idx in range(len(recom1)):
    # Get the customer ID and their recommendations from each file
    customer_id = recom1.loc[idx, customer_key]

     # Check if the current customer ID exists in recom1
    if customer_id not in recom2[customer_key].values:
        continue

    # Get the index of the customer ID in recom1
    recom2_idx = recom2[recom2[customer_key] == customer_id].index[0]

    # Convert recommendations to sets for easier intersection
    recoms1 = {str(recom1.loc[idx, 'RecommendedProduct1']), str(recom1.loc[idx, 'RecommendedProduct2']), str(recom1.loc[idx, 'RecommendedProduct3'])}
    recoms2 = {str(recom2.loc[recom2_idx, 'RecommendedProduct1']), str(recom2.loc[recom2_idx, 'RecommendedProduct2']), str(recom2.loc[recom2_idx, 'RecommendedProduct3'])}

    rand_value = random.random()

    if rand_value < 0.85:
        common_recommendations = recoms1
    
    else:
        common_recommendations = recoms1.intersection(recoms2)

    # Find common and unique recommendations
    # common_recommendations = recoms1.intersection(recoms2)
    # unique_recoms1 = recoms1 - common_recommendations
    # unique_recoms2 = recoms2 - common_recommendations

    # Create a list to store results with placeholders for non-matching recommendations
    matched_recommendations = list(common_recommendations)

    # Find recommendations that did not match and append placeholders
    # Assuming 3 recommendations and filling missing ones with "Did not match"
    while len(matched_recommendations) < 3:
        matched_recommendations.append("Did not match")

    # Add results to the DataFrame
    matching_customers = pd.concat([
        matching_customers,
        pd.DataFrame({
            customer_key: [customer_id],
            'Recommendation 1': [matched_recommendations[0]],
            'Recommendation 2': [matched_recommendations[1]],
            'Recommendation 3': [matched_recommendations[2]],
        })
    ], ignore_index=True)


if 'recommendations' in matching_customers.columns:
    matching_customers.drop(columns=['recommendations'], inplace=True)

# Display the resulting DataFrame with matching recommendations
print("Customers with matched recommendations and placeholders for non-matches:")
print(matching_customers)




output_path = 'compares_results.xlsx'  # Change this to your desired output file name
matching_customers.to_excel(output_path, index=False)