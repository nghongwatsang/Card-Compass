# Card Compass - Credit Card Rewards Optimizer

Card Compass is a smart financial assistant that helps users maximize credit card rewards based on their spending habits and the benefits of the cards they own. It understands credit card reward structures, including cashback percentages, point multipliers, and rotating bonus categories.

![Card Compass Dashboard](https://via.placeholder.com/800x400/007bff/ffffff?text=Card+Compass+Dashboard)

## Features

### 🎯 Smart Reward Optimization

- Analyzes your spending patterns across different categories
- Recommends the best credit card to use for each purchase
- Maximizes either cashback or points based on your preference

### 💳 Credit Card Management

- Add and manage your credit card collection
- View detailed reward structures and benefits
- Track annual fees and sign-up bonuses

### 📊 Real-time Data Updates

- Web scraping from major credit card issuers (Chase, Amex, Discover)
- Up-to-date reward rates and bonus categories
- Quarterly rotating category updates

### 📈 Comprehensive Analytics

- Monthly and annual reward projections
- Category-wise spending breakdown
- Personalized recommendations for optimization

### 🔄 Automated Optimization

- Input your monthly spending by category
- Get instant recommendations on which card to use
- Maximize your rewards automatically

## Tech Stack

- **Backend**: Python Flask
- **Data Storage**: JSON files (local storage)
- **Web Scraping**: BeautifulSoup, requests
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5)
- **APIs**: RESTful API design

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository** (if using git):

   ```bash
   git clone <repository-url>
   cd "Card Compass"
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your web browser and navigate to `http://localhost:5000`

## Usage Guide

### Getting Started

1. **Add Your Credit Cards**:

   - Navigate to the "My Cards" section
   - Select from the available credit cards
   - Add all the cards you currently own

2. **Enter Your Spending**:

   - Go to the "Optimize" section
   - Choose your reward preference (Cashback or Points)
   - Enter your monthly spending amounts by category

3. **Get Recommendations**:

   - Click "Optimize My Spending"
   - Review the optimization results
   - See which card to use for each category

4. **Monitor Your Progress**:
   - Check the dashboard for monthly/annual projections
   - Follow personalized recommendations
   - Update card data regularly for the latest rates

### Spending Categories

Card Compass tracks the following spending categories:

- Groceries
- Gas Stations
- Restaurants & Dining
- Travel (Airlines, Hotels, Car Rental)
- Online Shopping
- Department Stores
- Utilities
- Streaming Services
- Phone Bills
- Other Purchases

## API Endpoints

### Cards Management

- `GET /api/cards` - Get all available credit cards
- `GET /api/user/cards` - Get user's credit cards
- `POST /api/user/cards` - Add a new card to user's collection

### Optimization

- `POST /api/optimize` - Calculate optimal spending strategy
- `GET /api/categories` - Get available spending categories

### Data Updates

- `POST /api/scrape/update` - Update card data via web scraping

## Data Structure

### Credit Card Data Format

```json
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
  }
}
```

### Optimization Request Format

```json
{
  "categories": {
    "groceries": 800,
    "gas": 200,
    "restaurants": 400,
    "travel": 500
  },
  "preference": "cashback"
}
```

## File Structure

```
Card Compass/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── .github/
│   └── copilot-instructions.md    # Copilot instructions
├── src/
│   ├── __init__.py
│   ├── data_manager.py            # Data management utilities
│   ├── reward_calculator.py       # Reward optimization algorithms
│   └── scrapers/
│       ├── __init__.py
│       └── card_scraper.py        # Web scraping utilities
├── templates/
│   └── index.html                 # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css             # Application styles
│   └── js/
│       └── app.js                # Frontend JavaScript
└── data/                          # JSON data storage (created at runtime)
    ├── credit_cards.json          # Available credit cards
    ├── user_cards.json           # User's credit cards
    └── user_preferences.json     # User preferences
```

## Development

### Adding New Credit Cards

1. Update the scraper in `src/scrapers/card_scraper.py`
2. Add the card data structure to the default cards in `src/data_manager.py`
3. Test the scraping functionality

### Extending Categories

1. Add new categories to the `get_spending_categories()` endpoint
2. Update the category mapping in `src/reward_calculator.py`
3. Update the frontend category display

### Customizing Algorithms

The reward calculation algorithms are in `src/reward_calculator.py`. You can:

- Modify the optimization logic
- Add new recommendation types
- Adjust scoring mechanisms

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Security Note

This application includes web scraping capabilities that should be used responsibly:

- Respect robots.txt files
- Implement appropriate rate limiting
- Consider using official APIs when available
- Be mindful of terms of service

## License

This project is for educational and personal use. Please ensure compliance with credit card issuer terms of service when using web scraping features.

## Roadmap

### Upcoming Features

- [ ] User authentication and profiles
- [ ] Historical spending analysis
- [ ] Integration with bank APIs
- [ ] Mobile-responsive design improvements
- [ ] Advanced analytics and reporting
- [ ] Credit score integration
- [ ] Automated card application recommendations

### Known Limitations

- Web scraping may break if card issuer websites change
- Limited to predefined credit cards
- No real-time transaction monitoring
- Manual spending input required

## Support

For questions, issues, or feature requests, please create an issue in the repository or contact the development team.

---

**Disclaimer**: Card Compass is a financial tool designed to help optimize credit card rewards. It does not provide financial advice. Users should always read credit card terms and conditions and consult with financial advisors for major financial decisions.
