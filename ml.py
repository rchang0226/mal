# Load libraries
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split, KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn import linear_model
from sklearn import svm


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
