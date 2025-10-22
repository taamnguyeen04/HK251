"""
Titanic Survival Prediction - Logistic Regression Ensemble (Optimized for higher accuracy)
No ML libraries (scikit-learn, TensorFlow, PyTorch)
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# ============================================================
# LOGISTIC REGRESSION MODEL
# ============================================================

class LogisticRegression:
    def __init__(self, learning_rate=0.01, n_iterations=5000, regularization=0.05, early_stopping=True, patience=200):
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.reg = regularization
        self.early_stopping = early_stopping
        self.patience = patience
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
        
        best_loss = float('inf')
        patience_counter = 0
        
        for t in range(1, self.n_iter + 1):
            z = np.dot(X, self.weights) + self.bias
            y_pred = self.sigmoid(z)
            
            # Compute loss
            y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)
            loss = -np.mean(y * np.log(y_pred_clipped) + (1 - y) * np.log(1 - y_pred_clipped))
            loss += (self.reg / (2 * n_samples)) * np.sum(self.weights ** 2)
            
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
            
            # Early stopping
            if self.early_stopping:
                if loss < best_loss:
                    best_loss = loss
                    patience_counter = 0
                else:
                    patience_counter += 1
                    if patience_counter >= self.patience:
                        break

    def predict_proba(self, X):
        return self.sigmoid(np.dot(X, self.weights) + self.bias)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


# ============================================================
# ENSEMBLE METHODS
# ============================================================

class VotingEnsemble:
    """Soft voting với diverse hyperparameters"""
    def __init__(self, n_models=7):
        self.n_models = n_models
        self.models = []

    def fit(self, X, y):
        configs = [
            {'learning_rate': 0.015, 'n_iterations': 5000, 'regularization': 0.03},
            {'learning_rate': 0.012, 'n_iterations': 5000, 'regularization': 0.05},
            {'learning_rate': 0.018, 'n_iterations': 4500, 'regularization': 0.04},
            {'learning_rate': 0.010, 'n_iterations': 5500, 'regularization': 0.06},
            {'learning_rate': 0.020, 'n_iterations': 4000, 'regularization': 0.035},
            {'learning_rate': 0.013, 'n_iterations': 5200, 'regularization': 0.055},
            {'learning_rate': 0.016, 'n_iterations': 4800, 'regularization': 0.045},
        ]
        
        for config in configs[:self.n_models]:
            model = LogisticRegression(**config)
            model.fit(X, y)
            self.models.append(model)

    def predict_proba(self, X):
        probs = np.array([m.predict_proba(X) for m in self.models])
        return np.mean(probs, axis=0)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


class BaggingEnsemble:
    """Bootstrap Aggregating with feature sampling"""
    def __init__(self, n_estimators=15, sample_ratio=0.85, feature_ratio=0.9):
        self.n_estimators = n_estimators
        self.sample_ratio = sample_ratio
        self.feature_ratio = feature_ratio
        self.models = []
        self.feature_indices = []

    def fit(self, X, y):
        n_samples, n_features = X.shape
        sample_size = int(n_samples * self.sample_ratio)
        n_features_sample = int(n_features * self.feature_ratio)
        
        for _ in range(self.n_estimators):
            # Bootstrap sampling
            indices = np.random.choice(n_samples, sample_size, replace=True)
            feature_idx = np.random.choice(n_features, n_features_sample, replace=False)
            
            X_sample = X[indices][:, feature_idx]
            y_sample = y[indices]
            
            model = LogisticRegression(learning_rate=0.015, n_iterations=4000, regularization=0.05)
            model.fit(X_sample, y_sample)
            self.models.append(model)
            self.feature_indices.append(feature_idx)

    def predict_proba(self, X):
        probs = np.array([m.predict_proba(X[:, feat_idx]) 
                         for m, feat_idx in zip(self.models, self.feature_indices)])
        return np.mean(probs, axis=0)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


class StackingEnsemble:
    """Stacking với diverse base models"""
    def __init__(self, n_base_models=7):
        self.n_base_models = n_base_models
        self.base_models = []
        self.meta_model = None

    def fit(self, X, y):
        configs = [
            {'learning_rate': 0.015, 'n_iterations': 5000, 'regularization': 0.03},
            {'learning_rate': 0.012, 'n_iterations': 5000, 'regularization': 0.05},
            {'learning_rate': 0.018, 'n_iterations': 4500, 'regularization': 0.04},
            {'learning_rate': 0.010, 'n_iterations': 5500, 'regularization': 0.06},
            {'learning_rate': 0.020, 'n_iterations': 4000, 'regularization': 0.035},
            {'learning_rate': 0.013, 'n_iterations': 5200, 'regularization': 0.055},
            {'learning_rate': 0.016, 'n_iterations': 4800, 'regularization': 0.045},
        ]
        
        for config in configs[:self.n_base_models]:
            model = LogisticRegression(**config)
            model.fit(X, y)
            self.base_models.append(model)
        
        # Meta-features
        meta_X = np.column_stack([m.predict_proba(X) for m in self.base_models])
        
        # Meta-model
        self.meta_model = LogisticRegression(learning_rate=0.01, n_iterations=2000, regularization=0.1)
        self.meta_model.fit(meta_X, y)

    def predict_proba(self, X):
        meta_X = np.column_stack([m.predict_proba(X) for m in self.base_models])
        return self.meta_model.predict_proba(meta_X)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


class WeightedVotingEnsemble:
    """Weighted voting dựa trên performance"""
    def __init__(self, n_models=7):
        self.n_models = n_models
        self.models = []
        self.weights = None

    def fit(self, X, y):
        configs = [
            {'learning_rate': 0.015, 'n_iterations': 5000, 'regularization': 0.03},
            {'learning_rate': 0.012, 'n_iterations': 5000, 'regularization': 0.05},
            {'learning_rate': 0.018, 'n_iterations': 4500, 'regularization': 0.04},
            {'learning_rate': 0.010, 'n_iterations': 5500, 'regularization': 0.06},
            {'learning_rate': 0.020, 'n_iterations': 4000, 'regularization': 0.035},
            {'learning_rate': 0.013, 'n_iterations': 5200, 'regularization': 0.055},
            {'learning_rate': 0.016, 'n_iterations': 4800, 'regularization': 0.045},
        ]
        
        accuracies = []
        for config in configs[:self.n_models]:
            model = LogisticRegression(**config)
            model.fit(X, y)
            pred = model.predict(X)
            acc = np.mean(pred == y)
            self.models.append(model)
            accuracies.append(acc)
        
        # Calculate weights based on accuracy
        accuracies = np.array(accuracies)
        self.weights = accuracies / np.sum(accuracies)

    def predict_proba(self, X):
        probs = np.array([m.predict_proba(X) for m in self.models])
        return np.average(probs, axis=0, weights=self.weights)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


# ============================================================
# FEATURE ENGINEERING (Enhanced)
# ============================================================

def feature_engineering(df):
    df = df.copy()
    
    # Title extraction with better grouping
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    rare_titles = ['Lady', 'Countess','Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona']
    df['Title'] = df['Title'].replace(rare_titles, 'Rare')
    df['Title'] = df['Title'].replace(['Mlle', 'Ms'], 'Miss')
    df['Title'] = df['Title'].replace('Mme', 'Mrs')
    title_map = {'Mr': 0, 'Miss': 1, 'Mrs': 2, 'Master': 3, 'Rare': 4}
    df['Title'] = df['Title'].map(title_map).fillna(4)
    
    # Family features
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    
    # Family survival groups (based on domain knowledge)
    df['FamilySizeGroup'] = 0  # Alone
    df.loc[(df['FamilySize'] >= 2) & (df['FamilySize'] <= 4), 'FamilySizeGroup'] = 1  # Small
    df.loc[df['FamilySize'] >= 5, 'FamilySizeGroup'] = 2  # Large
    
    # Age features with better binning
    age_median = df.groupby(['Sex', 'Pclass'])['Age'].transform('median')
    df['Age'].fillna(age_median, inplace=True)
    df['Child'] = (df['Age'] < 16).astype(int)
    df['Young'] = ((df['Age'] >= 16) & (df['Age'] < 32)).astype(int)
    df['Adult'] = ((df['Age'] >= 32) & (df['Age'] < 50)).astype(int)
    df['Senior'] = (df['Age'] >= 50).astype(int)
    
    # Fare features
    df['Fare'].fillna(df.groupby('Pclass')['Fare'].transform('median'), inplace=True)
    df['FarePerPerson'] = df['Fare'] / df['FamilySize']
    df['FareBin'] = pd.qcut(df['Fare'], q=5, labels=False, duplicates='drop')
    
    # Cabin features
    df['HasCabin'] = (~df['Cabin'].isna()).astype(int)
    df['Deck'] = df['Cabin'].fillna('U').str[0]
    deck_map = {'A': 0, 'B': 0, 'C': 0, 'D': 1, 'E': 1, 'F': 2, 'G': 2, 'T': 2, 'U': 3}
    df['Deck'] = df['Deck'].map(deck_map)
    
    # Embarked
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    embarked_map = {'C': 0, 'Q': 1, 'S': 2}
    df['Embarked'] = df['Embarked'].map(embarked_map)
    
    # Ticket features
    df['TicketLen'] = df['Ticket'].str.len()
    df['TicketIsNum'] = df['Ticket'].str.isdigit().astype(int)
    
    # Advanced interactions
    df['Sex_Pclass'] = df['Sex'].map({'male': 0, 'female': 1}) * 3 + df['Pclass']
    df['Age_Class'] = df['Age'] * df['Pclass']
    df['Fare_Age'] = df['Fare'] / (df['Age'] + 1)
    df['Family_Pclass'] = df['FamilySize'] * df['Pclass']
    
    # Gender-based features
    df['Female_Child'] = ((df['Sex'] == 'female') & (df['Age'] < 16)).astype(int)
    df['Female_Class1'] = ((df['Sex'] == 'female') & (df['Pclass'] == 1)).astype(int)
    df['Male_Class3'] = ((df['Sex'] == 'male') & (df['Pclass'] == 3)).astype(int)
    
    return df


def prepare_features(df, fit_params=None):
    df = feature_engineering(df)
    
    # Select features
    features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 
                'FamilySize', 'IsAlone', 'FamilySizeGroup',
                'HasCabin', 'Title', 'Deck', 'Embarked',
                'Child', 'Young', 'Adult', 'Senior',
                'FarePerPerson', 'FareBin', 'TicketLen', 'TicketIsNum',
                'Sex_Pclass', 'Age_Class', 'Fare_Age', 'Family_Pclass',
                'Female_Child', 'Female_Class1', 'Male_Class3']
    
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
    
    X = df[features].copy()
    
    # Handle any remaining NaN
    X = X.fillna(X.median())
    
    # Standardization
    if fit_params is None:
        fit_params = {
            'mean': X.mean(),
            'std': X.std().replace(0, 1)
        }
    
    X = (X - fit_params['mean']) / fit_params['std']
    return X.values, fit_params


def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():
    np.random.seed(42)  # For reproducibility
    
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
        'Single LR (Optimized)': LogisticRegression(learning_rate=0.015, n_iterations=5000, regularization=0.05),
        'Voting (7 LR)': VotingEnsemble(n_models=10),
        'Weighted Voting (7 LR)': WeightedVotingEnsemble(n_models=10),
        'Bagging (15 LR)': BaggingEnsemble(n_estimators=15, sample_ratio=0.85, feature_ratio=0.9),
        'Stacking (7+1 LR)': StackingEnsemble(n_base_models=15)
    }
    
    results = {}
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_train)
        acc = accuracy(y_train, y_pred)
        results[name] = acc
        print(f"{name:25s} - Train Accuracy: {acc:.4f}")
    
    # Best model
    best_name = max(results, key=results.get)
    print(f"\nBest Model: {best_name} ({results[best_name]:.4f})")
    
    # Generate predictions with best model
    best_model = models[best_name]
    y_test_pred = best_model.predict(X_test)
    
    submission = pd.DataFrame({
        'PassengerId': test_df['PassengerId'],
        'Survived': y_test_pred
    })
    submission.to_csv('submission.csv', index=False)
    print(f"\nPredictions saved: {np.sum(y_test_pred)}/{len(y_test_pred)} survivors ({100*np.sum(y_test_pred)/len(y_test_pred):.1f}%)")


if __name__ == "__main__":
    main()