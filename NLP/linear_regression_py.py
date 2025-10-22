import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
np.random.seed(314)

class LinearRegression:
    def __init__(self, alpha=0.01, verbose=True):
        self.verbose = verbose
        self.weights = None
        self.bias = None
        self.alpha = alpha  # Regularization parameter

    def fit(self, X, y, regularization='ridge'):
        """Fit using closed-form solution with regularization
        
        Ridge: w = (X^T X + αI)^-1 X^T y
        """
        X, y = np.asarray(X, dtype=np.float64), np.asarray(y, dtype=np.float64)
        X_with_bias = np.c_[np.ones((X.shape[0], 1)), X]

        XtX = X_with_bias.T @ X_with_bias
        Xty = X_with_bias.T @ y
        
        # Add regularization (Ridge regression)
        reg_matrix = self.alpha * np.eye(XtX.shape[0])
        reg_matrix[0, 0] = 0  # Don't regularize bias term
        
        params = np.linalg.solve(XtX + reg_matrix, Xty)

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
    # More aggressive outlier removal
    price_lower = train_df['SalePrice'].quantile(0.005)
    price_upper = train_df['SalePrice'].quantile(0.995)
    train_df = train_df[(train_df['SalePrice'] >= price_lower) & 
                       (train_df['SalePrice'] <= price_upper)]

    if 'GrLivArea' in train_df.columns:
        # Remove extreme outliers in living area
        train_df = train_df[train_df['GrLivArea'] < 4000]
    
    return train_df


def create_polynomial_features(X, degree=2, interaction_only=False):
    """Create polynomial and interaction features"""
    X = np.asarray(X, dtype=np.float64)
    n_samples, n_features = X.shape
    
    if interaction_only:
        # Only create interaction terms (x1*x2, x1*x3, etc.)
        features = [X]
        for i in range(n_features):
            for j in range(i+1, n_features):
                features.append((X[:, i] * X[:, j]).reshape(-1, 1))
        return np.hstack(features)
    else:
        # Create polynomial features up to degree
        features = [X]
        if degree >= 2:
            # Add squared terms for most important features (first 10)
            n_poly = min(10, n_features)
            features.append(X[:, :n_poly] ** 2)
        return np.hstack(features)


def preprocess_data(train_df, test_df):
    """Enhanced preprocessing with feature engineering"""
    y_train = np.asarray(train_df['SalePrice'], dtype=np.float64)
    train_ids, test_ids = train_df['Id'].values, test_df['Id'].values

    X_train = train_df.drop(['Id', 'SalePrice'], axis=1)
    X_test = test_df.drop(['Id'], axis=1)
    all_data = pd.concat([X_train, X_test], ignore_index=True)

    # Feature Engineering: Create new features
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

    # Separate numeric and categorical
    numeric_cols = all_data.select_dtypes(include=[np.number]).columns
    categorical_cols = all_data.select_dtypes(include=['object']).columns

    # Fill missing values
    all_data[numeric_cols] = all_data[numeric_cols].fillna(all_data[numeric_cols].median())
    all_data[categorical_cols] = all_data[categorical_cols].fillna('None')

    # Encode categorical variables
    all_data_encoded = pd.get_dummies(all_data, columns=categorical_cols, drop_first=True)
    all_data_encoded = all_data_encoded.apply(pd.to_numeric, errors='coerce').fillna(0)

    X_train_encoded = all_data_encoded[:len(X_train)]
    X_test_encoded = all_data_encoded[len(X_train):]

    return X_train_encoded, X_test_encoded, y_train, train_ids, test_ids


def select_features(X_train_encoded, y_train, threshold=0.3, max_features=None):
    """Enhanced feature selection with multiple criteria"""
    train_with_target = X_train_encoded.copy()
    train_with_target['SalePrice'] = y_train
    train_with_target = train_with_target.apply(pd.to_numeric, errors='coerce').fillna(0)

    correlations = train_with_target.corr()['SalePrice'].drop('SalePrice')
    correlations_abs = correlations.abs().sort_values(ascending=False)
    
    # Select features above threshold
    selected_features = correlations_abs[correlations_abs > threshold].index.tolist()
    
    # Limit to max_features if specified
    if max_features and len(selected_features) > max_features:
        selected_features = selected_features[:max_features]

    return selected_features, correlations


def scale_features(X_train, X_test, y_train, log_transform_y=True):
    """Standardize features and optionally log-transform target"""
    X_train = np.asarray(X_train, dtype=np.float64)
    X_test = np.asarray(X_test, dtype=np.float64)
    y_train = np.asarray(y_train, dtype=np.float64)

    # Standardize X
    X_mean, X_std = np.mean(X_train, axis=0), np.std(X_train, axis=0) + 1e-8
    X_train_scaled = (X_train - X_mean) / X_std
    X_test_scaled = (X_test - X_mean) / X_std

    # Transform y (log transformation often helps with prices)
    if log_transform_y:
        y_train_transformed = np.log1p(y_train)  # log(1 + y) to handle zeros
        y_mean, y_std = np.mean(y_train_transformed), np.std(y_train_transformed)
        y_train_scaled = (y_train_transformed - y_mean) / y_std
        return X_train_scaled, X_test_scaled, y_train_scaled, y_mean, y_std, True
    else:
        y_mean, y_std = np.mean(y_train), np.std(y_train)
        y_train_scaled = (y_train - y_mean) / y_std
        return X_train_scaled, X_test_scaled, y_train_scaled, y_mean, y_std, False


def train_single_model(X_train_scaled, y_train_scaled, y_train, y_mean, y_std, 
                       log_transformed, alpha=0.5):
    """Train a single model with regularization"""
    model = LinearRegression(alpha=alpha, verbose=False)
    model.fit(X_train_scaled, y_train_scaled, regularization='ridge')

    y_pred_scaled = model.predict(X_train_scaled)
    y_pred_transformed = y_pred_scaled * y_std + y_mean
    
    # Inverse transform if log was used
    if log_transformed:
        y_pred = np.expm1(y_pred_transformed)  # exp(y) - 1
    else:
        y_pred = y_pred_transformed
    
    rmse = np.sqrt(np.mean((np.asarray(y_train, dtype=np.float64) - y_pred) ** 2))

    return model, rmse


def train_ensemble_models(X_train_encoded, X_test_encoded, y_train, 
                         thresholds=[0.25, 0.3, 0.35, 0.4],
                         alphas=[0.1, 0.5, 1.0, 2.0],
                         use_log=[True, False],
                         use_poly=[False, True]):
    """Train multiple models with different hyperparameters"""
    models_data = []

    for threshold in thresholds:
        for alpha in alphas:
            for log_transform in use_log:
                for polynomial in use_poly:
                    selected_features, correlations = select_features(
                        X_train_encoded, y_train, threshold, max_features=100
                    )

                    X_train_selected = np.asarray(X_train_encoded[selected_features], dtype=np.float64)
                    X_test_selected = np.asarray(X_test_encoded[selected_features], dtype=np.float64)

                    # Add polynomial features if specified
                    if polynomial and len(selected_features) <= 30:  # Only for smaller feature sets
                        X_train_selected = create_polynomial_features(X_train_selected, degree=2, interaction_only=False)
                        X_test_selected = create_polynomial_features(X_test_selected, degree=2, interaction_only=False)

                    X_train_scaled, X_test_scaled, y_train_scaled, y_mean, y_std, is_log = scale_features(
                        X_train_selected, X_test_selected, y_train, log_transform_y=log_transform
                    )

                    model, rmse = train_single_model(
                        X_train_scaled, y_train_scaled, y_train, y_mean, y_std, is_log, alpha
                    )

                    models_data.append({
                        'threshold': threshold,
                        'alpha': alpha,
                        'log_transform': log_transform,
                        'polynomial': polynomial,
                        'model': model,
                        'features': selected_features,
                        'X_test_scaled': X_test_scaled,
                        'y_mean': y_mean,
                        'y_std': y_std,
                        'log_transformed': is_log,
                        'rmse': rmse,
                        'n_features': X_train_scaled.shape[1]
                    })

    return models_data


def ensemble_predict(models_data, method='weighted_average', top_k=10):
    """Make ensemble predictions with weighted averaging"""
    # Sort models by RMSE and select top k
    sorted_models = sorted(models_data, key=lambda x: x['rmse'])[:top_k]
    
    all_predictions = []
    weights = []

    for data in sorted_models:
        y_test_pred_scaled = data['model'].predict(data['X_test_scaled'])
        y_test_pred_transformed = y_test_pred_scaled * data['y_std'] + data['y_mean']
        
        # Inverse transform if log was used
        if data['log_transformed']:
            y_test_pred = np.expm1(y_test_pred_transformed)
        else:
            y_test_pred = y_test_pred_transformed
        
        all_predictions.append(y_test_pred)
        
        # Weight inversely proportional to RMSE
        weights.append(1.0 / (data['rmse'] + 1e-6))

    all_predictions = np.array(all_predictions)
    weights = np.array(weights)
    weights = weights / weights.sum()  # Normalize

    if method == 'weighted_average':
        ensemble_pred = np.average(all_predictions, axis=0, weights=weights)
    else:  # simple average
        ensemble_pred = np.mean(all_predictions, axis=0)
    
    ensemble_pred = np.maximum(ensemble_pred, 0)

    return ensemble_pred


def visualize_ensemble_performance(models_data):
    """Visualize model performance"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Sort by RMSE
    sorted_models = sorted(models_data, key=lambda x: x['rmse'])
    
    # Top 20 models
    top_20 = sorted_models[:20]
    rmses = [d['rmse'] for d in top_20]
    labels = [f"T{d['threshold']}_A{d['alpha']}_L{int(d['log_transform'])}_P{int(d['polynomial'])}" 
              for d in top_20]

    axes[0, 0].barh(range(len(top_20)), rmses, color='steelblue', alpha=0.7)
    axes[0, 0].set_yticks(range(len(top_20)))
    axes[0, 0].set_yticklabels(labels, fontsize=7)
    axes[0, 0].set_xlabel('RMSE ($)')
    axes[0, 0].set_title('Top 20 Models by RMSE', fontweight='bold')
    axes[0, 0].grid(alpha=0.3, axis='x')
    axes[0, 0].invert_yaxis()

    # RMSE vs Alpha for different thresholds
    thresholds = sorted(set(d['threshold'] for d in models_data))
    for threshold in thresholds[:3]:  # Plot top 3 thresholds
        subset = [d for d in models_data if d['threshold'] == threshold]
        alphas = [d['alpha'] for d in subset]
        rmses = [d['rmse'] for d in subset]
        axes[0, 1].scatter(alphas, rmses, label=f'Threshold={threshold}', alpha=0.6, s=50)
    
    axes[0, 1].set_xlabel('Alpha (Regularization)')
    axes[0, 1].set_ylabel('RMSE ($)')
    axes[0, 1].set_title('RMSE vs Regularization', fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)

    # Feature count distribution
    n_features = [d['n_features'] for d in models_data]
    axes[1, 0].hist(n_features, bins=20, color='green', alpha=0.7, edgecolor='black')
    axes[1, 0].set_xlabel('Number of Features')
    axes[1, 0].set_ylabel('Count')
    axes[1, 0].set_title('Feature Count Distribution', fontweight='bold')
    axes[1, 0].grid(alpha=0.3)

    # RMSE distribution
    all_rmses = [d['rmse'] for d in models_data]
    axes[1, 1].hist(all_rmses, bins=30, color='purple', alpha=0.7, edgecolor='black')
    axes[1, 1].set_xlabel('RMSE ($)')
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].set_title('RMSE Distribution', fontweight='bold')
    axes[1, 1].axvline(np.mean(all_rmses), color='red', linestyle='--', 
                       label=f'Mean: ${np.mean(all_rmses):.0f}')
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('ensemble_performance.png', dpi=300)
    plt.close()

    print(f"\n{'='*60}")
    print(f"ENSEMBLE PERFORMANCE SUMMARY")
    print(f"{'='*60}")
    print(f"Total models trained: {len(models_data)}")
    print(f"Best RMSE: ${sorted_models[0]['rmse']:.2f}")
    print(f"Worst RMSE: ${sorted_models[-1]['rmse']:.2f}")
    print(f"Mean RMSE: ${np.mean(all_rmses):.2f}")
    print(f"Std RMSE: ${np.std(all_rmses):.2f}")
    print(f"\nBest Model Configuration:")
    print(f"  - Threshold: {sorted_models[0]['threshold']}")
    print(f"  - Alpha: {sorted_models[0]['alpha']}")
    print(f"  - Log Transform: {sorted_models[0]['log_transform']}")
    print(f"  - Polynomial: {sorted_models[0]['polynomial']}")
    print(f"  - Features: {sorted_models[0]['n_features']}")
    print(f"{'='*60}\n")


def generate_submission(ensemble_pred, test_ids):
    """Generate predictions and create submission file"""
    submission = pd.DataFrame({'Id': test_ids, 'SalePrice': ensemble_pred})
    submission.to_csv('submission.csv', index=False)
    print(f"Submission saved to 'submission.csv'")
    print(f"Prediction stats:")
    print(f"  - Min: ${ensemble_pred.min():.2f}")
    print(f"  - Max: ${ensemble_pred.max():.2f}")
    print(f"  - Mean: ${ensemble_pred.mean():.2f}")
    print(f"  - Median: ${np.median(ensemble_pred):.2f}")
    return submission


def analyze_best_model(models_data):
    """Analyze feature importance from best model"""
    best_model_data = min(models_data, key=lambda x: x['rmse'])

    weights = np.asarray(best_model_data['model'].weights, dtype=np.float64)
    
    # For polynomial features, only use original feature names
    n_original = len(best_model_data['features'])
    if len(weights) > n_original:
        weights = weights[:n_original]
    
    feature_importance = pd.DataFrame({
        'Feature': best_model_data['features'][:len(weights)],
        'Weight': weights,
        'Abs_Weight': np.abs(weights)
    }).sort_values('Abs_Weight', ascending=False)

    top_20 = feature_importance.head(20)
    colors = ['green' if w > 0 else 'red' for w in top_20['Weight']]

    plt.figure(figsize=(12, 8))
    plt.barh(range(len(top_20)), top_20['Weight'], color=colors, alpha=0.7)
    plt.yticks(range(len(top_20)), top_20['Feature'], fontsize=9)
    plt.xlabel('Weight Value (Standardized)', fontweight='bold')
    plt.title(f'Top 20 Feature Weights - Best Model (RMSE: ${best_model_data["rmse"]:.2f})', 
              fontweight='bold', fontsize=12)
    plt.grid(alpha=0.3, axis='x')
    plt.axvline(0, color='black', linewidth=1)
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300)
    plt.close()

    print(f"\nTop 10 Most Important Features:")
    for i, row in enumerate(top_20.head(10).itertuples(), 1):
        print(f"{i:2d}. {row.Feature:30s} | Weight: {row.Weight:8.4f}")


def main():
    """Main execution function with optimized ensemble learning"""
    try:
        print("Loading data...")
        train_df, test_df = load_data()
        
        print("Removing outliers...")
        train_df = remove_outliers(train_df)
        
        print("Preprocessing and engineering features...")
        X_train_encoded, X_test_encoded, y_train, train_ids, test_ids = preprocess_data(train_df, test_df)

        print(f"Training ensemble models...")
        print(f"Dataset size: {len(train_df)} training samples, {len(test_df)} test samples")
        print(f"Features: {X_train_encoded.shape[1]} after encoding\n")

        models_data = train_ensemble_models(
            X_train_encoded, X_test_encoded, y_train,
            thresholds=[0.25, 0.3, 0.35, 0.4],
            alphas=[0.1, 0.5, 1.0, 2.0],
            use_log=[True, False],
            use_poly=[False, True]
        )

        print("Creating ensemble predictions...")
        ensemble_pred = ensemble_predict(models_data, method='weighted_average', top_k=15)
        
        print("Generating visualizations...")
        visualize_ensemble_performance(models_data)
        
        print("Creating submission file...")
        generate_submission(ensemble_pred, test_ids)
        
        print("Analyzing best model...")
        analyze_best_model(models_data)
        
        print("\n✓ All tasks completed successfully!")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()