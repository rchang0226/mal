from matplotlib import pyplot
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import mal
import bow
from pandas import read_csv
from IPython.display import display
import ml


def generate_my_data():
    # assumes list order is the same for both
    return mal.get_anime_synopses('@me'), mal.get_anime_score_means('@me')


# Gets a random list of anime and returns a list of synopsis and a list of means
def generate_random_data():
    anime_list = mal.get_random_anime_list(100, 0, 10000)
    return mal.get_value_from_anime_list(anime_list, 'synopsis'), mal.get_value_from_anime_list(anime_list, 'mean')


def save_bow_rep(synopses, scores, name):
    # turn the sentences into bag of word vector representations
    df = bow.get_bow(synopses)

    # add corresponding scores to the dataframe (assumes list order is the same)
    df['scores'] = scores

    # save to a csv
    df.to_csv(name)


if __name__ == '__main__':
    """synopses, scores = generate_random_data()
    save_bow_rep(synopses, scores, 'random_list_100.csv')"""


    """# read the csv
    df = read_csv('my_list.csv')

    # need to remove the first column for some reason, has to do with how I saved the csv I think
    df = df.drop(df.columns[[0]], axis=1)

    # split the dataset
    x_train, x_validation, y_train, y_validation = ml.create_validation_dataset(df)

  # compare different algorithms
    ml.compare_models(x_train, y_train)

    # From the results, ['SGD: -4.982397 (3.225995)', 'BR: -0.225578 (0.147847)', 'LL: -0.187104 (0.117122)',
    # 'ARD: -0.356156 (0.273288)', 'PA: -5.262207 (3.244099)', 'SVM: -5.277980 (3.277356)', 'Linear: -0.226402 (
    # 0.149438)', 'SVR: -0.172713 (0.111821)'],
    # it seems that SVR was the best.
    # The worst were SGD, PA, and SVM.

    # make prediction on validation dataset
    model = svm.SVR()
    model.fit(x_train, y_train)
    predictions = model.predict(x_validation)

    # evaluate predictions
    print(r2_score(y_validation, predictions))
    print(mean_squared_error(y_validation, predictions))"""
