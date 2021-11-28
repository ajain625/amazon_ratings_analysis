from data_processing import sort_by_products, product_data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Process data to contain all relevant information

#raw_data = pd.read_csv(r"C:\Users\Mona Jain.000\Downloads\Movies_and_TV.csv", delimiter=',')
raw_data = pd.read_csv(r"C:\Users\Mona Jain.000\Downloads\Clothing_Shoes_and_Jewelry.csv", delimiter=',')

product_sorted_data = sort_by_products(raw_data)
product_data_reviews_ratings = product_data(product_sorted_data)

product_df = pd.DataFrame(product_data_reviews_ratings, columns = ('Total Ratings', 'Average Rating'))

"""
product_df.plot.scatter(x='Total Ratings', y='Average Rating')
plt.show()

"""
total_ratings_range = 20
#averaged_ratings_product_data = []
product_number_of_ratings = np.arange(1, total_ratings_range + 1)
product_average_ratings = np.zeros(total_ratings_range)
for i in range(1, total_ratings_range + 1):
    i_total_ratings = product_df[product_df['Total Ratings'] == i]
    product_average_ratings[i-1] = i_total_ratings["Average Rating"].mean()


#averaged_ratings_product_df = pd.DataFrame(averaged_ratings_product_data, columns=('Total Ratings', 'Average Rating'))
#averaged_ratings_product_df.plot.scatter(x='Total Reviews', y ='Average Rating')
#averaged_ratings_product_df = averaged_ratings_product_df.dropna()
#print(averaged_ratings_product_df)
#plt.show()
#product_average_ratings = averaged_ratings_product_df["Average Rating"].to_numpy()
#product_number_of_ratings = averaged_ratings_product_df['Total Ratings'].to_numpy()

#linear_regression = sm.OLS(product_average_ratings,sm.add_constant(product_number_of_ratings)).fit()
#print(linear_regression.summary())
#sns.regplot(data = averaged_ratings_product_df, x='Total Reviews', y='Average Rating')
#plt.show()

m, b = np.polyfit(product_number_of_ratings, product_average_ratings, 1)
print(m, b)
plt.plot(product_number_of_ratings, product_average_ratings, 'bo')
plt.plot(product_number_of_ratings, m*product_number_of_ratings + b, 'r-')
plt.show()


# Analysis of initial rating vs the total product reviews
"""
allData = rating_data(product_sorted_data)
df = pd.DataFrame(allData, columns = ('Review Number', 'Average Rating so far', 'Rating', 'Next Rating', 'Average Product Rating', 'Average Rounded Product Rating', 'Time Since Last Review', 'Time to Next Review', 'Total Product Reviews'))

df2 = df[df['Review Number'] == 1]
#df2['Total Product Reviews'] = df2['Total Product Reviews'].map(lambda x: math.log(x))

test = []
for i in range(1,6):
    rating_data = df2[df2['Rating'] == i]
    test.append([i, rating_data["Total Product Reviews"].mean(), rating_data["Total Product Reviews"].std()])


print(test)
#What does increasing standard deviation imply here?

"""
# Analysis of average product reviews as a function of intial-average rating
"""
df3 = df[df['Review Number'] == 1]
df3["Average - Initial"] = df3['Average Product Rating'] - df3['Rating']

#print(df3["Average - Initial"].mean()
# This is -0.05. Statistically significant?

df3["Average - Initial rounded to tenths"] = df3["Average - Initial"].map(lambda x: round(x, 1))


rating = []
reviews = []
for i in range(100):
    rating_data = df3[df3['Average - Initial rounded to tenths'] == (50-i)/10]
    rating.append((50-i)/10)
    reviews.append(rating_data["Total Product Reviews"].mean())

#sns.scatterplot(data = df3, x = "Average - Initial rounded to tenths", y = "Total Product Reviews")
plt.scatter(rating, reviews)
plt.show()
"""

# Analysis of Average Rating vs Total Reviews