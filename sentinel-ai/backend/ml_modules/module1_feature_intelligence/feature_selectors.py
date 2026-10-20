import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

class HybridFeatureSelector:
    """
    Implements Filter, RFE, and Tree-based feature selection, 
    followed by a consensus ranking mechanism.
    """
    def __init__(self, target_features: int = 20):
        self.target_features = target_features
        self.selection_stats: Dict[str, Any] = {}

    def run_filter_selection(self, X_train: pd.DataFrame, y_train: pd.Series) -> List[str]:
        print("  -> Running Filter Method (ANOVA F-value)...")
        # Select slightly more than target to allow consensus filtering
        k = min(self.target_features + 5, X_train.shape[1])
        selector = SelectKBest(score_func=f_classif, k=k)
        selector.fit(X_train, y_train)
        
        selected = X_train.columns[selector.get_support()].tolist()
        self.selection_stats['filter_selected_count'] = len(selected)
        self.selection_stats['filter_selected_features'] = selected
        return selected

    def run_rfe_selection(self, X_train: pd.DataFrame, y_train: pd.Series) -> List[str]:
        print("  -> Running Wrapper Method (RFE)...")
        # Using DecisionTree as it's computationally feasible for RFE on large datasets
        estimator = DecisionTreeClassifier(random_state=42)
        k = min(self.target_features + 5, X_train.shape[1])
        selector = RFE(estimator=estimator, n_features_to_select=k, step=0.1)
        selector.fit(X_train, y_train)
        
        selected = X_train.columns[selector.support_].tolist()
        self.selection_stats['rfe_selected_count'] = len(selected)
        self.selection_stats['rfe_selected_features'] = selected
        return selected

    def run_tree_importance(self, X_train: pd.DataFrame, y_train: pd.Series) -> List[str]:
        print("  -> Running Embedded Method (Tree-based Importance)...")
        rf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1, max_depth=10)
        rf.fit(X_train, y_train)
        
        importances = rf.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        k = min(self.target_features + 5, X_train.shape[1])
        selected = [X_train.columns[i] for i in indices[:k]]
        
        self.selection_stats['tree_selected_count'] = len(selected)
        self.selection_stats['tree_selected_features'] = selected
        return selected

    def hybrid_consensus(self, filter_feats: List[str], rfe_feats: List[str], tree_feats: List[str]) -> List[str]:
        """
        Combines the outputs of the three methods using a voting mechanism.
        """
        print("  -> Calculating Hybrid Feature-Ranking/Consensus...")
        feature_votes: Dict[str, int] = {}
        
        for feat in filter_feats + rfe_feats + tree_feats:
            feature_votes[feat] = feature_votes.get(feat, 0) + 1
            
        # Sort by votes (desc), then alphabetically
        sorted_features = sorted(feature_votes.items(), key=lambda x: (-x[1], x[0]))
        
        # Take features with at least 2 votes
        consensus_selected = [feat for feat, votes in sorted_features if votes >= 2]
        
        # If too few features overlap, just take the top ones up to target_features
        if len(consensus_selected) < self.target_features:
            consensus_selected = [feat for feat, votes in sorted_features][:self.target_features]
            
        # Ensure we don't exceed target
        final_selected = consensus_selected[:self.target_features]
        
        self.selection_stats['hybrid_consensus_count'] = len(final_selected)
        self.selection_stats['hybrid_consensus_features'] = final_selected
        self.selection_stats['feature_votes'] = feature_votes
        
        return final_selected

    def select_features(self, X_train: pd.DataFrame, y_train: pd.Series) -> List[str]:
        """Runs the entire hybrid feature selection pipeline."""
        filter_feats = self.run_filter_selection(X_train, y_train)
        rfe_feats = self.run_rfe_selection(X_train, y_train)
        tree_feats = self.run_tree_importance(X_train, y_train)
        
        final_features = self.hybrid_consensus(filter_feats, rfe_feats, tree_feats)
        print(f"[Module 1] Final feature subset contains {len(final_features)} features.")
        return final_features

    def get_stats(self) -> Dict[str, Any]:
        return self.selection_stats
