import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class LogisticRegression:
    def __init__(self, learning_rate=0.01, n_iterations=3000, regularization=0.05):
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.reg = regularization
        self.weights = None
        self.bias = None
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.eps = 1e-8

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.random.randn(n_features) * 0.01
        self.bias = 0
        
        m_w = np.zeros(n_features)
        v_w = np.zeros(n_features)
        m_b = v_b = 0
        
        for t in range(1, self.n_iter + 1):
            z = np.dot(X, self.weights) + self.bias
            y_pred = self.sigmoid(z)
            
            dw = (1/n_samples) * (np.dot(X.T, y_pred - y) + self.reg * self.weights)
            db = (1/n_samples) * np.sum(y_pred - y)
            
            m_w = self.beta1 * m_w + (1 - self.beta1) * dw
            m_b = self.beta1 * m_b + (1 - self.beta1) * db
            v_w = self.beta2 * v_w + (1 - self.beta2) * (dw ** 2)
            v_b = self.beta2 * v_b + (1 - self.beta2) * (db ** 2)
            
            m_w_hat = m_w / (1 - self.beta1 ** t)
            m_b_hat = m_b / (1 - self.beta1 ** t)
            v_w_hat = v_w / (1 - self.beta2 ** t)
            v_b_hat = v_b / (1 - self.beta2 ** t)
            
            self.weights -= self.lr * m_w_hat / (np.sqrt(v_w_hat) + self.eps)
            self.bias -= self.lr * m_b_hat / (np.sqrt(v_b_hat) + self.eps)

    def predict_proba(self, X):
        return self.sigmoid(np.dot(X, self.weights) + self.bias)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


# ============================================================
# ENSEMBLE METHODS
# ============================================================

class VotingEnsemble:
    """Soft voting với trọng số"""
    def __init__(self, n_models=5, weights=None):
        self.n_models = n_models
        self.models = []
        self.weights = weights if weights else np.ones(n_models) / n_models

    def fit(self, X, y):
        for i in range(self.n_models):
            model = LogisticRegression(
                learning_rate=0.01 + i*0.002,
                n_iterations=2500 + i*100,
                regularization=0.03 + i*0.01
            )
            model.fit(X, y)
            self.models.append(model)

    def predict_proba(self, X):
        probs = np.array([m.predict_proba(X) for m in self.models])
        return np.average(probs, axis=0, weights=self.weights)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


class BaggingEnsemble:
    """Bootstrap Aggregating"""
    def __init__(self, n_estimators=10, sample_ratio=0.8):
        self.n_estimators = n_estimators
        self.sample_ratio = sample_ratio
        self.models = []

    def fit(self, X, y):
        n_samples = X.shape[0]
        sample_size = int(n_samples * self.sample_ratio)
        
        for _ in range(self.n_estimators):
            indices = np.random.choice(n_samples, sample_size, replace=True)
            X_sample, y_sample = X[indices], y[indices]
            
            model = LogisticRegression(learning_rate=0.015, n_iterations=2000)
            model.fit(X_sample, y_sample)
            self.models.append(model)

    def predict_proba(self, X):
        probs = np.array([m.predict_proba(X) for m in self.models])
        return np.mean(probs, axis=0)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


class StackingEnsemble:
    """Stacking với meta-learner"""
    def __init__(self, n_base_models=5):
        self.n_base_models = n_base_models
        self.base_models = []
        self.meta_model = None

    def fit(self, X, y):
        # Train base models
        for i in range(self.n_base_models):
            model = LogisticRegression(
                learning_rate=0.01 + i*0.003,
                n_iterations=2000,
                regularization=0.04 + i*0.01
            )
            model.fit(X, y)
            self.base_models.append(model)
        
        # Generate meta-features
        meta_X = np.column_stack([m.predict_proba(X) for m in self.base_models])
        
        # Train meta-model
        self.meta_model = LogisticRegression(learning_rate=0.01, n_iterations=1000)
        self.meta_model.fit(meta_X, y)

    def predict_proba(self, X):
        meta_X = np.column_stack([m.predict_proba(X) for m in self.base_models])
        return self.meta_model.predict_proba(meta_X)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


class BlendingEnsemble:
    """Blending với validation set"""
    def __init__(self, n_models=5, val_split=0.2):
        self.n_models = n_models
        self.val_split = val_split
        self.base_models = []
        self.meta_model = None

    def fit(self, X, y):
        n_samples = X.shape[0]
        n_val = int(n_samples * self.val_split)
        indices = np.random.permutation(n_samples)
        train_idx, val_idx = indices[n_val:], indices[:n_val]
        
        X_train, y_train = X[train_idx], y[train_idx]
        X_val, y_val = X[val_idx], y[val_idx]
        
        # Train base models
        for i in range(self.n_models):
            model = LogisticRegression(
                learning_rate=0.012 + i*0.002,
                n_iterations=2500,
                regularization=0.05 + i*0.008
            )
            model.fit(X_train, y_train)
            self.base_models.append(model)
        
        # Generate meta-features from validation set
        meta_X = np.column_stack([m.predict_proba(X_val) for m in self.base_models])
        
        # Train meta-model
        self.meta_model = LogisticRegression(learning_rate=0.01, n_iterations=800)
        self.meta_model.fit(meta_X, y_val)

    def predict_proba(self, X):
        meta_X = np.column_stack([m.predict_proba(X) for m in self.base_models])
        return self.meta_model.predict_proba(meta_X)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)

def feature_engineering(df):
    df = df.copy()
    
    # Title extraction
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    title_map = {'Mr': 0, 'Miss': 1, 'Mrs': 2, 'Master': 3, 'Rev': 4, 'Dr': 4, 'Col': 4, 'Major': 4, 'Mlle': 1, 'Mme': 2, 'Don': 4, 'Dona': 4, 'Lady': 4, 'Countess': 4, 'Jonkheer': 4, 'Sir': 4, 'Capt': 4, 'Ms': 1}
    df['Title'] = df['Title'].map(title_map).fillna(4)
    
    # Family features
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    df['FamilySizeBin'] = pd.cut(df['FamilySize'], bins=[0, 1, 4, 11], labels=[0, 1, 2])
    
    # Age features
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 35, 60, 100], labels=[0, 1, 2, 3, 4])
    
    # Fare features
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    df['FarePerPerson'] = df['Fare'] / df['FamilySize']
    df['FareBin'] = pd.qcut(df['Fare'], q=4, labels=[0, 1, 2, 3], duplicates='drop')
    
    # Cabin features
    df['HasCabin'] = (~df['Cabin'].isna()).astype(int)
    df['Deck'] = df['Cabin'].fillna('U').str[0].map({c: i for i, c in enumerate('ABCDEFGTU')})
    
    # Embarked
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    df['EmbarkedNum'] = df['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})
    
    # Interactions
    df['Age_Class'] = df['Age'] * df['Pclass']
    df['Fare_Class'] = df['Fare'] / df['Pclass']
    
    return df


def prepare_features(df, fit_params=None):
    df = feature_engineering(df)
    
    features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 
                'FamilySize', 'IsAlone', 'HasCabin', 'Title', 'Deck',
                'FamilySizeBin', 'AgeGroup', 'FareBin', 'EmbarkedNum',
                'FarePerPerson', 'Age_Class', 'Fare_Class']
    
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
    
    X = df[features].copy()
    for col in X.select_dtypes(include=['category']).columns:
        X[col] = X[col].astype(int)
    
    if fit_params is None:
        fit_params = {'mean': X.mean(), 'std': X.std().replace(0, 1)}
    
    X = (X - fit_params['mean']) / fit_params['std']
    return X.values, fit_params


def main():
    # Load data
    train_df = pd.read_csv('C:/Users/tam/Documents/data/titanic/train.csv')
    test_df = pd.read_csv('C:/Users/tam/Documents/data/titanic/test.csv')
    
    # Prepare features
    X_train, fit_params = prepare_features(train_df)
    y_train = train_df['Survived'].values
    X_test, _ = prepare_features(test_df, fit_params)
    
    print(f"Training samples: {X_train.shape[0]}, Features: {X_train.shape[1]}\n")
    
    # Models
    models = {
        'Single LR': LogisticRegression(learning_rate=0.015, n_iterations=3000, regularization=0.05),
        'Voting (5 LR)': VotingEnsemble(n_models=5),
        'Bagging (10 LR)': BaggingEnsemble(n_estimators=10, sample_ratio=0.8),
        'Stacking (5+1 LR)': StackingEnsemble(n_base_models=8),
        'Blending (5+1 LR)': BlendingEnsemble(n_models=5, val_split=0.2)
    }
    
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_train)
        acc = np.mean(y_train == y_pred)
        results[name] = acc
        print(f"{name:20s} - Accuracy: {acc:.4f}")
    
    # Best model
    best_name = max(results, key=results.get)
    print(f"\nBest Model: {best_name} ({results[best_name]:.4f})")
    
    # Generate predictions
    best_model = models[best_name]
    y_test_pred = best_model.predict(X_test)
    
    submission = pd.DataFrame({
        'PassengerId': test_df['PassengerId'],
        'Survived': y_test_pred
    })
    submission.to_csv('submission.csv', index=False)
    print(f"\nPredictions saved: {np.sum(y_test_pred)}/{len(y_test_pred)} survivors")


if __name__ == "__main__":
    main()