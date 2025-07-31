import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List, Any
from datetime import datetime
import logging

class CardScraper:
    """Web scraper for collecting credit card reward data"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Rate limiting
        self.request_delay = 2  # seconds between requests
    
    def update_all_cards(self):
        """Update all credit card data from various sources"""
        self.logger.info("Starting credit card data update...")
        
        try:
            # Update Chase cards
            chase_cards = self._scrape_chase_cards()
            
            # Update Discover cards
            discover_cards = self._scrape_discover_cards()
            
            # Update American Express cards
            amex_cards = self._scrape_amex_cards()
            
            # Combine all card data
            all_cards = chase_cards + discover_cards + amex_cards
            
            self.logger.info(f"Successfully updated {len(all_cards)} credit cards")
            return all_cards
            
        except Exception as e:
            self.logger.error(f"Error updating card data: {str(e)}")
            raise
    
    def _scrape_chase_cards(self) -> List[Dict[str, Any]]:
        """Scrape Chase credit card information"""
        self.logger.info("Scraping Chase cards...")
        
        # In a real implementation, you would scrape from Chase's website
        # For this demo, we'll return mock data that represents scraped information
        
        cards = [
            {
                "id": "chase_freedom_unlimited_updated",
                "name": "Chase Freedom Unlimited",
                "issuer": "Chase",
                "type": "cashback",
                "rewards": {
                    "base_rate": 1.5,
                    "categories": {
                        "all_purchases": 1.5,
                        "travel_through_chase": 5.0,
                        "dining": 3.0,
                        "drugstores": 3.0
                    }
                },
                "annual_fee": 0,
                "sign_up_bonus": {
                    "amount": 200,
                    "requirement": "Spend $500 in first 3 months"
                },
                "scraped_at": datetime.now().isoformat(),
                "source_url": "https://creditcards.chase.com/rewards-credit-cards/sapphire/preferred"
            },
            {
                "id": "chase_sapphire_preferred_updated",
                "name": "Chase Sapphire Preferred",
                "issuer": "Chase",
                "type": "points",
                "rewards": {
                    "base_rate": 1,
                    "categories": {
                        "travel": 2,
                        "dining": 2,
                        "online_grocery": 2,
                        "streaming": 2,
                        "all_purchases": 1
                    }
                },
                "annual_fee": 95,
                "sign_up_bonus": {
                    "amount": 60000,
                    "requirement": "Spend $4,000 in first 3 months"
                },
                "scraped_at": datetime.now().isoformat(),
                "source_url": "https://creditcards.chase.com/rewards-credit-cards/sapphire/preferred"
            }
        ]
        
        time.sleep(self.request_delay)
        return cards
    
    def _scrape_discover_cards(self) -> List[Dict[str, Any]]:
        """Scrape Discover credit card information"""
        self.logger.info("Scraping Discover cards...")
        
        # Mock data representing scraped Discover information
        cards = [
            {
                "id": "discover_it_cash_back_updated",
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
                "scraped_at": datetime.now().isoformat(),
                "source_url": "https://www.discover.com/credit-cards/cash-back/it-card.html"
            }
        ]
        
        time.sleep(self.request_delay)
        return cards
    
    def _scrape_amex_cards(self) -> List[Dict[str, Any]]:
        """Scrape American Express credit card information"""
        self.logger.info("Scraping American Express cards...")
        
        # Mock data representing scraped Amex information
        cards = [
            {
                "id": "amex_gold_updated",
                "name": "American Express Gold Card",
                "issuer": "American Express", 
                "type": "points",
                "rewards": {
                    "base_rate": 1,
                    "categories": {
                        "dining": 4,
                        "groceries": 4,
                        "gas_stations": 3,
                        "all_purchases": 1
                    }
                },
                "annual_fee": 250,
                "annual_credits": {
                    "dining": 120,
                    "uber": 120
                },
                "sign_up_bonus": {
                    "amount": 60000,
                    "requirement": "Spend $4,000 in first 6 months"
                },
                "scraped_at": datetime.now().isoformat(),
                "source_url": "https://www.americanexpress.com/us/credit-cards/card/gold-card/"
            },
            {
                "id": "amex_platinum_updated",
                "name": "The Platinum Card from American Express",
                "issuer": "American Express",
                "type": "points", 
                "rewards": {
                    "base_rate": 1,
                    "categories": {
                        "airlines": 5,
                        "hotels": 5,
                        "all_purchases": 1
                    }
                },
                "annual_fee": 695,
                "annual_credits": {
                    "airline": 200,
                    "hotel": 200,
                    "uber": 200,
                    "saks": 100,
                    "streaming": 240
                },
                "sign_up_bonus": {
                    "amount": 100000,
                    "requirement": "Spend $6,000 in first 6 months"
                },
                "scraped_at": datetime.now().isoformat(),
                "source_url": "https://www.americanexpress.com/us/credit-cards/card/platinum/"
            }
        ]
        
        time.sleep(self.request_delay)
        return cards
    
    def _make_request(self, url: str) -> BeautifulSoup:
        """Make a web request with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            self.logger.error(f"Request failed for {url}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Parsing failed for {url}: {str(e)}")
            raise
    
    def _extract_reward_rates(self, soup: BeautifulSoup, card_name: str) -> Dict[str, Any]:
        """Extract reward rates from parsed HTML"""
        # This would contain the actual parsing logic for each card issuer's website
        # Each issuer has different HTML structures, so this needs to be customized
        
        # Placeholder implementation
        rewards = {
            "base_rate": 1,
            "categories": {}
        }
        
        return rewards
    
    def _extract_annual_fee(self, soup: BeautifulSoup) -> int:
        """Extract annual fee information from parsed HTML"""
        # Placeholder implementation
        return 0
    
    def _extract_signup_bonus(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract sign-up bonus information from parsed HTML"""
        # Placeholder implementation
        return {
            "amount": 0,
            "requirement": "No requirement found"
        }
    
    def validate_scraped_data(self, card_data: Dict[str, Any]) -> bool:
        """Validate scraped credit card data"""
        required_fields = ['id', 'name', 'issuer', 'type', 'rewards']
        
        for field in required_fields:
            if field not in card_data:
                self.logger.warning(f"Missing required field: {field}")
                return False
        
        # Validate reward structure
        if 'base_rate' not in card_data['rewards']:
            self.logger.warning("Missing base_rate in rewards")
            return False
        
        return True
