import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
np.random.seed(314)

class LinearRegression:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        """Fit using closed-form solution: w = (X^T X)^-1 X^T y"""
        X, y = np.asarray(X, dtype=np.float64), np.asarray(y, dtype=np.float64)
        X_with_bias = np.c_[np.ones((X.shape[0], 1)), X]

        XtX = X_with_bias.T @ X_with_bias
        Xty = X_with_bias.T @ y
        params = np.linalg.solve(XtX + 1e-8 * np.eye(XtX.shape[0]), Xty)

        self.bias = params[0]
        self.weights = params[1:]

    def predict(self, X):
        """Make predictions"""
        return np.asarray(X, dtype=np.float64) @ self.weights + self.bias


def load_data():
    """Load training and test data"""
    train_df = pd.read_csv(r'C:\Users\tam\Documents\data\house\train.csv')
    test_df = pd.read_csv(r'C:\Users\tam\Documents\data\house\test.csv')
    return train_df, test_df


def remove_outliers(train_df):
    """Remove price and area outliers"""
    price_lower = train_df['SalePrice'].quantile(0.01)
    price_upper = train_df['SalePrice'].quantile(0.99)
    train_df = train_df[(train_df['SalePrice'] >= price_lower) & (train_df['SalePrice'] <= price_upper)]

    if 'GrLivArea' in train_df.columns:
        train_df = train_df[train_df['GrLivArea'] < 4000]

    return train_df


def preprocess_data(train_df, test_df):
    """Preprocess the data"""
    y_train = np.asarray(train_df['SalePrice'], dtype=np.float64)
    train_ids, test_ids = train_df['Id'].values, test_df['Id'].values

    X_train = train_df.drop(['Id', 'SalePrice'], axis=1)
    X_test = test_df.drop(['Id'], axis=1)
    all_data = pd.concat([X_train, X_test], ignore_index=True)

    numeric_cols = all_data.select_dtypes(include=[np.number]).columns
    categorical_cols = all_data.select_dtypes(include=['object']).columns

    all_data[numeric_cols] = all_data[numeric_cols].fillna(all_data[numeric_cols].median())
    all_data[categorical_cols] = all_data[categorical_cols].fillna('None')

    all_data_encoded = pd.get_dummies(all_data, columns=categorical_cols, drop_first=False)
    all_data_encoded = all_data_encoded.apply(pd.to_numeric, errors='coerce').fillna(0)

    X_train_encoded = all_data_encoded[:len(X_train)]
    X_test_encoded = all_data_encoded[len(X_train):]

    return X_train_encoded, X_test_encoded, y_train, train_ids, test_ids


def select_features(X_train_encoded, y_train, threshold=0.4):
    """Select features based on correlation with target"""
    train_with_target = X_train_encoded.copy()
    train_with_target['SalePrice'] = y_train
    train_with_target = train_with_target.apply(pd.to_numeric, errors='coerce').fillna(0)

    correlations = train_with_target.corr()['SalePrice'].drop('SalePrice')
    correlations_abs = correlations.abs().sort_values(ascending=False)
    selected_features = correlations_abs[correlations_abs > threshold].index.tolist()

    return selected_features, correlations


def scale_features(X_train, X_test, y_train):
    """Standardize features and target"""
    X_train = np.asarray(X_train, dtype=np.float64)
    X_test = np.asarray(X_test, dtype=np.float64)
    y_train = np.asarray(y_train, dtype=np.float64)

    X_mean, X_std = np.mean(X_train, axis=0), np.std(X_train, axis=0) + 1e-8
    X_train_scaled = (X_train - X_mean) / X_std
    X_test_scaled = (X_test - X_mean) / X_std

    y_mean, y_std = np.mean(y_train), np.std(y_train)
    y_train_scaled = (y_train - y_mean) / y_std

    return X_train_scaled, X_test_scaled, y_train_scaled, y_mean, y_std


def train_single_model(X_train_scaled, y_train_scaled, y_train, y_mean, y_std):
    """Train a single model"""
    model = LinearRegression(verbose=False)
    model.fit(X_train_scaled, y_train_scaled)

    y_pred_scaled = model.predict(X_train_scaled)
    y_pred = y_pred_scaled * y_std + y_mean
    rmse = np.sqrt(np.mean((np.asarray(y_train, dtype=np.float64) - y_pred) ** 2))

    return model, rmse


def train_ensemble_models(X_train_encoded, X_test_encoded, y_train, thresholds=[0.3, 0.35, 0.4, 0.45, 0.5]):
    """Train multiple models with different feature thresholds and ensemble predictions"""
    models_data = []

    for threshold in thresholds:
        selected_features, correlations = select_features(X_train_encoded, y_train, threshold)

        X_train_selected = np.asarray(X_train_encoded[selected_features], dtype=np.float64)
        X_test_selected = np.asarray(X_test_encoded[selected_features], dtype=np.float64)

        X_train_scaled, X_test_scaled, y_train_scaled, y_mean, y_std = scale_features(
            X_train_selected, X_test_selected, y_train
        )

        model, rmse = train_single_model(X_train_scaled, y_train_scaled, y_train, y_mean, y_std)

        models_data.append({
            'threshold': threshold,
            'model': model,
            'features': selected_features,
            'X_test_scaled': X_test_scaled,
            'y_mean': y_mean,
            'y_std': y_std,
            'rmse': rmse,
            'n_features': len(selected_features)
        })

    return models_data


def ensemble_predict(models_data):
    """Make ensemble predictions by averaging"""
    all_predictions = []

    for data in models_data:
        y_test_pred_scaled = data['model'].predict(data['X_test_scaled'])
        y_test_pred = y_test_pred_scaled * data['y_std'] + data['y_mean']
        all_predictions.append(y_test_pred)

    ensemble_pred = np.mean(all_predictions, axis=0)
    ensemble_pred = np.maximum(ensemble_pred, 0)

    return ensemble_pred


def visualize_ensemble_performance(models_data):
    """Visualize model performance across thresholds"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    thresholds = [d['threshold'] for d in models_data]
    rmses = [d['rmse'] for d in models_data]
    n_features = [d['n_features'] for d in models_data]

    axes[0].plot(thresholds, rmses, 'o-', linewidth=2, markersize=8, color='blue')
    axes[0].set_xlabel('Correlation Threshold')
    axes[0].set_ylabel('RMSE ($)')
    axes[0].set_title('Model Performance vs Threshold', fontweight='bold')
    axes[0].grid(alpha=0.3)

    axes[1].plot(thresholds, n_features, 'o-', linewidth=2, markersize=8, color='green')
    axes[1].set_xlabel('Correlation Threshold')
    axes[1].set_ylabel('Number of Features')
    axes[1].set_title('Feature Count vs Threshold', fontweight='bold')
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('ensemble_performance.png', dpi=300)
    plt.close()


def generate_submission(ensemble_pred, test_ids):
    """Generate predictions and create submission file"""
    submission = pd.DataFrame({'Id': test_ids, 'SalePrice': ensemble_pred})
    submission.to_csv('submission.csv', index=False)
    return submission


def analyze_best_model(models_data):
    """Analyze feature importance from best model"""
    best_model_data = min(models_data, key=lambda x: x['rmse'])

    weights = np.asarray(best_model_data['model'].weights, dtype=np.float64)
    feature_importance = pd.DataFrame({
        'Feature': best_model_data['features'],
        'Weight': weights,
        'Abs_Weight': np.abs(weights)
    }).sort_values('Abs_Weight', ascending=False)

    top_15 = feature_importance.head(15)
    colors = ['green' if w > 0 else 'red' for w in top_15['Weight']]

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(top_15)), top_15['Weight'], color=colors, alpha=0.7)
    plt.yticks(range(len(top_15)), top_15['Feature'], fontsize=9)
    plt.xlabel('Weight Value')
    plt.title(f'Top 15 Feature Weights (threshold={best_model_data["threshold"]})', fontweight='bold')
    plt.grid(alpha=0.3, axis='x')
    plt.axvline(0, color='black', linewidth=0.5)
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300)
    plt.close()


def main():
    """Main execution function with ensemble learning"""
    try:
        train_df, test_df = load_data()
        train_df = remove_outliers(train_df)
        X_train_encoded, X_test_encoded, y_train, train_ids, test_ids = preprocess_data(train_df, test_df)

        models_data = train_ensemble_models(
            X_train_encoded, X_test_encoded, y_train,
            thresholds=[0.3, 0.35, 0.4, 0.45, 0.5]
        )

        ensemble_pred = ensemble_predict(models_data)
        visualize_ensemble_performance(models_data)
        generate_submission(ensemble_pred, test_ids)
        analyze_best_model(models_data)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()