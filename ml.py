# Load libraries
from pandas import read_csv
from matplotlib import pyplot
from sklearn.model_selection import train_test_split, KFold
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
from sklearn import svm
import mal
import time
import bow
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# takes in a panda dataframe as input
def create_validation_dataset(dataset):
    array = dataset.values
    y_shape = array.shape[1] - 1

    # assumes the last column is the label
    x = array[:, 0:y_shape]
    y = array[:, y_shape]

    x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=0.20, random_state=1)
    return x_train, x_validation, y_train, y_validation


# For regression (not classifier)
def compare_models(x_train, y_train):
    models = []
    models.append(('SGD', linear_model.SGDRegressor()))
    models.append(('BR', linear_model.BayesianRidge()))
    models.append(('LL', linear_model.LassoLars()))
    models.append(('ARD', linear_model.ARDRegression()))
    models.append(('PA', linear_model.PassiveAggressiveRegressor()))
    models.append(('SVM', linear_model.TheilSenRegressor()))
    models.append(('Linear', linear_model.LinearRegression()))
    models.append(('SVR', svm.SVR()))

    results = []
    names = []
    for name, model in models:
        kfold = KFold(n_splits=10, random_state=1, shuffle=True)
        cv_results = cross_val_score(model, x_train, y_train, cv=kfold, scoring='neg_mean_squared_error')
        results.append(cv_results)
        names.append(name)
        print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
    pyplot.boxplot(results, labels=names)
    pyplot.title('Algorithm Comparison')
    pyplot.show()


def generate_my_data():
    # assumes list order is the same for both
    return mal.get_anime_synopses('@me'), mal.get_anime_score_means('@me')


# Gets a random list of anime and returns a list of synopsis and a list of means
def generate_random_data():
    random_numbers = mal.get_random_numbers(1200, 0, 10000)
    chunks = [random_numbers[x:x + 100] for x in range(0, len(random_numbers), 100)]
    anime_list = []
    for num, chunk in enumerate(chunks):
        primitive_obj_list = [mal.get_anime_by_rank(num) for num in chunk]
        id_list = [x['id'] for x in primitive_obj_list]
        obj_list = mal.get_anime_objects(id_list)
        anime_list.extend(obj_list)
        print(f"batch #{num} done")
        time.sleep(180)

    return mal.get_value_from_anime_list(anime_list, 'synopsis'), mal.get_value_from_anime_list(anime_list, 'mean')


def save_bow_rep(synopses, scores, name):
    # turn the sentences into bag of word vector representations
    df = bow.get_bow(synopses)

    # add corresponding scores to the dataframe (assumes list order is the same)
    df['scores'] = scores

    # save to a csv
    df.to_csv(name)


def create_data():
    synopses, scores = generate_random_data()
    save_bow_rep(synopses, scores, 'random_list_1200.csv')


def train_and_predict():
    # read the csv
    df = read_csv('random_list_1200.csv')

    # need to remove the first column for some reason, has to do with how I saved the csv I think
    df = df.drop(df.columns[[0]], axis=1)

    # split the dataset
    x_train, x_validation, y_train, y_validation = create_validation_dataset(df)

    """# compare different algorithms
    ml.compare_models(x_train, y_train)"""

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
    print(mean_squared_error(y_validation, predictions))
