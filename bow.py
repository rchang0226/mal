import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from IPython.display import display


def get_bow(data):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data)
    df_bow_sklearn = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
    df_bow_sklearn.head()
    return df_bow_sklearn
    # display(df_bow_sklearn)
