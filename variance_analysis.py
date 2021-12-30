# Analysis of mean of squared difference between rating and average rating vs rating number

from data_processing import sort_by_products, rating_data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Process data to contain all relevant information

# Fill in with csv file path for analysis
#raw_data = pd.read_csv(r"", delimiter=',')


product_sorted_data = sort_by_products(raw_data)
rating_df = rating_data(product_sorted_data)

# Identify only those ratings for which the product has more than a certain number of total ratings
min_total_ratings = 300
variance_df = rating_df[rating_df["Total Product Ratings"] > min_total_ratings]
print(variance_df.shape)

# Create new column with square of difference of that particular rating and the final average product rating
variance_df["Average - Current Rating"] = variance_df['Average Product Rating'] - variance_df['Rating']
variance_df["Square of Average - Current Rating"] = variance_df["Average - Current Rating"].map(lambda x: x**2)

# Create and populate numpy arrays with the rating number and variance. Variance for the ith rating is calculated as follows: 
# First look at the ith rating of a certain product and take the square of its difference from the final average product rating.
# Then, take the mean of all these squares over all products/
mean_diff = np.zeros(min_total_ratings)
review_num = np.arange(1, min_total_ratings + 1)
for i in range(min_total_ratings):
    nth_ratings = variance_df[variance_df["Rating Number"] == i+1]   
    mean_diff[i] = nth_ratings["Square of Average - Current Rating"].mean()

# Plot the data along with the line of best fit
slope, yintercept = np.polyfit(review_num, mean_diff, 1)
print(slope, yintercept)
plt.scatter(review_num, mean_diff)
plt.plot(review_num,  slope*review_num + yintercept, 'r-')
plt.title("Variance Analysis")
plt.xlabel("Rating Number (N)")
plt.ylabel("Variance of Nth Rating")
plt.show()

#Future Ideas: Compare datasets of different types of products; Different Values of min_total_ratings; Calculate T values
