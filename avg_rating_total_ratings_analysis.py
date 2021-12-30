from data_processing import sort_by_products, product_data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Process data to contain all relevant information

# Fill in with csv data file path for analysis
raw_data = pd.read_csv(r"", delimiter=',')


product_sorted_data = sort_by_products(raw_data)
product_data_reviews_ratings = product_data(product_sorted_data)

product_df = pd.DataFrame(product_data_reviews_ratings, columns = ('Total Ratings', 'Average Rating'))

total_ratings_range = 40
#averaged_ratings_product_data = []
product_number_of_ratings = np.arange(1, total_ratings_range + 1)
product_average_ratings = np.zeros(total_ratings_range)
for i in range(1, total_ratings_range + 1):
    i_total_ratings = product_df[product_df['Total Ratings'] == i]
    product_average_ratings[i-1] = i_total_ratings["Average Rating"].mean()


m, b = np.polyfit(product_number_of_ratings, product_average_ratings, 1)
print(m, b)
plt.plot(product_number_of_ratings, product_average_ratings, 'bo')
plt.plot(product_number_of_ratings, m*product_number_of_ratings + b, 'r-')
plt.title("Rating to Performance Analysis")
plt.xlabel("Total Ratings")
plt.ylabel("Average Product Rating")
plt.show()