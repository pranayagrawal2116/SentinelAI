import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

def hybrid_feature_selection(X_train, y_train, feature_names, k=15):
    print(f"[Module 2] Starting Hybrid Feature Selection (Target features = {k})...")
    
    # We will store "votes" for each feature
    feature_votes = {feat: 0 for feat in feature_names}
    
    # 1. Filter Method (Statistical ANOVA F-value)
    print("  -> Running Filter Method (ANOVA SelectKBest)...")
    selector_filter = SelectKBest(score_func=f_classif, k=k)
    selector_filter.fit(X_train, y_train)
    filter_features = np.array(feature_names)[selector_filter.get_support()]
    for feat in filter_features:
        feature_votes[feat] += 1
        
    # 2. Wrapper Method (Recursive Feature Elimination - RFE)
    # Using DecisionTree as a lightweight estimator for RFE
    print("  -> Running Wrapper Method (RFE with Decision Tree)...")
    rfe_estimator = DecisionTreeClassifier(random_state=42)
    selector_rfe = RFE(estimator=rfe_estimator, n_features_to_select=k, step=5)
    selector_rfe.fit(X_train, y_train)
    rfe_features = np.array(feature_names)[selector_rfe.support_]
    for feat in rfe_features:
        feature_votes[feat] += 1
        
    # 3. Embedded Method (Tree-based Feature Importance)
    print("  -> Running Embedded Method (Random Forest Importance)...")
    rf_embedded = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    rf_embedded.fit(X_train, y_train)
    importances = rf_embedded.feature_importances_
    indices = np.argsort(importances)[::-1]
    embedded_features = [feature_names[i] for i in indices[:k]]
    for feat in embedded_features:
        feature_votes[feat] += 1
        
    # 4. Consensus Ranking
    print("  -> Calculating Hybrid Consensus...")
    # Sort features by number of votes (descending), then by their original order to break ties
    sorted_features = sorted(feature_votes.items(), key=lambda item: item[1], reverse=True)
    
    # Select features that appeared in at least 2 out of 3 methods, 
    # or just take the top 'k' if not enough features overlap
    selected_features = []
    for feat, votes in sorted_features:
        if votes >= 2:
            selected_features.append(feat)
            
    # Fallback: if intersection is too strict, just pad with the highest voted features up to k
    if len(selected_features) < k:
        for feat, votes in sorted_features:
            if feat not in selected_features:
                selected_features.append(feat)
            if len(selected_features) == k:
                break
                
    # If it selected more than k (rare but possible in ties), trim to k
    final_selected_features = selected_features[:k]
    
    print(f"[Module 2] Hybrid Selection Complete. Selected {len(final_selected_features)} features.")
    print(f"  -> Features: {final_selected_features}")
    
    return final_selected_features

def apply_feature_selection(X_train, X_test, selected_features):
    X_train_sel = X_train[selected_features]
    X_test_sel = X_test[selected_features]
    return X_train_sel, X_test_sel

if __name__ == "__main__":
    # Test logic
    from module1_preprocessing import get_iot_data, preprocess_data
    df = get_iot_data(use_synthetic=True)
    X_train, X_test, y_train, y_test, feats, classes = preprocess_data(df)
    selected_feats = hybrid_feature_selection(X_train, y_train, feats, k=15)
