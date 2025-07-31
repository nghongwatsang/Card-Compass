import json
import os
from typing import Dict, List, Any
from datetime import datetime

class DataManager:
    """Manages all data operations for Card Compass"""
    
    def __init__(self):
        self.data_dir = "data"
        self.cards_file = os.path.join(self.data_dir, "credit_cards.json")
        self.user_cards_file = os.path.join(self.data_dir, "user_cards.json")
        self.user_preferences_file = os.path.join(self.data_dir, "user_preferences.json")
    
    def initialize_data_files(self):
        """Initialize data files with default data if they don't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize credit cards data
        if not os.path.exists(self.cards_file):
            default_cards = self._get_default_cards_data()
            self._save_json(self.cards_file, default_cards)
        
        # Initialize user cards
        if not os.path.exists(self.user_cards_file):
            self._save_json(self.user_cards_file, [])
        
        # Initialize user preferences
        if not os.path.exists(self.user_preferences_file):
            default_preferences = {
                "reward_preference": "cashback",
                "monthly_spending": {},
                "created_at": datetime.now().isoformat()
            }
            self._save_json(self.user_preferences_file, default_preferences)
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        """Get all available credit cards"""
        return self._load_json(self.cards_file)
    
    def get_user_cards(self) -> List[Dict[str, Any]]:
        """Get user's credit cards"""
        return self._load_json(self.user_cards_file)
    
    def add_user_card(self, card_data: Dict[str, Any]):
        """Add a credit card to user's collection"""
        user_cards = self.get_user_cards()
        card_data['added_at'] = datetime.now().isoformat()
        user_cards.append(card_data)
        self._save_json(self.user_cards_file, user_cards)
    
    def remove_user_card(self, card_id: str):
        """Remove a credit card from user's collection"""
        user_cards = self.get_user_cards()
        user_cards = [card for card in user_cards if card.get('id') != card_id]
        self._save_json(self.user_cards_file, user_cards)
    
    def update_card_data(self, card_id: str, updated_data: Dict[str, Any]):
        """Update credit card data"""
        cards = self.get_all_cards()
        for i, card in enumerate(cards):
            if card.get('id') == card_id:
                cards[i].update(updated_data)
                cards[i]['updated_at'] = datetime.now().isoformat()
                break
        self._save_json(self.cards_file, cards)
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences"""
        return self._load_json(self.user_preferences_file)
    
    def update_user_preferences(self, preferences: Dict[str, Any]):
        """Update user preferences"""
        current_prefs = self.get_user_preferences()
        current_prefs.update(preferences)
        current_prefs['updated_at'] = datetime.now().isoformat()
        self._save_json(self.user_preferences_file, current_prefs)
    
    def _load_json(self, file_path: str) -> Any:
        """Load JSON data from file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_json(self, file_path: str, data: Any):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _get_default_cards_data(self) -> List[Dict[str, Any]]:
        """Get default credit cards data"""
        return [
            {
                "id": "chase_freedom_unlimited",
                "name": "Chase Freedom Unlimited",
                "issuer": "Chase",
                "type": "cashback",
                "rewards": {
                    "base_rate": 1.5,
                    "categories": {
                        "all_purchases": 1.5
                    }
                },
                "annual_fee": 0,
                "sign_up_bonus": {
                    "amount": 200,
                    "requirement": "Spend $500 in first 3 months"
                },
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "chase_sapphire_preferred",
                "name": "Chase Sapphire Preferred",
                "issuer": "Chase",
                "type": "points",
                "rewards": {
                    "base_rate": 1,
                    "categories": {
                        "travel": 2,
                        "dining": 2,
                        "all_purchases": 1
                    }
                },
                "annual_fee": 95,
                "sign_up_bonus": {
                    "amount": 60000,
                    "requirement": "Spend $4,000 in first 3 months"
                },
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "discover_it_cash_back",
                "name": "Discover it Cash Back",
                "issuer": "Discover",
                "type": "cashback",
                "rewards": {
                    "base_rate": 1,
                    "categories": {
                        "rotating_5x": 5,
                        "all_purchases": 1
                    },
                    "rotating_schedule": {
                        "Q1": "gas_stations_grocery_stores",
                        "Q2": "restaurants_paypal_gas_stations",
                        "Q3": "walmart_drugstores",
                        "Q4": "amazon_target"
                    }
                },
                "annual_fee": 0,
                "sign_up_bonus": {
                    "amount": "Double cash back first year",
                    "requirement": "No minimum spend"
                },
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "amex_gold",
                "name": "American Express Gold Card",
                "issuer": "American Express",
                "type": "points",
                "rewards": {
                    "base_rate": 1,
                    "categories": {
                        "dining": 4,
                        "groceries": 4,
                        "all_purchases": 1
                    }
                },
                "annual_fee": 250,
                "sign_up_bonus": {
                    "amount": 60000,
                    "requirement": "Spend $4,000 in first 6 months"
                },
                "updated_at": datetime.now().isoformat()
            }
        ]
