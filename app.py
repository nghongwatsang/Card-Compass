from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from src.data_manager import DataManager
from src.reward_calculator import RewardCalculator
from src.scrapers.card_scraper import CardScraper

app = Flask(__name__)

# Initialize components
data_manager = DataManager()
reward_calculator = RewardCalculator()
card_scraper = CardScraper()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/cards', methods=['GET'])
def get_cards():
    """Get all available credit cards"""
    try:
        cards = data_manager.get_all_cards()
        return jsonify({"success": True, "cards": cards})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/user/cards', methods=['GET', 'POST'])
def user_cards():
    """Get or update user's credit cards"""
    if request.method == 'GET':
        try:
            user_cards = data_manager.get_user_cards()
            return jsonify({"success": True, "cards": user_cards})
        except Exception as e:
            response = jsonify({"success": False, "error": str(e)})
            response.status_code = 500
            return response

    elif request.method == 'POST':
        try:
            card_data = request.json
            data_manager.add_user_card(card_data)
            return jsonify({"success": True, "message": "Card added successfully"})
        except Exception as e:
            response = jsonify({"success": False, "error": str(e)})
            response.status_code = 500
            return response

@app.route('/api/optimize', methods=['POST'])
def optimize_spending():
    """Calculate optimal spending strategy"""
    try:
        spending_data = request.json
        user_cards = data_manager.get_user_cards()
        
        optimization = reward_calculator.optimize_spending(
            user_cards=user_cards,
            spending_categories=spending_data.get('categories', {}),
            preference=spending_data.get('preference', 'cashback')
        )
        
        return jsonify({
            "success": True,
            "optimization": optimization
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/scrape/update', methods=['POST'])
def update_card_data():
    """Update credit card data via web scraping"""
    try:
        card_scraper.update_all_cards()
        return jsonify({"success": True, "message": "Card data updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_spending_categories():
    """Get available spending categories"""
    categories = [
        "groceries", "gas", "restaurants", "travel", "online_shopping",
        "department_stores", "utilities", "insurance", "entertainment",
        "streaming_services", "phone_bill", "other"
    ]
    return jsonify({"success": True, "categories": categories})

if __name__ == '__main__':
    # Ensure data directories exist
    os.makedirs('data', exist_ok=True)
    
    # Initialize data files if they don't exist
    data_manager.initialize_data_files()
    
    app.run(debug=True, host='0.0.0.0', port=5001)
