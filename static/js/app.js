// Card Compass - Main JavaScript Application
class CardCompass {
    constructor() {
        this.currentSection = 'dashboard';
        this.userCards = [];
        this.availableCards = [];
        this.spendingCategories = [];
        this.optimizationResults = null;
        
        this.init();
    }
    
    async init() {
        this.setupEventListeners();
        await this.loadInitialData();
        this.showSection('dashboard');
    }
    
    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.getAttribute('href').replace('#', '');
                this.showSection(section);
            });
        });
        
        // Add card form
        document.getElementById('add-card-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addUserCard();
        });
        
        // Spending optimization form
        document.getElementById('spending-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.optimizeSpending();
        });
        
        // Update cards button
        document.getElementById('update-cards-btn').addEventListener('click', () => {
            this.updateCardData();
        });
    }
    
    async loadInitialData() {
        try {
            await Promise.all([
                this.loadAvailableCards(),
                this.loadUserCards(),
                this.loadSpendingCategories()
            ]);
            
            this.updateDashboard();
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showError('Failed to load application data');
        }
    }
    
    async loadAvailableCards() {
        try {
            const response = await fetch('/api/cards');
            const data = await response.json();
            
            if (data.success) {
                this.availableCards = data.cards;
                this.populateCardSelect();
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error loading available cards:', error);
            throw error;
        }
    }
    
    async loadUserCards() {
        try {
            const response = await fetch('/api/user/cards');
            const data = await response.json();
            
            if (data.success) {
                this.userCards = data.cards;
                this.displayUserCards();
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error loading user cards:', error);
            throw error;
        }
    }
    
    async loadSpendingCategories() {
        try {
            const response = await fetch('/api/categories');
            const data = await response.json();
            
            if (data.success) {
                this.spendingCategories = data.categories;
                this.displaySpendingCategories();
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error loading spending categories:', error);
            throw error;
        }
    }
    
    showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.section').forEach(section => {
            section.style.display = 'none';
        });
        
        // Show target section
        document.getElementById(sectionName).style.display = 'block';
        
        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[href="#${sectionName}"]`).classList.add('active');
        
        this.currentSection = sectionName;
        
        // Load section-specific data
        if (sectionName === 'dashboard') {
            this.updateDashboard();
        }
    }
    
    populateCardSelect() {
        const select = document.getElementById('card-select');
        select.innerHTML = '<option value="">Choose a card...</option>';
        
        this.availableCards.forEach(card => {
            const option = document.createElement('option');
            option.value = card.id;
            option.textContent = `${card.name} (${card.issuer})`;
            select.appendChild(option);
        });
    }
    
    displayUserCards() {
        const container = document.getElementById('user-cards-list');
        
        if (this.userCards.length === 0) {
            container.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    No credit cards added yet. Add your first card to get started!
                </div>
            `;
            return;
        }
        
        container.innerHTML = this.userCards.map(card => `
            <div class="card-item">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <div class="card-issuer">${card.issuer}</div>
                        <div class="card-name">${card.name}</div>
                        <span class="card-type ${card.type}">${card.type}</span>
                    </div>
                    <button class="btn btn-sm btn-outline-danger" onclick="cardCompass.removeUserCard('${card.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="mt-2">
                    <small class="text-muted">
                        Annual Fee: $${card.annual_fee || 0} |
                        Base Rate: ${card.rewards.base_rate}${card.type === 'cashback' ? '%' : 'x'}
                    </small>
                </div>
                ${this.renderCardRewards(card)}
            </div>
        `).join('');
    }
    
    renderCardRewards(card) {
        const categories = card.rewards.categories || {};
        const categoryHtml = Object.entries(categories)
            .map(([category, rate]) => `
                <div class="reward-category">
                    ${this.formatCategoryName(category)}: ${rate}${card.type === 'cashback' ? '%' : 'x'}
                </div>
            `).join('');
        
        return categoryHtml ? `<div class="mt-2">${categoryHtml}</div>` : '';
    }
    
    displaySpendingCategories() {
        const container = document.getElementById('spending-categories');
        
        container.innerHTML = this.spendingCategories.map(category => `
            <div class="spending-category">
                <label for="${category}" class="form-label">
                    ${this.formatCategoryName(category)}
                </label>
                <div class="input-group">
                    <span class="input-group-text">$</span>
                    <input type="number" class="form-control" id="${category}" 
                           name="${category}" min="0" step="0.01" placeholder="0.00">
                </div>
            </div>
        `).join('');
    }
    
    async addUserCard() {
        const cardId = document.getElementById('card-select').value;
        
        if (!cardId) {
            this.showError('Please select a card');
            return;
        }
        
        const selectedCard = this.availableCards.find(card => card.id === cardId);
        if (!selectedCard) {
            this.showError('Selected card not found');
            return;
        }
        
        // Check if card already exists
        if (this.userCards.some(card => card.id === cardId)) {
            this.showError('This card is already in your collection');
            return;
        }
        
        try {
            this.showLoading(true);
            
            const response = await fetch('/api/user/cards', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(selectedCard)
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadUserCards();
                document.getElementById('add-card-form').reset();
                this.showSuccess('Card added successfully!');
                this.updateDashboard();
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error adding card:', error);
            this.showError('Failed to add card');
        } finally {
            this.showLoading(false);
        }
    }
    
    async removeUserCard(cardId) {
        if (!confirm('Are you sure you want to remove this card?')) {
            return;
        }
        
        try {
            this.userCards = this.userCards.filter(card => card.id !== cardId);
            this.displayUserCards();
            this.updateDashboard();
            this.showSuccess('Card removed successfully!');
        } catch (error) {
            console.error('Error removing card:', error);
            this.showError('Failed to remove card');
        }
    }
    
    async optimizeSpending() {
        const formData = new FormData(document.getElementById('spending-form'));
        const spendingData = {};
        
        // Collect spending amounts
        const categories = {};
        this.spendingCategories.forEach(category => {
            const amount = parseFloat(formData.get(category)) || 0;
            if (amount > 0) {
                categories[category] = amount;
            }
        });
        
        if (Object.keys(categories).length === 0) {
            this.showError('Please enter at least one spending amount');
            return;
        }
        
        spendingData.categories = categories;
        spendingData.preference = document.getElementById('reward-preference').value;
        
        try {
            this.showLoading(true);
            
            const response = await fetch('/api/optimize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(spendingData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.optimizationResults = data.optimization;
                this.displayOptimizationResults();
                this.updateDashboard();
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error optimizing spending:', error);
            this.showError('Failed to optimize spending');
        } finally {
            this.showLoading(false);
        }
    }
    
    displayOptimizationResults() {
        const container = document.getElementById('optimization-results');
        
        if (!this.optimizationResults) {
            container.innerHTML = '<p class="text-muted">No optimization results available.</p>';
            return;
        }
        
        const results = this.optimizationResults;
        const currency = results.currency === 'USD' ? '$' : ' points';
        
        container.innerHTML = `
            <div class="optimization-result">
                <h6>Monthly Rewards: <span class="text-success">${currency}${results.total_monthly_rewards}</span></h6>
                <h6>Annual Projection: <span class="text-success">${currency}${results.total_annual_rewards}</span></h6>
            </div>
            
            <h6 class="mt-3">Category Breakdown:</h6>
            ${Object.entries(results.category_breakdown || {}).map(([category, data]) => `
                <div class="optimization-result">
                    <strong>${this.formatCategoryName(category)}</strong><br>
                    <small class="text-muted">
                        Spending: $${data.amount} | 
                        Rewards: ${currency}${data.reward_amount.toFixed(2)} |
                        Best Card: ${data.best_card?.name || 'None'}
                    </small>
                </div>
            `).join('')}
            
            ${results.recommendations?.length ? `
                <h6 class="mt-3">Recommendations:</h6>
                ${results.recommendations.map(rec => `
                    <div class="recommendation ${rec.priority}">
                        <div class="recommendation-title">${rec.title}</div>
                        <div class="recommendation-description">${rec.description}</div>
                    </div>
                `).join('')}
            ` : ''}
        `;
    }
    
    updateDashboard() {
        // Update stats cards
        if (this.optimizationResults) {
            const currency = this.optimizationResults.currency === 'USD' ? '$' : '';
            const suffix = this.optimizationResults.currency === 'USD' ? '' : ' pts';
            
            document.getElementById('monthly-rewards').textContent = 
                `${currency}${this.optimizationResults.total_monthly_rewards}${suffix}`;
            document.getElementById('annual-rewards').textContent = 
                `${currency}${this.optimizationResults.total_annual_rewards}${suffix}`;
        }
        
        document.getElementById('active-cards').textContent = this.userCards.length;
        
        // Calculate optimization score (simplified)
        const score = this.calculateOptimizationScore();
        document.getElementById('optimization-score').textContent = score;
        
        // Update recommendations
        this.updateRecommendations();
    }
    
    calculateOptimizationScore() {
        if (!this.optimizationResults || this.userCards.length === 0) {
            return '--';
        }
        
        // Simplified scoring based on number of cards and optimization results
        const baseScore = Math.min(this.userCards.length * 20, 60);
        const rewardBonus = this.optimizationResults.total_monthly_rewards > 50 ? 25 : 15;
        const recBonus = this.optimizationResults.recommendations?.length > 0 ? 15 : 5;
        
        return Math.min(baseScore + rewardBonus + recBonus, 100);
    }
    
    updateRecommendations() {
        const container = document.getElementById('recommendations-list');
        
        if (!this.optimizationResults?.recommendations?.length) {
            if (this.userCards.length === 0) {
                container.innerHTML = `
                    <div class="recommendation low">
                        <div class="recommendation-title">Get Started</div>
                        <div class="recommendation-description">Add your first credit card to begin optimizing your rewards.</div>
                    </div>
                `;
            } else {
                container.innerHTML = `
                    <div class="recommendation medium">
                        <div class="recommendation-title">Optimize Your Spending</div>
                        <div class="recommendation-description">Enter your monthly spending amounts to get personalized recommendations.</div>
                    </div>
                `;
            }
            return;
        }
        
        container.innerHTML = this.optimizationResults.recommendations.map(rec => `
            <div class="recommendation ${rec.priority}">
                <div class="recommendation-title">${rec.title}</div>
                <div class="recommendation-description">${rec.description}</div>
            </div>
        `).join('');
    }
    
    async updateCardData() {
        try {
            this.showLoading(true);
            
            const response = await fetch('/api/scrape/update', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadAvailableCards();
                this.showSuccess('Card data updated successfully!');
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error updating card data:', error);
            this.showError('Failed to update card data');
        } finally {
            this.showLoading(false);
        }
    }
    
    formatCategoryName(category) {
        return category.replace(/_/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
    }
    
    showLoading(show) {
        if (show) {
            const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
            modal.show();
        } else {
            const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
            if (modal) {
                modal.hide();
            }
        }
    }
    
    showSuccess(message) {
        this.showAlert(message, 'success');
    }
    
    showError(message) {
        this.showAlert(message, 'danger');
    }
    
    showAlert(message, type) {
        // Remove existing alerts
        document.querySelectorAll('.alert-notification').forEach(alert => alert.remove());
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show alert-notification`;
        alert.style.position = 'fixed';
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '9999';
        alert.style.minWidth = '300px';
        
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.cardCompass = new CardCompass();
});
