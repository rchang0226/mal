import mal
import bow
from pandas import read_csv
from IPython.display import display

import ml


def save_bow_rep():
    # get the anime synopses
    data = mal.get_anime_synopses('@me')
    # turn the sentences into bag of word vector representations
    df = bow.get_bow(data)

    # get corresponding scores for each anime (assumes list order is the same)
    scores = mal.get_anime_score_means('@me')

    # add scores to the dataframe
    df['scores'] = scores

    df.to_csv('my_list.csv')


if __name__ == '__main__':
    # read the csv
    df = read_csv('my_list.csv')

    # need to remove the first column for some reason, has to do with how I saved the csv I think
    df = df.drop(df.columns[[0]], axis=1)

    # split the dataset
    x_train, x_validation, y_train, y_validation = ml.create_validation_dataset(df)

    # compare different algorithms
    result = ml.build_models(x_train, y_train)
    print(result)

    # From the results, ['SGD: -4.982397 (3.225995)', 'BR: -0.225578 (0.147847)', 'LL: -0.187104 (0.117122)',
    # 'ARD: -0.356156 (0.273288)', 'PA: -5.262207 (3.244099)', 'SVM: -5.277980 (3.277356)', 'Linear: -0.226402 (
    # 0.149438)', 'SVR: -0.172713 (0.111821)'],
    # it seems that SVR was the best.
    # The worst were SGD, PA, and SVM.





