import pandas as pd
import numpy as np

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

def rating_data(data, time_analysis = False):
    """Takes list of lists of lists where each element of the primary list is a list all ratings for one single product. Each rating is a list of the form 
    [productid, rating, timestamp]. Returns a pandas dataframe with columns: 
    ['Review Number', 'Average Rating so far', 'Rating', 'Next Rating', 'Average Product Rating', 'Average Rounded Product Rating', 'Time Since Last Review', 'Time to Next Review', 'Total Product Reviews']
    if time_analysis = True. Else, returns pandas dataframe with columns:
    ['Review Number', 'Rating', 'Average Product Rating', 'Average Rounded Product Rating', 'Total Product Reviews']"""

    all_data = []
    total_products = len(data)

    for i in range(total_products):
        total_ratings = len(data[i])
        final_average_rating = 0

        for j in range(total_ratings):
            final_average_rating += data[i][j][1]
        
        final_average_rating = final_average_rating/total_ratings
        final_average_rating_rounded = round(final_average_rating, 1)

        if time_analysis:
            data[i].sort(key=lambda x: x[2])
            for j in range(total_ratings):            
                rating_number = j+1
                rating = data[i][j][1]
                if j == 0:
                    averageRating = float(data[i][j][1])
                    timeSinceLast = None
                else:
                    averageRating = (averageRating * (j) + data[i][j][1])/(j+1)
                    timeSinceLast = data[i][j][2] - data[i][j-1][2]
                
                if j == total_ratings-1:
                    nextRating = None #or maybe averageRating?
                    timeToNext = None
                else:
                    nextRating = data[i][j+1][1]
                    timeToNext = data[i][j+1][2] - data[i][j][2]
                dataPoint = [rating_number, averageRating, rating, nextRating, final_average_rating, final_average_rating_rounded, timeSinceLast, timeToNext, total_ratings]
                all_data.append(dataPoint)

        else:
            for j in range(total_ratings):
                rating_number = j+1
                rating = data[i][j][1]
                dataPoint = [rating_number, rating, final_average_rating, final_average_rating_rounded, total_ratings]
                all_data.append(dataPoint)

    if time_analysis:
        return pd.DataFrame(all_data, columns = ('Rating Number', 'Average Rating so far', 'Rating', 'Next Rating', 'Average Product Rating', 'Average Rounded Product Rating', 'Time Since Last Rating', 'Time to Next Rating', 'Total Product Ratings'))
    else:
        return pd.DataFrame(all_data, columns = ('Rating Number', 'Rating', 'Average Product Rating', 'Average Rounded Product Rating', 'Total Product Ratings'))





