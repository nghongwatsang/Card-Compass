from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import calendar

class RewardCalculator:
    """Calculates optimal credit card usage for maximum rewards"""
    
    def __init__(self):
        self.category_mapping = {
            "groceries": ["groceries", "grocery_stores", "supermarkets"],
            "gas": ["gas", "gas_stations", "fuel"],
            "restaurants": ["dining", "restaurants", "food"],
            "travel": ["travel", "airlines", "hotels", "car_rental"],
            "online_shopping": ["online", "e_commerce", "amazon"],
            "department_stores": ["department_stores", "retail"],
            "utilities": ["utilities", "bills"],
            "streaming_services": ["streaming", "entertainment"],
            "phone_bill": ["phone", "telecommunications"]
        }
    
    def optimize_spending(self, user_cards: List[Dict], spending_categories: Dict[str, float], 
                         preference: str = "cashback") -> Dict[str, Any]:
        """
        Calculate optimal spending strategy for maximum rewards
        
        Args:
            user_cards: List of user's credit cards
            spending_categories: Dict of category -> monthly spending amount
            preference: 'cashback' or 'points'
        
        Returns:
            Optimization results with recommendations
        """
        if not user_cards:
            return {
                "error": "No credit cards found. Please add your cards first.",
                "recommendations": []
            }
        
        # Filter cards by preference
        relevant_cards = self._filter_cards_by_preference(user_cards, preference)
        
        # Calculate rewards for each category
        category_optimizations = {}
        total_rewards = 0
        
        for category, amount in spending_categories.items():
            if amount > 0:
                best_card, reward_amount = self._find_best_card_for_category(
                    relevant_cards, category, amount
                )
                
                category_optimizations[category] = {
                    "amount": amount,
                    "best_card": best_card,
                    "reward_amount": reward_amount,
                    "reward_rate": reward_amount / amount if amount > 0 else 0
                }
                total_rewards += reward_amount
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            category_optimizations, user_cards, preference
        )
        
        # Calculate monthly and annual projections
        monthly_projection = total_rewards
        annual_projection = total_rewards * 12
        
        return {
            "total_monthly_rewards": round(monthly_projection, 2),
            "total_annual_rewards": round(annual_projection, 2),
            "currency": "USD" if preference == "cashback" else "points",
            "category_breakdown": category_optimizations,
            "recommendations": recommendations,
            "optimization_date": datetime.now().isoformat()
        }
    
    def _filter_cards_by_preference(self, cards: List[Dict], preference: str) -> List[Dict]:
        """Filter cards based on user preference (cashback or points)"""
        if preference == "cashback":
            return [card for card in cards if card.get("type") == "cashback"]
        elif preference == "points":
            return [card for card in cards if card.get("type") == "points"]
        else:
            return cards
    
    def _find_best_card_for_category(self, cards: List[Dict], category: str, 
                                   amount: float) -> Tuple[Dict, float]:
        """Find the best credit card for a specific spending category"""
        best_card = None
        max_reward = 0
        
        for card in cards:
            reward_amount = self._calculate_reward_for_category(card, category, amount)
            
            if reward_amount > max_reward:
                max_reward = reward_amount
                best_card = card
        
        # If no specific category match, use base rate
        if best_card is None and cards:
            best_card = cards[0]  # Default to first card
            max_reward = self._calculate_base_reward(best_card, amount)
        
        return best_card, max_reward
    
    def _calculate_reward_for_category(self, card: Dict, category: str, 
                                     amount: float) -> float:
        """Calculate reward amount for a specific category and card"""
        rewards = card.get("rewards", {})
        categories = rewards.get("categories", {})
        
        # Check for direct category match
        if category in categories:
            rate = categories[category]
            return amount * (rate / 100) if card.get("type") == "cashback" else amount * rate
        
        # Check for mapped category matches
        category_variations = self.category_mapping.get(category, [category])
        for variation in category_variations:
            if variation in categories:
                rate = categories[variation]
                return amount * (rate / 100) if card.get("type") == "cashback" else amount * rate
        
        # Check for rotating categories (like Discover)
        if "rotating_5x" in categories:
            current_quarter = self._get_current_quarter()
            rotating_schedule = rewards.get("rotating_schedule", {})
            
            if current_quarter in rotating_schedule:
                rotating_category = rotating_schedule[current_quarter]
                if any(cat in rotating_category.lower() for cat in category_variations):
                    rate = categories["rotating_5x"]
                    return amount * (rate / 100) if card.get("type") == "cashback" else amount * rate
        
        # Fall back to base rate
        return self._calculate_base_reward(card, amount)
    
    def _calculate_base_reward(self, card: Dict, amount: float) -> float:
        """Calculate reward using base rate"""
        base_rate = card.get("rewards", {}).get("base_rate", 1)
        
        if card.get("type") == "cashback":
            return amount * (base_rate / 100)
        else:  # points
            return amount * base_rate
    
    def _get_current_quarter(self) -> str:
        """Get current quarter (Q1, Q2, Q3, Q4)"""
        current_month = datetime.now().month
        if current_month <= 3:
            return "Q1"
        elif current_month <= 6:
            return "Q2"
        elif current_month <= 9:
            return "Q3"
        else:
            return "Q4"
    
    def _generate_recommendations(self, optimizations: Dict, all_cards: List[Dict], 
                                preference: str) -> List[Dict]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Recommendation 1: Missing high-reward categories
        missing_categories = self._find_missing_high_reward_categories(optimizations, all_cards)
        if missing_categories:
            recommendations.append({
                "type": "missing_categories",
                "title": "Consider cards for high-spend categories",
                "description": f"You could earn more rewards in: {', '.join(missing_categories)}",
                "priority": "high"
            })
        
        # Recommendation 2: Annual fee optimization
        fee_recommendation = self._analyze_annual_fees(optimizations, all_cards)
        if fee_recommendation:
            recommendations.append(fee_recommendation)
        
        # Recommendation 3: Rotating category optimization
        rotating_rec = self._check_rotating_categories(optimizations)
        if rotating_rec:
            recommendations.append(rotating_rec)
        
        # Recommendation 4: Sign-up bonus opportunities
        signup_rec = self._check_signup_bonuses(all_cards)
        if signup_rec:
            recommendations.append(signup_rec)
        
        return recommendations
    
    def _find_missing_high_reward_categories(self, optimizations: Dict, 
                                           all_cards: List[Dict]) -> List[str]:
        """Find categories where user could get better rewards"""
        missing = []
        
        for category, data in optimizations.items():
            current_rate = data.get("reward_rate", 0)
            
            # Check if there are better cards available for this category
            for card in all_cards:
                potential_reward = self._calculate_reward_for_category(
                    card, category, data["amount"]
                )
                potential_rate = potential_reward / data["amount"] if data["amount"] > 0 else 0
                
                if potential_rate > current_rate * 1.5:  # 50% better
                    missing.append(category)
                    break
        
        return missing
    
    def _analyze_annual_fees(self, optimizations: Dict, all_cards: List[Dict]) -> Dict:
        """Analyze if paying annual fees would be worth it"""
        total_annual_rewards = sum(data["reward_amount"] * 12 for data in optimizations.values())
        
        # Check for premium cards that might be worth the fee
        for card in all_cards:
            annual_fee = card.get("annual_fee", 0)
            if annual_fee > 0:
                # Calculate potential rewards with this card
                potential_rewards = 0
                for category, data in optimizations.items():
                    reward = self._calculate_reward_for_category(card, category, data["amount"])
                    potential_rewards += reward
                
                annual_potential = potential_rewards * 12
                net_benefit = annual_potential - total_annual_rewards - annual_fee
                
                if net_benefit > 100:  # At least $100 net benefit
                    return {
                        "type": "annual_fee",
                        "title": f"Consider {card['name']}",
                        "description": f"Could earn ${net_benefit:.0f} more annually after ${annual_fee} fee",
                        "priority": "medium"
                    }
        
        return None
    
    def _check_rotating_categories(self, optimizations: Dict) -> Dict:
        """Check for rotating category opportunities"""
        current_quarter = self._get_current_quarter()
        
        # This is a simplified check - in a real app, you'd have more detailed data
        return {
            "type": "rotating",
            "title": f"Check Q{current_quarter[-1]} rotating categories",
            "description": "Make sure you're maximizing quarterly bonus categories",
            "priority": "low"
        }
    
    def _check_signup_bonuses(self, all_cards: List[Dict]) -> Dict:
        """Check for available sign-up bonuses"""
        # This would typically check against cards the user doesn't have
        return {
            "type": "signup_bonus",
            "title": "New card opportunities",
            "description": "Consider new cards with sign-up bonuses if you can meet spending requirements",
            "priority": "low"
        }
