# Future Ideas --- TO DO

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