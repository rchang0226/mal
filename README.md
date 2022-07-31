# Description
NLP methods are applied to a variety of data from anime cataloging sites such as MyAnimeList(MAL) and AniList. Mostly, I wanted to experiment around with the bag of words representation and sentiment analysis, and I figured it would be more interesting to try them on datasets that are meaningful to myself.

## Data collection
mal.py has a variety of functions for grabbing data from the official MAL API, such as getting mean anime scores, synopses, and more. anilist.py serves a similar purpose, but for grabbing data from the AniList API instead. 

## Bag of words
Originally, I was interested to know if there was a correlation between the way anime synopses were written and the mean score of that anime. I decided to practice using the bag of words model to represent each anime synopsis. ml.py compares a variety of linear regression models as well as a support vector machine, using 10-fold cross validation on the metric of mean squared error. Epsilon-Support Vector Regression had relatively the lowest error, so it was used to make a prediction on the validation dataset. Unfortunately, the R2 was very low at around 0.15, which either means there was no correlation to begin with, or the model is flawed, or both. In case it was due to a lack of data, I tried running it on a thousand anime, rather than the hundred I had ran it on before, but without filtering for the vocabulary size, the BoW representation became much too sparse, as the mean squared errors were beginning to give 0's. 

## Sentiment analysis
Next, I looked towards performing sentiment analysis on anime reviews by users of the sites. I used a model trained previously on movie review sentiments (see https://github.com/rchang0226/nlp). main.py tests this model on anime reviews pulled from AniList. According to the original training dataset, in a 5-star system, 3.5 and above were labeled as positive, and 2 and below were labeled as negative. AniList uses a 100-point system, so I scaled it accordingly, such that 70 and above is positive, and 40 and below is negative. 

The model had an accuracy of 84% on the anime review set, which is very close to the original 85% the model had on its original validation test set, so it seems to have performed well in this new context. 

I later realized that significantly more positive reviews than negative ones were pulled from AniList, so in order to ensure that this accuracy wasn't being artificially inflated by the number of positive reviews, I tested the model on only the negative reviews, getting an accuracy of around 75%, which is still on the high end, although there does appear to be a slight positive bias. 

Next, I plan to train a model that tries to predict mean scores based on the script of the anime. 
