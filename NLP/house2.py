import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
np.random.seed(314)

class LinearRegression:
    def __init__(self, alpha=0.01):
        self.weights = None
        self.bias = None
        self.alpha = alpha

    def fit(self, X, y):
        X, y = np.asarray(X, dtype=np.float64), np.asarray(y, dtype=np.float64)
        X_with_bias = np.c_[np.ones((X.shape[0], 1)), X]
        XtX = X_with_bias.T @ X_with_bias
        Xty = X_with_bias.T @ y
        reg_matrix = self.alpha * np.eye(XtX.shape[0])
        reg_matrix[0, 0] = 0
        params = np.linalg.solve(XtX + reg_matrix, Xty)
        self.bias = params[0]
        self.weights = params[1:]

    def predict(self, X):
        return np.asarray(X, dtype=np.float64) @ self.weights + self.bias


def load_data():
    train_df = pd.read_csv(r'C:\Users\tam\Documents\data\house\train.csv')
    test_df = pd.read_csv(r'C:\Users\tam\Documents\data\house\test.csv')
    return train_df, test_df


def remove_outliers(train_df):
    price_lower = train_df['SalePrice'].quantile(0.005)
    price_upper = train_df['SalePrice'].quantile(0.995)
    train_df = train_df[(train_df['SalePrice'] >= price_lower) & 
                       (train_df['SalePrice'] <= price_upper)]
    if 'GrLivArea' in train_df.columns:
        train_df = train_df[train_df['GrLivArea'] < 4000]
    return train_df


def create_polynomial_features(X, degree=2, interaction_only=False):
    X = np.asarray(X, dtype=np.float64)
    n_samples, n_features = X.shape
    if interaction_only:
        features = [X]
        for i in range(n_features):
            for j in range(i+1, n_features):
                features.append((X[:, i] * X[:, j]).reshape(-1, 1))
        return np.hstack(features)
    else:
        features = [X]
        if degree >= 2:
            n_poly = min(10, n_features)
            features.append(X[:, :n_poly] ** 2)
        return np.hstack(features)


def preprocess_data(train_df, test_df):
    y_train = np.asarray(train_df['SalePrice'], dtype=np.float64)
    train_ids, test_ids = train_df['Id'].values, test_df['Id'].values
    X_train = train_df.drop(['Id', 'SalePrice'], axis=1)
    X_test = test_df.drop(['Id'], axis=1)
    all_data = pd.concat([X_train, X_test], ignore_index=True)

    if 'YearBuilt' in all_data.columns and 'YrSold' in all_data.columns:
        all_data['HouseAge'] = all_data['YrSold'] - all_data['YearBuilt']
        all_data['HouseAge'] = all_data['HouseAge'].clip(lower=0)
    if 'YearRemodAdd' in all_data.columns and 'YrSold' in all_data.columns:
        all_data['RemodAge'] = all_data['YrSold'] - all_data['YearRemodAdd']
        all_data['RemodAge'] = all_data['RemodAge'].clip(lower=0)
    if 'TotalBsmtSF' in all_data.columns and '1stFlrSF' in all_data.columns and '2ndFlrSF' in all_data.columns:
        all_data['TotalSF'] = all_data['TotalBsmtSF'] + all_data['1stFlrSF'] + all_data['2ndFlrSF']
    if 'GrLivArea' in all_data.columns and 'TotRmsAbvGrd' in all_data.columns:
        all_data['AvgRoomSize'] = all_data['GrLivArea'] / (all_data['TotRmsAbvGrd'] + 1)
    if 'GarageArea' in all_data.columns and 'GarageCars' in all_data.columns:
        all_data['GaragePerCar'] = all_data['GarageArea'] / (all_data['GarageCars'] + 1)

    numeric_cols = all_data.select_dtypes(include=[np.number]).columns
    categorical_cols = all_data.select_dtypes(include=['object']).columns
    all_data[numeric_cols] = all_data[numeric_cols].fillna(all_data[numeric_cols].median())
    all_data[categorical_cols] = all_data[categorical_cols].fillna('None')
    all_data_encoded = pd.get_dummies(all_data, columns=categorical_cols, drop_first=True)
    all_data_encoded = all_data_encoded.apply(pd.to_numeric, errors='coerce').fillna(0)
    X_train_encoded = all_data_encoded[:len(X_train)]
    X_test_encoded = all_data_encoded[len(X_train):]
    return X_train_encoded, X_test_encoded, y_train, train_ids, test_ids


def select_features(X_train_encoded, y_train, threshold=0.3, max_features=None):
    train_with_target = X_train_encoded.copy()
    train_with_target['SalePrice'] = y_train
    train_with_target = train_with_target.apply(pd.to_numeric, errors='coerce').fillna(0)
    correlations = train_with_target.corr()['SalePrice'].drop('SalePrice')
    correlations_abs = correlations.abs().sort_values(ascending=False)
    selected_features = correlations_abs[correlations_abs > threshold].index.tolist()
    if max_features and len(selected_features) > max_features:
        selected_features = selected_features[:max_features]
    return selected_features, correlations


def scale_features(X_train, X_test, y_train, log_transform_y=True):
    X_train = np.asarray(X_train, dtype=np.float64)
    X_test = np.asarray(X_test, dtype=np.float64)
    y_train = np.asarray(y_train, dtype=np.float64)
    X_mean, X_std = np.mean(X_train, axis=0), np.std(X_train, axis=0) + 1e-8
    X_train_scaled = (X_train - X_mean) / X_std
    X_test_scaled = (X_test - X_mean) / X_std
    if log_transform_y:
        y_train_transformed = np.log1p(y_train)
        y_mean, y_std = np.mean(y_train_transformed), np.std(y_train_transformed)
        y_train_scaled = (y_train_transformed - y_mean) / y_std
        return X_train_scaled, X_test_scaled, y_train_scaled, y_mean, y_std, True
    else:
        y_mean, y_std = np.mean(y_train), np.std(y_train)
        y_train_scaled = (y_train - y_mean) / y_std
        return X_train_scaled, X_test_scaled, y_train_scaled, y_mean, y_std, False


def train_single_model(X_train_scaled, y_train_scaled, y_train, y_mean, y_std, log_transformed, alpha=0.5):
    model = LinearRegression(alpha=alpha)
    model.fit(X_train_scaled, y_train_scaled)
    y_pred_scaled = model.predict(X_train_scaled)
    y_pred_transformed = y_pred_scaled * y_std + y_mean
    if log_transformed:
        y_pred = np.expm1(y_pred_transformed)
    else:
        y_pred = y_pred_transformed
    rmse = np.sqrt(np.mean((np.asarray(y_train, dtype=np.float64) - y_pred) ** 2))
    return model, rmse


def train_ensemble_models(X_train_encoded, X_test_encoded, y_train, 
                         thresholds=[0.25, 0.3, 0.35, 0.4],
                         alphas=[0.1, 0.5, 1.0, 2.0],
                         use_log=[True, False],
                         use_poly=[False, True]):
    models_data = []
    for threshold in thresholds:
        for alpha in alphas:
            for log_transform in use_log:
                for polynomial in use_poly:
                    selected_features, correlations = select_features(X_train_encoded, y_train, threshold, max_features=100)
                    X_train_selected = np.asarray(X_train_encoded[selected_features], dtype=np.float64)
                    X_test_selected = np.asarray(X_test_encoded[selected_features], dtype=np.float64)
                    if polynomial and len(selected_features) <= 30:
                        X_train_selected = create_polynomial_features(X_train_selected, degree=2, interaction_only=False)
                        X_test_selected = create_polynomial_features(X_test_selected, degree=2, interaction_only=False)
                    X_train_scaled, X_test_scaled, y_train_scaled, y_mean, y_std, is_log = scale_features(
                        X_train_selected, X_test_selected, y_train, log_transform_y=log_transform)
                    model, rmse = train_single_model(X_train_scaled, y_train_scaled, y_train, y_mean, y_std, is_log, alpha)
                    models_data.append({
                        'model': model, 'X_test_scaled': X_test_scaled,
                        'y_mean': y_mean, 'y_std': y_std,
                        'log_transformed': is_log, 'rmse': rmse
                    })
    return models_data


def ensemble_predict(models_data, top_k=10):
    sorted_models = sorted(models_data, key=lambda x: x['rmse'])[:top_k]
    all_predictions = []
    weights = []
    for data in sorted_models:
        y_test_pred_scaled = data['model'].predict(data['X_test_scaled'])
        y_test_pred_transformed = y_test_pred_scaled * data['y_std'] + data['y_mean']
        if data['log_transformed']:
            y_test_pred = np.expm1(y_test_pred_transformed)
        else:
            y_test_pred = y_test_pred_transformed
        all_predictions.append(y_test_pred)
        weights.append(1.0 / (data['rmse'] + 1e-6))
    all_predictions = np.array(all_predictions)
    weights = np.array(weights)
    weights = weights / weights.sum()
    ensemble_pred = np.average(all_predictions, axis=0, weights=weights)
    ensemble_pred = np.maximum(ensemble_pred, 0)
    return ensemble_pred


def generate_submission(ensemble_pred, test_ids):
    submission = pd.DataFrame({'Id': test_ids, 'SalePrice': ensemble_pred})
    submission.to_csv('submission.csv', index=False)
    return submission


def main():
    train_df, test_df = load_data()
    train_df = remove_outliers(train_df)
    X_train_encoded, X_test_encoded, y_train, train_ids, test_ids = preprocess_data(train_df, test_df)
    models_data = train_ensemble_models(X_train_encoded, X_test_encoded, y_train,
                                       thresholds=[0.25, 0.3, 0.35, 0.4],
                                       alphas=[0.1, 0.5, 1.0, 2.0],
                                       use_log=[True, False],
                                       use_poly=[False, True])
    ensemble_pred = ensemble_predict(models_data, top_k=15)
    generate_submission(ensemble_pred, test_ids)


if __name__ == '__main__':
    main()