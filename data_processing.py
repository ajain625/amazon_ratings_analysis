from numpy.lib.type_check import nan_to_num
import pandas as pd
import seaborn as sns
import random
import matplotlib.pyplot as plt
import math
import numpy as np
import statsmodels.api as sm

def product_data(data):
    """Takes list of lists of lists where each element of the primary list is a list all ratings for a certain product. Each rating is a list of the form 
    [productid, rating, timestamp]. Returns a list of lists of the form [total_product_ratings, average_product_rating]"""

    product_data_reviews_ratings = []
    for i in range(len(data)):
        average_product_rating = 0
        total_product_ratings = len(data[i])
        for j in range(total_product_ratings):
            average_product_rating += data[i][j][1]
        average_product_rating = average_product_rating/total_product_ratings
        product_data_reviews_ratings.append([total_product_ratings, average_product_rating])
    return product_data_reviews_ratings

def sort_by_products(pandas_dataframe):
    """Takes in a Pandas dataframe of all ratings of the form userid-productid-rating-timestamp and returns a list of lists of lists. where each element of the primary list is a list all ratings for a certain product. Each rating is a list of the form 
    [productid, rating, timestamp]"""
    list_of_rows = [list(row) for row in pandas_dataframe.values]

    product_sorted_data = []
    product_list = []
    idPrev = list_of_rows[0][0]

    for i in range(len(list_of_rows)):
        idCurrent = list_of_rows[i][0]
        if idPrev == idCurrent:
            list_of_rows[i].pop(1)
            product_list.append(list_of_rows[i])        
        else:
            product_sorted_data.append(product_list)
            product_list = []
            list_of_rows[i].pop(1)
            product_list.append(list_of_rows[i])
            idPrev = idCurrent

    product_sorted_data.append(product_list)
    return product_sorted_data

def rating_data(data):
    """Takes list of lists of lists where each element of the primary list is a list all ratings for a certain product. Each rating is a list of the form 
    [productid, rating, timestamp]. Returns a list of lists of the form 
    [review_number, averageRating, rating, nextRating, final_average_rating, final_average_rating_rounded, timeSinceLast, timeToNext, totalReviews]"""

    all_data = []
    total_products = len(data)

    for i in range(total_products):
        totalReviews = len(data[i])
        #data[i].sort(key=lambda x: x[2])
        final_average_rating = 0

        for j in range(totalReviews):
            final_average_rating += data[i][j][1]
        
        final_average_rating = final_average_rating/totalReviews 
        final_average_rating_rounded = round(final_average_rating, 1)      

        for j in range(totalReviews):
            review_number = j+1
            rating = data[i][j][1]
            """
            if j == 0:
                averageRating = float(data[i][j][1])
                timeSinceLast = None
            else:
                averageRating = (averageRating * (j) + data[i][j][1])/(j+1)
                timeSinceLast = data[i][j][2] - data[i][j-1][2]
            
            if j == totalReviews-1:
                nextRating = None #or maybe averageRating?
                timeToNext = None
            else:
                nextRating = data[i][j+1][1]
                timeToNext = data[i][j+1][2] - data[i][j][2]
            """
            #dataPoint = [review_number, averageRating, rating, nextRating, final_average_rating, final_average_rating_rounded, timeSinceLast, timeToNext, totalReviews]
            dataPoint = [review_number,  rating, final_average_rating, final_average_rating_rounded,  totalReviews]
            all_data.append(dataPoint)
    return all_data

#Book 2: around 1 million, Book 1: around 100,000
rawData = pd.read_csv(r"C:\Users\Mona Jain.000\Downloads\Movies_and_TV.csv", delimiter=',')
#rawData = pd.read_csv(r"C:\Users\Mona Jain.000\Downloads\ratings_Clothing_Shoes_and_Jewelry(1).csv", delimiter=',')
print(rawData.head())
product_sorted_data = sort_by_products(rawData)



#allData = rating_data(product_sorted_data)
#df = pd.DataFrame(allData, columns = ('Review Number', 'Average Rating so far', 'Rating', 'Next Rating', 'Average Product Rating', 'Average Rounded Product Rating', 'Time Since Last Review', 'Time to Next Review', 'Total Product Reviews'))

# print(df.info())
#df1 = df.head(10000)
#print(df1.std())
#print(df1.mean())


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

# Analysis of mean of difference between rating and average rating vs review number
print(product_sorted_data[:2])
allData = rating_data(product_sorted_data)
df = pd.DataFrame(allData, columns = ('Review Number', 'Rating', 'Average Product Rating', 'Average Rounded Product Rating', 'Total Product Reviews'))
df4 = df[df["Total Product Reviews"] > 300]
print(df.shape)
print(df4.shape)
df4["Average - Current Rating"] = df4['Average Product Rating'] - df4['Rating']
df4["Abs of average - current rating"] = df4["Average - Current Rating"].map(lambda x: abs(x))
mean_diff= []
review_num = []
for i in range(1, 300):
    rating_data = df4[df4["Review Number"] == i]   
    mean_diff.append(rating_data["Abs of average - current rating"].mean())
    review_num.append(i)

mean_diff = np.asarray(mean_diff)
review_num = np.asarray(review_num)

m, b = np.polyfit(review_num, mean_diff, 1)
print(m, b)
plt.scatter(review_num, mean_diff)
plt.plot(review_num,  m*review_num + b, 'r-')
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
#print(df2.head)

#sns.scatterplot(data = df2, x = 'Rating', y = 'Total Product Reviews')
#plt.show()
#df1 = (df1 - df1.mean())/df1.std()
#print(df1.corr())
#sns.pairplot(df1)
#cmap = sns.diverging_palette(0, 255, as_cmap=True)
#sns.heatmap(df1.corr(), cmap=cmap)
#sns.scatterplot(data=df1, x='Time Since Last Review', y ='Time to Next Review')
#plt.show()

