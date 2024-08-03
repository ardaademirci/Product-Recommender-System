import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np



# Load the CSV data
file_path = 'dataset.csv'  # Change this to your CSV file's path
# Try different encodings if UTF-8 fails
possible_encodings = ['utf-8', 'ISO-8859-1', 'cp1252']

df = None
for encoding in possible_encodings:
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        print(f"Successfully read the CSV file with '{encoding}' encoding.")
        break
    except UnicodeDecodeError as e:
        print(f"Failed to read with '{encoding}' encoding: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if df is None:
    raise Exception("Failed to read the CSV file with all attempted encodings.")

# If successfully read, proceed with the rest of the code
print("First few rows of the dataframe:")
print(df.head())

# Data cleaning
# Drop duplicates in case there are any, and remove rows with missing values
df.drop_duplicates(inplace=True)
df.dropna(subset=['CustomerID', 'StockCode'], inplace=True)

# Create a mapping from StockCode to Description
product_descriptions = df.drop_duplicates(subset=['StockCode']).set_index('StockCode')['Description']


# Create a pivot table to get customer-product interactions
# This creates a binary matrix where rows are customers and columns are products
customer_product_matrix = (
    df.pivot_table(index='CustomerID', columns='StockCode', values='Quantity', aggfunc='sum')
    .fillna(0)
    # .applymap(lambda x: 1 if x > 0 else 0)
)

# Instead of .applymap, use .apply with lambda to create a binary matrix
customer_product_binary_matrix = customer_product_matrix.apply(
    lambda x: x.map(lambda y: 1 if y > 0 else 0), axis=1
)

# Create the KNN model using KDTree
knn = NearestNeighbors(metric='euclidean', algorithm='kd_tree', n_neighbors=5)

# Fit the model to the customer-product matrix
knn.fit(customer_product_matrix)

# Function to get recommendations for a given customer
def get_recommendations(customer_id, n_recommendations=3):
    customer_index = customer_product_matrix.index.get_loc(customer_id)
    distances, indices = knn.kneighbors(customer_product_matrix.iloc[[customer_index]])
    
    similar_customers = indices[0]
    customer_products = customer_product_matrix.iloc[customer_index]
    
    # Find products that the customer has not purchased
    non_purchased_products = customer_product_matrix.columns[customer_products == 0]
    
    # Count the number of similar customers who have purchased each non-purchased product
    product_recommendations = non_purchased_products.to_series().apply(
        lambda product: customer_product_matrix.iloc[similar_customers][product].sum()
    )
    
    # Get the top n_recommendations products
    top_recommendations = product_recommendations.nlargest(n_recommendations).index.tolist()
    
    return top_recommendations

# Generate recommendations for each customer and store them in a list
recommendations_list = []

# for customer_id in customer_product_matrix.index:
#     recommendations = get_recommendations(customer_id)
#     recommendations_list.append({
#         'CustomerID': customer_id,
#         'RecommendedProducts': recommendations
#     })
#     # print(recommendations_list)
#     # print("---------------------------")
#     print(customer_id)

#   Burası her bir özelliğe bir kolon ayırıyor.
for customer_id in customer_product_matrix.index:
    recommendations = get_recommendations(customer_id)
    # Ensure that the length of recommendations is always n_recommendations
    while len(recommendations) < 3:
        recommendations.append(None)  # Pad with None if fewer than 3 recommendations
    recommendations_list.append({
        'CustomerID': customer_id,
        'RecommendedProduct1': recommendations[0],
        'RecommendedProduct2': recommendations[1],
        'RecommendedProduct3': recommendations[2]
    })
    print(customer_id)



# Convert the recommendations list to a DataFrame and save to CSV
recommendations_df = pd.DataFrame(recommendations_list)

output_path = 'knn_customer_recommendations.xlsx'  # Change this to your desired output file name
recommendations_df.to_excel(output_path, index=False)

print("Recommendations saved to", output_path)
