from data_processing import sort_by_products, rating_data

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rawData = pd.read_csv(r"C:\Users\Mona Jain.000\Downloads\Movies_and_TV.csv", delimiter=',')
#rawData = pd.read_csv(r"C:\Users\Mona Jain.000\Downloads\Clothing_Shoes_and_Jewelry(1).csv", delimiter=',')

product_sorted_data = sort_by_products(rawData)



#allData = rating_data(product_sorted_data)
#df = pd.DataFrame(allData, columns = ('Review Number', 'Average Rating so far', 'Rating', 'Next Rating', 'Average Product Rating', 'Average Rounded Product Rating', 'Time Since Last Review', 'Time to Next Review', 'Total Product Reviews'))


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

# Analysis of mean of squared difference between rating and average rating vs rating number

# Process data to contain all relevant information
df = rating_data(product_sorted_data)

# Identify only those ratings for which the product has more than a certain number of total ratings
min_total_reviews = 300
df4 = df[df["Total Product Ratings"] > min_total_reviews]
print(df4.shape)

# Create new column with square of difference of that particular rating and the final average product rating
df4["Average - Current Rating"] = df4['Average Product Rating'] - df4['Rating']
df4["Square of Average - Current Rating"] = df4["Average - Current Rating"].map(lambda x: x**2)

# Create and populate numpy arrays with the rating number and variance. Variance for the ith rating is calculated as follows: 
# First look at the ith rating of a certain product and take the square of its difference from the final average product rating.
# Then, take the mean of all these squares over all products/
mean_diff = np.zeros(min_total_reviews)
review_num = np.arange(1, min_total_reviews + 1)
for i in range(min_total_reviews):
    nth_ratings = df4[df4["Rating Number"] == i+1]   
    mean_diff[i] = nth_ratings["Square of Average - Current Rating"].mean()

# Plot the data along with the line of best fit
slope, yintercept = np.polyfit(review_num, mean_diff, 1)
print(slope, yintercept)
plt.scatter(review_num, mean_diff)
plt.plot(review_num,  slope*review_num + yintercept, 'r-')
plt.title("Variance of Nth Rating")
plt.xlabel("Rating Number (N)")
plt.ylabel("Variance of Nth Rating")
plt.show()
#Compare datasets, review numbers, rating so far vs average product rating


# Analysis of Average Rating vs Total Reviews
"""

product_data_reviews_ratings = product_data(product_sorted_data)
#df.plot.scatter(x='Total Product Reviews',y='Average Product Rating')
#plt.show()
# Possibly Unnecessary
product_df = pd.DataFrame(product_data_reviews_ratings, columns = ('Total Reviews', 'Average Rating'))
averaged_ratings_product_data = []
for i in range(1, 500):
    rating_data = product_df[product_df['Total Reviews'] == i]
    averaged_ratings_product_data.append((i, rating_data["Average Rating"].mean()))


averaged_ratings_product_df = pd.DataFrame(averaged_ratings_product_data, columns=('Total Reviews', 'Average Rating'))
#averaged_ratings_product_df.plot.scatter(x='Total Reviews', y ='Average Rating')
averaged_ratings_product_df = averaged_ratings_product_df.dropna()
#print(averaged_ratings_product_df)
#plt.show()
product_average_ratings = averaged_ratings_product_df["Average Rating"].to_numpy()
product_number_of_ratings = averaged_ratings_product_df['Total Reviews'].to_numpy()

#linear_regression = sm.OLS(product_average_ratings,sm.add_constant(product_number_of_ratings)).fit()
#print(linear_regression.summary())
#sns.regplot(data = averaged_ratings_product_df, x='Total Reviews', y='Average Rating')
#plt.show()

m, b = np.polyfit(product_number_of_ratings, product_average_ratings, 1)
print(m, b)
plt.plot(product_number_of_ratings, product_average_ratings, 'bo')
plt.plot(product_number_of_ratings, m*product_number_of_ratings + b, 'r-')
plt.show()

#take averages here? i.e. for all products with 1 review, average rating and so on 
"""