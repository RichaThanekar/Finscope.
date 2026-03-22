"""
Flask API Backend for SIP Investment Recommendation System
WITH EXPANDED FUND DATABASE AND INFLATION DATA INTEGRATION
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================================================
# LOAD INFLATION DATA FROM EXCEL
# ============================================================================

def load_inflation_data(filepath='inflation_data.xlsx'):
    """
    Load inflation data from Excel file
    Expected columns: 'month', 'combined_inflation'
    """
    try:
        inflation_df = pd.read_excel(filepath)
        inflation_df.columns = inflation_df.columns.str.lower().str.strip()
        
        column_mapping = {
            'combined inflation': 'combined_inflation',
            'combined_inflation': 'combined_inflation',
            'inflation': 'combined_inflation'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in inflation_df.columns:
                inflation_df.rename(columns={old_col: new_col}, inplace=True)
        
        if 'month' in inflation_df.columns:
            inflation_df['month'] = pd.to_datetime(inflation_df['month'])
        
        inflation_df = inflation_df.sort_values('month', ascending=False)
        
        print(f"✓ Loaded {len(inflation_df)} inflation records")
        print(f"  Date range: {inflation_df['month'].min()} to {inflation_df['month'].max()}")
        print(f"  Latest inflation: {inflation_df.iloc[0]['combined_inflation']:.2f}%")
        
        return inflation_df
        
    except FileNotFoundError:
        print(f"⚠ Warning: {filepath} not found. Using default inflation value.")
        return None
    except Exception as e:
        print(f"⚠ Error loading inflation data: {e}")
        return None


def get_current_inflation(inflation_df):
    """Get the most recent inflation rate from the dataset"""
    if inflation_df is None or len(inflation_df) == 0:
        return 5.2
    return float(inflation_df.iloc[0]['combined_inflation'])


def get_historical_inflation_trend(inflation_df, months=6):
    """Get inflation trend for the last N months"""
    if inflation_df is None or len(inflation_df) == 0:
        return None
    
    recent_data = inflation_df.head(months)
    
    return {
        'average': float(recent_data['combined_inflation'].mean()),
        'min': float(recent_data['combined_inflation'].min()),
        'max': float(recent_data['combined_inflation'].max()),
        'current': float(recent_data.iloc[0]['combined_inflation']),
        'trend': 'increasing' if recent_data.iloc[0]['combined_inflation'] > recent_data['combined_inflation'].mean() else 'decreasing',
        'months_analyzed': len(recent_data)
    }

# ============================================================================
# INITIALIZE - LOAD MODELS AND INFLATION DATA
# ============================================================================

print("=" * 80)
print("INITIALIZING SIP RECOMMENDATION API")
print("=" * 80)

print("\n[1/2] Loading trained ML models...")
try:
    sip_model = joblib.load('sip_amount_model.pkl')
    allocation_model = joblib.load('allocation_model.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoders = joblib.load('label_encoders.pkl')
    print("✓ All ML models loaded successfully!")
except FileNotFoundError as e:
    print(f"⚠ Model files not found. Using rule-based system.")
    print(f"Error: {e}")
    sip_model = None
    allocation_model = None
    scaler = None
    label_encoders = None

print("\n[2/2] Loading inflation data from Excel...")
INFLATION_DATA = load_inflation_data('inflation_data.xlsx')

print("\n" + "=" * 80)
print("✅ INITIALIZATION COMPLETE")
print("=" * 80 + "\n")

# ============================================================================
# EXPANDED FUND DATABASE
# ============================================================================

FUND_DATABASE = {
    'equity': [
        # Large Cap Funds
        {
            'name': 'Parag Parikh Flexi Cap Fund',
            'category': 'Equity',
            'sub_category': 'Flexi Cap',
            'returns_1y': 18.5,
            'returns_3y': 15.2,
            'returns_5y': 17.8,
            'risk': 'High',
            'expense_ratio': 0.82,
            'min_sip': 1000,
            'fund_size': 45000
        },
        {
            'name': 'Axis Bluechip Fund',
            'category': 'Equity',
            'sub_category': 'Large Cap',
            'returns_1y': 16.2,
            'returns_3y': 13.8,
            'returns_5y': 15.4,
            'risk': 'High',
            'expense_ratio': 0.45,
            'min_sip': 500,
            'fund_size': 32000
        },
        {
            'name': 'HDFC Top 100 Fund',
            'category': 'Equity',
            'sub_category': 'Large Cap',
            'returns_1y': 15.8,
            'returns_3y': 13.2,
            'returns_5y': 14.9,
            'risk': 'High',
            'expense_ratio': 0.52,
            'min_sip': 500,
            'fund_size': 28000
        },
        {
            'name': 'ICICI Prudential Bluechip Fund',
            'category': 'Equity',
            'sub_category': 'Large Cap',
            'returns_1y': 16.5,
            'returns_3y': 14.1,
            'returns_5y': 15.8,
            'risk': 'High',
            'expense_ratio': 0.89,
            'min_sip': 100,
            'fund_size': 52000
        },
        {
            'name': 'Mirae Asset Large Cap Fund',
            'category': 'Equity',
            'sub_category': 'Large Cap',
            'returns_1y': 17.2,
            'returns_3y': 14.5,
            'returns_5y': 16.2,
            'risk': 'High',
            'expense_ratio': 0.48,
            'min_sip': 500,
            'fund_size': 38000
        },
        
        # Mid Cap Funds
        {
            'name': 'Kotak Emerging Equity Fund',
            'category': 'Equity',
            'sub_category': 'Mid Cap',
            'returns_1y': 22.4,
            'returns_3y': 19.6,
            'returns_5y': 21.2,
            'risk': 'Very High',
            'expense_ratio': 0.68,
            'min_sip': 1000,
            'fund_size': 18000
        },
        {
            'name': 'Axis Midcap Fund',
            'category': 'Equity',
            'sub_category': 'Mid Cap',
            'returns_1y': 24.8,
            'returns_3y': 21.2,
            'returns_5y': 22.5,
            'risk': 'Very High',
            'expense_ratio': 0.55,
            'min_sip': 500,
            'fund_size': 21000
        },
        {
            'name': 'Motilal Oswal Midcap Fund',
            'category': 'Equity',
            'sub_category': 'Mid Cap',
            'returns_1y': 26.5,
            'returns_3y': 23.8,
            'returns_5y': 24.2,
            'risk': 'Very High',
            'expense_ratio': 0.71,
            'min_sip': 500,
            'fund_size': 12000
        },
        {
            'name': 'DSP Midcap Fund',
            'category': 'Equity',
            'sub_category': 'Mid Cap',
            'returns_1y': 23.2,
            'returns_3y': 20.5,
            'returns_5y': 21.8,
            'risk': 'Very High',
            'expense_ratio': 0.62,
            'min_sip': 500,
            'fund_size': 16000
        },
        
        # Small Cap Funds
        {
            'name': 'Nippon India Small Cap Fund',
            'category': 'Equity',
            'sub_category': 'Small Cap',
            'returns_1y': 28.5,
            'returns_3y': 25.2,
            'returns_5y': 26.8,
            'risk': 'Very High',
            'expense_ratio': 0.88,
            'min_sip': 1000,
            'fund_size': 32000
        },
        {
            'name': 'Axis Small Cap Fund',
            'category': 'Equity',
            'sub_category': 'Small Cap',
            'returns_1y': 30.2,
            'returns_3y': 26.8,
            'returns_5y': 28.1,
            'risk': 'Very High',
            'expense_ratio': 0.65,
            'min_sip': 500,
            'fund_size': 15000
        },
        {
            'name': 'Quant Small Cap Fund',
            'category': 'Equity',
            'sub_category': 'Small Cap',
            'returns_1y': 32.5,
            'returns_3y': 28.5,
            'returns_5y': 29.8,
            'risk': 'Very High',
            'expense_ratio': 0.78,
            'min_sip': 1000,
            'fund_size': 8000
        },
        
        # Sector Funds
        {
            'name': 'ICICI Prudential Technology Fund',
            'category': 'Equity',
            'sub_category': 'Sectoral - Technology',
            'returns_1y': 25.8,
            'returns_3y': 22.5,
            'returns_5y': 24.2,
            'risk': 'Very High',
            'expense_ratio': 0.92,
            'min_sip': 500,
            'fund_size': 12000
        },
        {
            'name': 'SBI Banking & Financial Services Fund',
            'category': 'Equity',
            'sub_category': 'Sectoral - Banking',
            'returns_1y': 19.5,
            'returns_3y': 16.8,
            'returns_5y': 18.2,
            'risk': 'Very High',
            'expense_ratio': 0.68,
            'min_sip': 500,
            'fund_size': 9000
        },
        {
            'name': 'Nippon India Pharma Fund',
            'category': 'Equity',
            'sub_category': 'Sectoral - Pharma',
            'returns_1y': 21.2,
            'returns_3y': 18.5,
            'returns_5y': 19.8,
            'risk': 'Very High',
            'expense_ratio': 0.85,
            'min_sip': 1000,
            'fund_size': 7000
        },
    ],
    
    'debt': [
        # Corporate Bond Funds
        {
            'name': 'ICICI Prudential Corporate Bond Fund',
            'category': 'Debt',
            'sub_category': 'Corporate Bond',
            'returns_1y': 7.2,
            'returns_3y': 7.8,
            'returns_5y': 8.1,
            'risk': 'Low',
            'expense_ratio': 0.35,
            'min_sip': 1000,
            'fund_size': 42000
        },
        {
            'name': 'HDFC Corporate Bond Fund',
            'category': 'Debt',
            'sub_category': 'Corporate Bond',
            'returns_1y': 7.5,
            'returns_3y': 8.0,
            'returns_5y': 8.3,
            'risk': 'Low',
            'expense_ratio': 0.38,
            'min_sip': 500,
            'fund_size': 28000
        },
        {
            'name': 'Kotak Corporate Bond Fund',
            'category': 'Debt',
            'sub_category': 'Corporate Bond',
            'returns_1y': 7.3,
            'returns_3y': 7.9,
            'returns_5y': 8.2,
            'risk': 'Low',
            'expense_ratio': 0.32,
            'min_sip': 1000,
            'fund_size': 18000
        },
        
        # Banking & PSU Debt Funds
        {
            'name': 'Axis Banking & PSU Debt Fund',
            'category': 'Debt',
            'sub_category': 'Banking & PSU',
            'returns_1y': 7.5,
            'returns_3y': 8.0,
            'returns_5y': 8.3,
            'risk': 'Low',
            'expense_ratio': 0.28,
            'min_sip': 500,
            'fund_size': 35000
        },
        {
            'name': 'ICICI Prudential Banking & PSU Debt Fund',
            'category': 'Debt',
            'sub_category': 'Banking & PSU',
            'returns_1y': 7.4,
            'returns_3y': 7.9,
            'returns_5y': 8.2,
            'risk': 'Low',
            'expense_ratio': 0.31,
            'min_sip': 1000,
            'fund_size': 30000
        },
        {
            'name': 'SBI Banking & PSU Debt Fund',
            'category': 'Debt',
            'sub_category': 'Banking & PSU',
            'returns_1y': 7.6,
            'returns_3y': 8.1,
            'returns_5y': 8.4,
            'risk': 'Low',
            'expense_ratio': 0.29,
            'min_sip': 500,
            'fund_size': 22000
        },
        
        # Liquid Funds
        {
            'name': 'HDFC Liquid Fund',
            'category': 'Debt',
            'sub_category': 'Liquid',
            'returns_1y': 6.8,
            'returns_3y': 6.5,
            'returns_5y': 6.7,
            'risk': 'Very Low',
            'expense_ratio': 0.18,
            'min_sip': 5000,
            'fund_size': 48000
        },
        {
            'name': 'ICICI Prudential Liquid Fund',
            'category': 'Debt',
            'sub_category': 'Liquid',
            'returns_1y': 6.9,
            'returns_3y': 6.6,
            'returns_5y': 6.8,
            'risk': 'Very Low',
            'expense_ratio': 0.20,
            'min_sip': 5000,
            'fund_size': 42000
        },
        {
            'name': 'Axis Liquid Fund',
            'category': 'Debt',
            'sub_category': 'Liquid',
            'returns_1y': 6.7,
            'returns_3y': 6.4,
            'returns_5y': 6.6,
            'risk': 'Very Low',
            'expense_ratio': 0.19,
            'min_sip': 5000,
            'fund_size': 35000
        },
        
        # Short Duration Funds
        {
            'name': 'HDFC Short Term Debt Fund',
            'category': 'Debt',
            'sub_category': 'Short Duration',
            'returns_1y': 7.1,
            'returns_3y': 7.5,
            'returns_5y': 7.8,
            'risk': 'Low',
            'expense_ratio': 0.42,
            'min_sip': 1000,
            'fund_size': 25000
        },
        {
            'name': 'ICICI Prudential Short Term Fund',
            'category': 'Debt',
            'sub_category': 'Short Duration',
            'returns_1y': 7.2,
            'returns_3y': 7.6,
            'returns_5y': 7.9,
            'risk': 'Low',
            'expense_ratio': 0.45,
            'min_sip': 1000,
            'fund_size': 20000
        },
    ],
    
    'hybrid': [
        # Aggressive Hybrid Funds
        {
            'name': 'ICICI Prudential Equity & Debt Fund',
            'category': 'Hybrid',
            'sub_category': 'Aggressive Hybrid',
            'returns_1y': 14.5,
            'returns_3y': 12.8,
            'returns_5y': 13.5,
            'risk': 'Moderate',
            'expense_ratio': 0.95,
            'min_sip': 100,
            'fund_size': 38000
        },
        {
            'name': 'HDFC Hybrid Equity Fund',
            'category': 'Hybrid',
            'sub_category': 'Aggressive Hybrid',
            'returns_1y': 13.8,
            'returns_3y': 12.2,
            'returns_5y': 13.0,
            'risk': 'Moderate',
            'expense_ratio': 0.82,
            'min_sip': 500,
            'fund_size': 32000
        },
        {
            'name': 'SBI Equity Hybrid Fund',
            'category': 'Hybrid',
            'sub_category': 'Aggressive Hybrid',
            'returns_1y': 14.2,
            'returns_3y': 12.5,
            'returns_5y': 13.2,
            'risk': 'Moderate',
            'expense_ratio': 0.78,
            'min_sip': 500,
            'fund_size': 28000
        },
        
        # Balanced Hybrid Funds
        {
            'name': 'HDFC Balanced Advantage Fund',
            'category': 'Hybrid',
            'sub_category': 'Balanced Hybrid',
            'returns_1y': 12.5,
            'returns_3y': 11.2,
            'returns_5y': 11.8,
            'risk': 'Moderate',
            'expense_ratio': 0.68,
            'min_sip': 500,
            'fund_size': 45000
        },
        {
            'name': 'ICICI Prudential Balanced Advantage Fund',
            'category': 'Hybrid',
            'sub_category': 'Balanced Hybrid',
            'returns_1y': 12.8,
            'returns_3y': 11.5,
            'returns_5y': 12.0,
            'risk': 'Moderate',
            'expense_ratio': 0.72,
            'min_sip': 100,
            'fund_size': 40000
        },
        
        # Conservative Hybrid Funds
        {
            'name': 'HDFC Conservative Hybrid Fund',
            'category': 'Hybrid',
            'sub_category': 'Conservative Hybrid',
            'returns_1y': 9.5,
            'returns_3y': 9.2,
            'returns_5y': 9.8,
            'risk': 'Low to Moderate',
            'expense_ratio': 0.58,
            'min_sip': 1000,
            'fund_size': 18000
        },
        {
            'name': 'ICICI Prudential Regular Savings Fund',
            'category': 'Hybrid',
            'sub_category': 'Conservative Hybrid',
            'returns_1y': 9.2,
            'returns_3y': 8.9,
            'returns_5y': 9.5,
            'risk': 'Low to Moderate',
            'expense_ratio': 0.62,
            'min_sip': 1000,
            'fund_size': 15000
        },
    ]
}

# ============================================================================
# MARKET CONDITIONS (SIMULATED DATA - REPLACE WITH REAL API)
# ============================================================================

def get_market_conditions():
    """
    Get current market conditions
    In production, this should fetch real-time data from financial APIs
    """
    current_inflation = get_current_inflation(INFLATION_DATA)
    
    return {
        'inflation_rate': current_inflation,
        'repo_rate': 6.5,  # Current RBI repo rate
        'Nifty50_PE_ratio': 22.5,
        'GDP_growth_rate': 7.2,
        'market_volatility_index': 15.2,
        'bond_yield_10yr': 7.1
    }

# ============================================================================
# FUND RECOMMENDATION ENGINE
# ============================================================================

def recommend_funds(asset_allocation, risk_tolerance, sip_amount):
    """
    Recommend specific funds based on asset allocation and risk profile
    """
    recommendations = []
    
    # Equity funds
    if asset_allocation['equity'] > 0:
        equity_funds = FUND_DATABASE['equity'].copy()
        
        # Filter based on risk tolerance
        if risk_tolerance == 'low':
            equity_funds = [f for f in equity_funds if f['sub_category'] in ['Large Cap', 'Flexi Cap']]
        elif risk_tolerance == 'medium':
            equity_funds = [f for f in equity_funds if f['sub_category'] in ['Large Cap', 'Flexi Cap', 'Mid Cap']]
        # For high risk, include all equity funds
        
        # Sort by returns and pick top funds
        equity_funds = sorted(equity_funds, key=lambda x: x['returns_3y'], reverse=True)
        
        # Select 2-3 equity funds
        num_equity_funds = min(3, len(equity_funds))
        selected_equity = equity_funds[:num_equity_funds]
        
        equity_allocation_per_fund = asset_allocation['equity'] / num_equity_funds
        
        for fund in selected_equity:
            fund_copy = fund.copy()
            fund_copy['allocation_percentage'] = round(equity_allocation_per_fund, 2)
            fund_copy['monthly_investment'] = round(sip_amount * equity_allocation_per_fund / 100)
            recommendations.append(fund_copy)
    
    # Debt funds
    if asset_allocation['debt'] > 0:
        debt_funds = FUND_DATABASE['debt'].copy()
        
        # Sort by returns
        debt_funds = sorted(debt_funds, key=lambda x: x['returns_3y'], reverse=True)
        
        # Select 1-2 debt funds
        num_debt_funds = min(2, len(debt_funds))
        selected_debt = debt_funds[:num_debt_funds]
        
        debt_allocation_per_fund = asset_allocation['debt'] / num_debt_funds
        
        for fund in selected_debt:
            fund_copy = fund.copy()
            fund_copy['allocation_percentage'] = round(debt_allocation_per_fund, 2)
            fund_copy['monthly_investment'] = round(sip_amount * debt_allocation_per_fund / 100)
            recommendations.append(fund_copy)
    
    # Hybrid funds
    if asset_allocation['hybrid'] > 0:
        hybrid_funds = FUND_DATABASE['hybrid'].copy()
        
        # Filter based on risk tolerance
        if risk_tolerance == 'low':
            hybrid_funds = [f for f in hybrid_funds if 'Conservative' in f['sub_category']]
        elif risk_tolerance == 'medium':
            hybrid_funds = [f for f in hybrid_funds if 'Balanced' in f['sub_category'] or 'Conservative' in f['sub_category']]
        # For high risk, prefer aggressive hybrid
        
        # Sort by returns
        hybrid_funds = sorted(hybrid_funds, key=lambda x: x['returns_3y'], reverse=True)
        
        # Select 1-2 hybrid funds
        num_hybrid_funds = min(2, len(hybrid_funds))
        selected_hybrid = hybrid_funds[:num_hybrid_funds]
        
        hybrid_allocation_per_fund = asset_allocation['hybrid'] / num_hybrid_funds
        
        for fund in selected_hybrid:
            fund_copy = fund.copy()
            fund_copy['allocation_percentage'] = round(hybrid_allocation_per_fund, 2)
            fund_copy['monthly_investment'] = round(sip_amount * hybrid_allocation_per_fund / 100)
            recommendations.append(fund_copy)
    
    return recommendations

# ============================================================================
# INSIGHTS GENERATION
# ============================================================================

def generate_insights(user_data, sip_amount, asset_allocation, projections):
    """
    Generate personalized insights based on user profile and recommendations
    """
    insights = []
    
    # Calculate financial metrics
    disposable_income = user_data['monthly_income'] - user_data['monthly_expenses'] - user_data['existing_EMIs']
    investment_ratio = (sip_amount / disposable_income * 100) if disposable_income > 0 else 0
    
    # Insight 1: Investment capacity
    if investment_ratio > 80:
        insights.append({
            'type': 'warning',
            'message': f'Your recommended SIP is {investment_ratio:.0f}% of your disposable income. Consider reviewing your expenses or increasing your income sources.'
        })
    elif investment_ratio > 50:
        insights.append({
            'type': 'positive',
            'message': f'Great commitment! You\'re investing {investment_ratio:.0f}% of your disposable income. This disciplined approach will help you reach your goals faster.'
        })
    else:
        insights.append({
            'type': 'tip',
            'message': f'You\'re investing {investment_ratio:.0f}% of your disposable income. Consider gradually increasing your SIP amount to accelerate wealth creation.'
        })
    
    # Insight 2: Time horizon
    years = user_data['goal_duration_years']
    if years < 3:
        insights.append({
            'type': 'warning',
            'message': f'Your goal timeline is only {years} years. Consider a higher allocation to debt funds to reduce volatility risk.'
        })
    elif years >= 10:
        insights.append({
            'type': 'positive',
            'message': f'With {years} years to invest, you have excellent time to benefit from equity market growth and ride out volatility.'
        })
    
    # Insight 3: Goal achievement
    if projections and projections['goal_achievement'] < 80:
        shortfall = user_data['goal_amount'] - projections['future_value']
        insights.append({
            'type': 'warning',
            'message': f'Current projections suggest you may fall short of your goal by ₹{shortfall:,.0f}. Consider increasing your SIP or extending your timeline.'
        })
    elif projections and projections['goal_achievement'] >= 100:
        insights.append({
            'type': 'positive',
            'message': f'Excellent! You\'re projected to exceed your goal. You could consider additional financial goals or early retirement planning.'
        })
    
    # Insight 4: Risk profile alignment
    age = user_data['age']
    risk_tolerance = user_data['risk_tolerance']
    
    if age < 35 and risk_tolerance == 'low':
        insights.append({
            'type': 'tip',
            'message': 'At your age, you could potentially take on more risk in equities for higher long-term returns. Consider gradually increasing equity exposure.'
        })
    elif age > 50 and risk_tolerance == 'high':
        insights.append({
            'type': 'info',
            'message': 'As you approach retirement age, consider gradually shifting towards more stable debt investments to protect your wealth.'
        })
    
    # Insight 5: Emergency fund
    emergency_fund_needed = user_data['monthly_expenses'] * 6
    if user_data['current_savings'] < emergency_fund_needed:
        insights.append({
            'type': 'warning',
            'message': f'Build an emergency fund of ₹{emergency_fund_needed:,.0f} (6 months of expenses) before aggressive investing. Current savings: ₹{user_data["current_savings"]:,.0f}.'
        })
    
    # Insight 6: Inflation impact
    inflation_rate = get_current_inflation(INFLATION_DATA)
    if inflation_rate > 6:
        insights.append({
            'type': 'info',
            'message': f'Current inflation is {inflation_rate:.1f}%. Your investments need to generate returns above this rate to build real wealth.'
        })
    
    return insights

# ============================================================================
# CALCULATE PROJECTIONS
# ============================================================================

def calculate_projections(sip_amount, duration_years, asset_allocation, goal_amount):
    """
    Calculate future value and projections based on historical returns
    """
    # Expected returns based on asset allocation
    equity_return = 12.0  # Historical average
    debt_return = 7.5     # Historical average
    hybrid_return = 9.5   # Historical average
    
    expected_return = (
        (asset_allocation['equity'] / 100 * equity_return) +
        (asset_allocation['debt'] / 100 * debt_return) +
        (asset_allocation['hybrid'] / 100 * hybrid_return)
    )
    
    # Convert annual return to monthly
    monthly_return = expected_return / 12 / 100
    
    # Calculate future value using SIP formula
    months = duration_years * 12
    future_value = sip_amount * (((1 + monthly_return) ** months - 1) / monthly_return) * (1 + monthly_return)
    
    total_investment = sip_amount * months
    wealth_gain = future_value - total_investment
    goal_achievement = (future_value / goal_amount * 100) if goal_amount > 0 else 0
    
    return {
        'total_investment': int(total_investment),
        'future_value': int(future_value),
        'wealth_gain': int(wealth_gain),
        'expected_return_rate': round(expected_return, 2),
        'goal_achievement': round(goal_achievement, 2)
    }

# ============================================================================
# RULE-BASED SIP CALCULATION (FALLBACK IF NO MODEL)
# ============================================================================

def calculate_sip_rule_based(user_data):
    """
    Rule-based SIP amount calculation if ML model is not available
    """
    # Calculate disposable income
    disposable_income = user_data['monthly_income'] - user_data['monthly_expenses'] - user_data['existing_EMIs']
    
    # Base SIP calculation
    if user_data['risk_tolerance'] == 'high':
        base_percentage = 0.40  # 40% of disposable income
    elif user_data['risk_tolerance'] == 'medium':
        base_percentage = 0.30  # 30% of disposable income
    else:
        base_percentage = 0.20  # 20% of disposable income
    
    sip_amount = disposable_income * base_percentage
    
    # Adjust based on age (younger = more aggressive)
    age = user_data['age']
    if age < 30:
        sip_amount *= 1.2
    elif age > 50:
        sip_amount *= 0.8
    
    # Adjust based on goal duration
    if user_data['goal_duration_years'] < 5:
        sip_amount *= 1.3
    elif user_data['goal_duration_years'] > 15:
        sip_amount *= 0.9
    
    # Ensure minimum SIP
    sip_amount = max(500, sip_amount)
    
    # Round to nearest 100
    sip_amount = round(sip_amount / 100) * 100
    
    return int(sip_amount)


def calculate_asset_allocation_rule_based(user_data):
    """
    Rule-based asset allocation if ML model is not available
    """
    age = user_data['age']
    risk_tolerance = user_data['risk_tolerance']
    duration = user_data['goal_duration_years']
    
    # Base allocation on age (100 - age rule for equity)
    equity_base = max(20, min(80, 100 - age))
    
    # Adjust for risk tolerance
    if risk_tolerance == 'high':
        equity_base += 15
    elif risk_tolerance == 'low':
        equity_base -= 15
    
    # Adjust for duration
    if duration < 3:
        equity_base -= 20
    elif duration > 15:
        equity_base += 10
    
    # Ensure bounds
    equity = max(20, min(80, equity_base))
    
    # Distribute remaining between debt and hybrid
    remaining = 100 - equity
    
    if risk_tolerance == 'low':
        debt = int(remaining * 0.7)
        hybrid = remaining - debt
    elif risk_tolerance == 'high':
        hybrid = int(remaining * 0.6)
        debt = remaining - hybrid
    else:
        debt = int(remaining * 0.5)
        hybrid = remaining - debt
    
    return {
        'equity': equity,
        'debt': debt,
        'hybrid': hybrid
    }

# ============================================================================
# MAIN PREDICTION ENDPOINT
# ============================================================================

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Main endpoint for SIP recommendations
    """
    try:
        # Get user data from request
        user_data = request.json
        
        # Validate required fields
        required_fields = [
            'age', 'monthly_income', 'monthly_expenses', 'existing_EMIs',
            'current_savings', 'current_investments_value', 'goal_type',
            'goal_amount', 'goal_duration_years', 'risk_tolerance'
        ]
        
        for field in required_fields:
            if field not in user_data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Get market conditions
        market_conditions = get_market_conditions()
        
        # Calculate SIP amount
        if sip_model is not None:
            # Use ML model if available
            try:
                # Prepare features for model
                features = pd.DataFrame([{
                    'age': user_data['age'],
                    'monthly_income': user_data['monthly_income'],
                    'monthly_expenses': user_data['monthly_expenses'],
                    'existing_EMIs': user_data['existing_EMIs'],
                    'current_savings': user_data['current_savings'],
                    'current_investments_value': user_data['current_investments_value'],
                    'goal_amount': user_data['goal_amount'],
                    'goal_duration_years': user_data['goal_duration_years'],
                    'goal_type': user_data['goal_type'],
                    'risk_tolerance': user_data['risk_tolerance'],
                    'inflation_rate': market_conditions['inflation_rate']
                }])
                
                # Encode categorical variables
                for col in ['goal_type', 'risk_tolerance']:
                    if col in label_encoders:
                        features[col] = label_encoders[col].transform(features[col])
                
                # Scale features
                features_scaled = scaler.transform(features)
                
                # Predict SIP amount
                sip_amount = int(sip_model.predict(features_scaled)[0])
                
                # Predict asset allocation
                allocation_pred = allocation_model.predict(features_scaled)[0]
                asset_allocation = {
                    'equity': int(allocation_pred[0]),
                    'debt': int(allocation_pred[1]),
                    'hybrid': int(allocation_pred[2])
                }
            except Exception as e:
                print(f"Model prediction failed: {e}. Using rule-based approach.")
                sip_amount = calculate_sip_rule_based(user_data)
                asset_allocation = calculate_asset_allocation_rule_based(user_data)
        else:
            # Use rule-based approach
            sip_amount = calculate_sip_rule_based(user_data)
            asset_allocation = calculate_asset_allocation_rule_based(user_data)
        
        # Calculate projections
        projections = calculate_projections(
            sip_amount,
            user_data['goal_duration_years'],
            asset_allocation,
            user_data['goal_amount']
        )
        
        # Get fund recommendations
        fund_recommendations = recommend_funds(
            asset_allocation,
            user_data['risk_tolerance'],
            sip_amount
        )
        
        # Generate insights
        insights = generate_insights(
            user_data,
            sip_amount,
            asset_allocation,
            projections
        )
        
        # Get inflation context
        inflation_context = get_historical_inflation_trend(INFLATION_DATA)
        
        # Prepare response
        response = {
            'success': True,
            'data': {
                'recommended_SIP_amount': sip_amount,
                'asset_allocation': asset_allocation,
                'fund_recommendations': fund_recommendations,
                'projections': projections,
                'insights': insights,
                'market_conditions': market_conditions,
                'inflation_context': inflation_context,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error in prediction endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'success': True,
        'status': 'API is running',
        'models_loaded': sip_model is not None,
        'inflation_data_loaded': INFLATION_DATA is not None,
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================================================
# GET AVAILABLE FUNDS ENDPOINT
# ============================================================================

@app.route('/api/funds', methods=['GET'])
def get_funds():
    """
    Get all available funds in the database
    """
    try:
        category = request.args.get('category', None)
        
        if category and category.lower() in FUND_DATABASE:
            funds = FUND_DATABASE[category.lower()]
        else:
            # Return all funds
            funds = []
            for cat_funds in FUND_DATABASE.values():
                funds.extend(cat_funds)
        
        return jsonify({
            'success': True,
            'count': len(funds),
            'funds': funds
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# GET MARKET CONDITIONS ENDPOINT
# ============================================================================

@app.route('/api/market', methods=['GET'])
def get_market():
    """
    Get current market conditions
    """
    try:
        market_conditions = get_market_conditions()
        inflation_context = get_historical_inflation_trend(INFLATION_DATA)
        
        return jsonify({
            'success': True,
            'data': {
                'market_conditions': market_conditions,
                'inflation_context': inflation_context,
                'timestamp': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# RUN THE APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🚀 STARTING FLASK API SERVER")
    print("=" * 80)
    print(f"📡 API will be available at: http://127.0.0.1:5001")
    print(f"📊 ML Models: {'✅ Loaded' if sip_model else '⚠️  Using Rule-Based System'}")
    print(f"📈 Inflation Data: {'✅ Loaded' if INFLATION_DATA is not None else '⚠️  Using Default Values'}")
    print(f"💼 Funds Database: {sum(len(funds) for funds in FUND_DATABASE.values())} funds available")
    print("=" * 80 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5001)

# """
# Flask API Backend for SIP Investment Recommendation System
# WITH INFLATION DATA INTEGRATION FROM EXCEL
# """

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import pandas as pd
# import numpy as np
# import os
# from datetime import datetime

# app = Flask(__name__)
# CORS(app)

# # ============================================================================
# # LOAD INFLATION DATA FROM EXCEL
# # ============================================================================

# def load_inflation_data(filepath='inflation_data.xlsx'):
#     """
#     Load inflation data from Excel file
#     Expected columns: 'month', 'combined_inflation'
#     """
#     try:
#         # Read Excel file
#         inflation_df = pd.read_excel(filepath)
        
#         # Standardize column names (handle different naming conventions)
#         inflation_df.columns = inflation_df.columns.str.lower().str.strip()
        
#         # Rename columns to expected format
#         column_mapping = {
#             'combined inflation': 'combined_inflation',
#             'combined_inflation': 'combined_inflation',
#             'inflation': 'combined_inflation'
#         }
        
#         for old_col, new_col in column_mapping.items():
#             if old_col in inflation_df.columns:
#                 inflation_df.rename(columns={old_col: new_col}, inplace=True)
        
#         # Convert month column to datetime if it's not already
#         if 'month' in inflation_df.columns:
#             inflation_df['month'] = pd.to_datetime(inflation_df['month'])
        
#         # Sort by date
#         inflation_df = inflation_df.sort_values('month', ascending=False)
        
#         print(f"✓ Loaded {len(inflation_df)} inflation records")
#         print(f"  Date range: {inflation_df['month'].min()} to {inflation_df['month'].max()}")
#         print(f"  Latest inflation: {inflation_df.iloc[0]['combined_inflation']:.2f}%")
        
#         return inflation_df
        
#     except FileNotFoundError:
#         print(f"⚠ Warning: {filepath} not found. Using default inflation value.")
#         return None
#     except Exception as e:
#         print(f"⚠ Error loading inflation data: {e}")
#         return None


# def get_current_inflation(inflation_df):
#     """
#     Get the most recent inflation rate from the dataset
#     """
#     if inflation_df is None or len(inflation_df) == 0:
#         return 5.2  # Default fallback value
    
#     # Return the most recent inflation value
#     return float(inflation_df.iloc[0]['combined_inflation'])


# def get_historical_inflation_trend(inflation_df, months=12):
#     """
#     Get inflation trend for the last N months
#     """
#     if inflation_df is None or len(inflation_df) == 0:
#         return None
    
#     recent_data = inflation_df.head(months)
    
#     return {
#         'average': float(recent_data['combined_inflation'].mean()),
#         'min': float(recent_data['combined_inflation'].min()),
#         'max': float(recent_data['combined_inflation'].max()),
#         'current': float(recent_data.iloc[0]['combined_inflation']),
#         'trend': 'increasing' if recent_data.iloc[0]['combined_inflation'] > recent_data['combined_inflation'].mean() else 'decreasing',
#         'months_analyzed': len(recent_data)
#     }


# def get_inflation_by_date(inflation_df, target_date=None):
#     """
#     Get inflation for a specific date or the closest available date
#     """
#     if inflation_df is None or len(inflation_df) == 0:
#         return 5.2
    
#     if target_date is None:
#         return get_current_inflation(inflation_df)
    
#     target_date = pd.to_datetime(target_date)
    
#     # Find the closest date
#     inflation_df['date_diff'] = abs(inflation_df['month'] - target_date)
#     closest = inflation_df.loc[inflation_df['date_diff'].idxmin()]
    
#     return float(closest['combined_inflation'])


# # ============================================================================
# # INITIALIZE - LOAD MODELS AND INFLATION DATA
# # ============================================================================

# print("=" * 80)
# print("INITIALIZING SIP RECOMMENDATION API")
# print("=" * 80)

# # Load ML Models
# print("\n[1/2] Loading trained ML models...")
# try:
#     sip_model = joblib.load('sip_amount_model.pkl')
#     allocation_model = joblib.load('allocation_model.pkl')
#     scaler = joblib.load('scaler.pkl')
#     label_encoders = joblib.load('label_encoders.pkl')
#     print("✓ All ML models loaded successfully!")
# except FileNotFoundError as e:
#     print(f"⚠ Model files not found. Please run the training script first.")
#     print(f"Error: {e}")

# # Load Inflation Data
# print("\n[2/2] Loading inflation data from Excel...")
# INFLATION_DATA = load_inflation_data('inflation_data.xlsx')  # Update path as needed

# print("\n" + "=" * 80)
# print("✅ INITIALIZATION COMPLETE")
# print("=" * 80 + "\n")

# # ============================================================================
# # FUND DATABASE
# # ============================================================================

# FUND_DATABASE = {
#     'equity': [
#         {
#             'name': 'Parag Parikh Flexi Cap Fund',
#             'category': 'Equity',
#             'sub_category': 'Flexi Cap',
#             'returns_1y': 18.5,
#             'returns_3y': 15.2,
#             'returns_5y': 17.8,
#             'risk': 'High',
#             'expense_ratio': 0.82,
#             'min_sip': 1000
#         },
#         {
#             'name': 'Axis Bluechip Fund',
#             'category': 'Equity',
#             'sub_category': 'Large Cap',
#             'returns_1y': 16.2,
#             'returns_3y': 13.8,
#             'returns_5y': 15.4,
#             'risk': 'High',
#             'expense_ratio': 0.45,
#             'min_sip': 500
#         },
#         {
#             'name': 'Kotak Emerging Equity Fund',
#             'category': 'Equity',
#             'sub_category': 'Mid Cap',
#             'returns_1y': 22.4,
#             'returns_3y': 19.6,
#             'returns_5y': 21.2,
#             'risk': 'Very High',
#             'expense_ratio': 0.68,
#             'min_sip': 1000
#         },
#         {
#             'name': 'HDFC Top 100 Fund',
#             'category': 'Equity',
#             'sub_category': 'Large Cap',
#             'returns_1y': 15.8,
#             'returns_3y': 13.2,
#             'returns_5y': 14.9,
#             'risk': 'High',
#             'expense_ratio': 0.52,
#             'min_sip': 500
#         }
#     ],
#     'debt': [
#         {
#             'name': 'ICICI Prudential Corporate Bond Fund',
#             'category': 'Debt',
#             'sub_category': 'Corporate Bond',
#             'returns_1y': 7.2,
#             'returns_3y': 7.8,
#             'returns_5y': 8.1,
#             'risk': 'Low',
#             'expense_ratio': 0.35,
#             'min_sip': 1000
#         },
#         {
#             'name': 'Axis Banking & PSU Debt Fund',
#             'category': 'Debt',
#             'sub_category': 'Banking & PSU',
#             'returns_1y': 7.5,
#             'returns_3y': 8.0,
#             'returns_5y': 8.3,
#             'risk': 'Low',
#             'expense_ratio': 0.28,
#             'min_sip': 500
#         },
#         {
#             'name': 'SBI Magnum Gilt Fund',
#             'category': 'Debt',
#             'sub_category': 'Gilt',
#             'returns_1y': 6.8,
#             'returns_3y': 7.2,
#             'returns_5y': 7.8,
#             'risk': 'Low',
#             'expense_ratio': 0.42,
#             'min_sip': 500
#         }
#     ],
#     'hybrid': [
#         {
#             'name': 'HDFC Balanced Advantage Fund',
#             'category': 'Hybrid',
#             'sub_category': 'Dynamic Asset Allocation',
#             'returns_1y': 12.8,
#             'returns_3y': 11.5,
#             'returns_5y': 12.9,
#             'risk': 'Medium',
#             'expense_ratio': 0.88,
#             'min_sip': 1000
#         },
#         {
#             'name': 'ICICI Prudential Equity & Debt Fund',
#             'category': 'Hybrid',
#             'sub_category': 'Aggressive Hybrid',
#             'returns_1y': 14.2,
#             'returns_3y': 12.8,
#             'returns_5y': 13.5,
#             'risk': 'Medium',
#             'expense_ratio': 0.95,
#             'min_sip': 500
#         },
#         {
#             'name': 'Mirae Asset Hybrid Equity Fund',
#             'category': 'Hybrid',
#             'sub_category': 'Aggressive Hybrid',
#             'returns_1y': 15.1,
#             'returns_3y': 13.2,
#             'returns_5y': 14.8,
#             'risk': 'Medium',
#             'expense_ratio': 0.72,
#             'min_sip': 1000
#         }
#     ]
# }

# # ============================================================================
# # HELPER FUNCTIONS
# # ============================================================================

# def get_market_data():
#     """
#     Get current market data including real-time inflation from Excel
#     """
#     # Get current inflation from loaded data
#     current_inflation = get_current_inflation(INFLATION_DATA)
    
#     return {
#         'inflation_rate': current_inflation,  # 🔥 REAL INFLATION FROM EXCEL
#         'repo_rate': 6.5,
#         'Nifty50_PE_ratio': 22.5,
#         'market_volatility_index': 15.3,
#         'GDP_growth_rate': 6.7,
#         'average_fund_return_3y': 12.5,
#         'fund_risk_score': 6.2,
#         'FD_interest_rate': 7.0
#     }


# def select_funds(equity_pct, debt_pct, hybrid_pct, risk_tolerance):
#     """Select best funds based on allocation and risk tolerance"""
#     recommendations = []
    
#     if equity_pct > 0:
#         equity_funds = FUND_DATABASE['equity']
#         if risk_tolerance == 'high':
#             selected = equity_funds[2]
#         else:
#             selected = equity_funds[0]
        
#         recommendations.append({
#             **selected,
#             'allocation_percentage': round(equity_pct, 1)
#         })
    
#     if debt_pct > 0:
#         debt_funds = FUND_DATABASE['debt']
#         selected = debt_funds[0]
        
#         recommendations.append({
#             **selected,
#             'allocation_percentage': round(debt_pct, 1)
#         })
    
#     if hybrid_pct > 0:
#         hybrid_funds = FUND_DATABASE['hybrid']
#         if risk_tolerance == 'high':
#             selected = hybrid_funds[2]
#         else:
#             selected = hybrid_funds[0]
        
#         recommendations.append({
#             **selected,
#             'allocation_percentage': round(hybrid_pct, 1)
#         })
    
#     return recommendations


# def calculate_projections(sip_amount, equity_pct, debt_pct, hybrid_pct, duration_years, goal_amount):
#     """Calculate investment projections"""
#     equity_return = 0.14
#     debt_return = 0.075
#     hybrid_return = 0.115
    
#     weighted_return = (
#         (equity_pct / 100) * equity_return +
#         (debt_pct / 100) * debt_return +
#         (hybrid_pct / 100) * hybrid_return
#     )
    
#     r = weighted_return / 12
#     n = duration_years * 12
    
#     if r > 0:
#         future_value = sip_amount * ((np.power(1 + r, n) - 1) / r)
#     else:
#         future_value = sip_amount * n
    
#     total_investment = sip_amount * n
    
#     return {
#         'total_investment': int(total_investment),
#         'future_value': int(future_value),
#         'expected_returns': round(weighted_return * 100, 2),
#         'goal_achievement': min(100, round((future_value / goal_amount) * 100, 1)) if goal_amount > 0 else 100,
#         'wealth_gain': int(future_value - total_investment)
#     }


# # ============================================================================
# # API ENDPOINTS
# # ============================================================================

# @app.route('/', methods=['GET'])
# def home():
#     """Health check endpoint"""
#     current_inflation = get_current_inflation(INFLATION_DATA)
    
#     return jsonify({
#         'status': 'active',
#         'message': 'SIP Investment Recommendation API with Real-time Inflation Data',
#         'version': '2.0.0',
#         'current_inflation': current_inflation,
#         'inflation_data_loaded': INFLATION_DATA is not None,
#         'endpoints': {
#             'predict': '/api/predict (POST)',
#             'market_data': '/api/market-data (GET)',
#             'inflation_info': '/api/inflation-info (GET)',
#             'inflation_trend': '/api/inflation-trend (GET)',
#             'funds': '/api/funds (GET)'
#         }
#     })


# @app.route('/api/inflation-info', methods=['GET'])
# def get_inflation_info():
#     """
#     Get current inflation information
#     """
#     if INFLATION_DATA is None:
#         return jsonify({
#             'success': False,
#             'error': 'Inflation data not loaded'
#         }), 404
    
#     current_inflation = get_current_inflation(INFLATION_DATA)
#     latest_record = INFLATION_DATA.iloc[0]
    
#     return jsonify({
#         'success': True,
#         'data': {
#             'current_inflation': current_inflation,
#             'as_of_date': latest_record['month'].strftime('%Y-%m-%d'),
#             'total_records': len(INFLATION_DATA),
#             'data_range': {
#                 'from': INFLATION_DATA['month'].min().strftime('%Y-%m-%d'),
#                 'to': INFLATION_DATA['month'].max().strftime('%Y-%m-%d')
#             }
#         }
#     })


# @app.route('/api/inflation-trend', methods=['GET'])
# def get_inflation_trend_endpoint():
#     """
#     Get inflation trend analysis
#     Query params: months (default: 12)
#     """
#     if INFLATION_DATA is None:
#         return jsonify({
#             'success': False,
#             'error': 'Inflation data not loaded'
#         }), 404
    
#     months = request.args.get('months', default=12, type=int)
#     months = min(max(1, months), len(INFLATION_DATA))  # Validate range
    
#     trend_data = get_historical_inflation_trend(INFLATION_DATA, months)
    
#     # Get monthly data for charting
#     recent_data = INFLATION_DATA.head(months)
#     monthly_values = [
#         {
#             'month': row['month'].strftime('%Y-%m'),
#             'inflation': float(row['combined_inflation'])
#         }
#         for _, row in recent_data.iterrows()
#     ]
#     monthly_values.reverse()  # Chronological order
    
#     return jsonify({
#         'success': True,
#         'data': {
#             'summary': trend_data,
#             'monthly_data': monthly_values
#         }
#     })


# @app.route('/api/market-data', methods=['GET'])
# def get_market_info():
#     """Get current market indicators with real inflation"""
#     market_data = get_market_data()
    
#     # Add inflation trend if available
#     inflation_trend = None
#     if INFLATION_DATA is not None:
#         inflation_trend = get_historical_inflation_trend(INFLATION_DATA, 6)
    
#     return jsonify({
#         'success': True,
#         'data': market_data,
#         'inflation_trend': inflation_trend,
#         'timestamp': pd.Timestamp.now().isoformat()
#     })


# @app.route('/api/funds', methods=['GET'])
# def get_funds():
#     """Get all available funds"""
#     category = request.args.get('category', 'all')
    
#     if category == 'all':
#         funds = {
#             'equity': FUND_DATABASE['equity'],
#             'debt': FUND_DATABASE['debt'],
#             'hybrid': FUND_DATABASE['hybrid']
#         }
#     elif category in FUND_DATABASE:
#         funds = FUND_DATABASE[category]
#     else:
#         return jsonify({
#             'success': False,
#             'error': 'Invalid category. Use: equity, debt, hybrid, or all'
#         }), 400
    
#     return jsonify({
#         'success': True,
#         'data': funds
#     })


# @app.route('/api/predict', methods=['POST'])
# def predict():
#     """
#     Main prediction endpoint with real-time inflation integration
#     """
#     try:
#         data = request.get_json()
        
#         required_fields = [
#             'age', 'monthly_income', 'monthly_expenses', 'existing_EMIs',
#             'current_savings', 'current_investments_value', 'goal_type',
#             'goal_amount', 'goal_duration_years', 'risk_tolerance',
#             'investment_experience', 'need_for_liquidity'
#         ]
        
#         missing_fields = [field for field in required_fields if field not in data]
#         if missing_fields:
#             return jsonify({
#                 'success': False,
#                 'error': f'Missing required fields: {", ".join(missing_fields)}'
#             }), 400
        
#         # Get market data with REAL INFLATION from Excel
#         market_data = get_market_data()
#         user_input = {**data, **market_data}
        
#         # Prepare features
#         feature_cols = [
#             'age', 'monthly_income', 'monthly_expenses', 'existing_EMIs',
#             'current_savings', 'current_investments_value', 'goal_amount',
#             'goal_duration_years', 'need_for_liquidity', 'inflation_rate',
#             'repo_rate', 'Nifty50_PE_ratio', 'market_volatility_index',
#             'GDP_growth_rate', 'average_fund_return_3y', 'fund_risk_score',
#             'FD_interest_rate', 'goal_type', 'risk_tolerance', 'investment_experience'
#         ]
        
#         input_df = pd.DataFrame([{k: user_input[k] for k in feature_cols}])
        
#         # Encode categorical variables
#         for col, le in label_encoders.items():
#             if col in input_df.columns:
#                 try:
#                     input_df[col] = le.transform([input_df[col].values[0]])[0]
#                 except ValueError:
#                     input_df[col] = 0
        
#         # Scale and predict
#         input_scaled = scaler.transform(input_df)
#         sip_amount = sip_model.predict(input_scaled)[0]
#         allocations = allocation_model.predict(input_scaled)[0]
        
#         # Process predictions
#         sip_amount = int(round(sip_amount, -2))
#         equity_pct = max(0, min(100, round(allocations[0], 1)))
#         debt_pct = max(0, min(100, round(allocations[1], 1)))
#         hybrid_pct = max(0, min(100, round(allocations[2], 1)))
        
#         # Normalize allocations
#         total = equity_pct + debt_pct + hybrid_pct
#         if total > 0:
#             equity_pct = round((equity_pct / total) * 100, 1)
#             debt_pct = round((debt_pct / total) * 100, 1)
#             hybrid_pct = 100 - equity_pct - debt_pct
        
#         # Get recommendations
#         fund_recommendations = select_funds(
#             equity_pct, debt_pct, hybrid_pct, data['risk_tolerance']
#         )
        
#         # Calculate projections
#         projections = calculate_projections(
#             sip_amount, equity_pct, debt_pct, hybrid_pct,
#             data['goal_duration_years'], data['goal_amount']
#         )
        
#         # Get inflation context
#         inflation_context = None
#         if INFLATION_DATA is not None:
#             inflation_context = get_historical_inflation_trend(INFLATION_DATA, 6)
        
#         # Generate response
#         response = {
#             'success': True,
#             'data': {
#                 'recommended_SIP_amount': sip_amount,
#                 'asset_allocation': {
#                     'equity': equity_pct,
#                     'debt': debt_pct,
#                     'hybrid': hybrid_pct
#                 },
#                 'fund_recommendations': fund_recommendations,
#                 'projections': projections,
#                 'market_conditions': market_data,
#                 'inflation_context': inflation_context,
#                 'insights': generate_insights(
#                     sip_amount, equity_pct, data['monthly_income'],
#                     data['risk_tolerance'], projections['goal_achievement'],
#                     market_data['inflation_rate']
#                 )
#             },
#             'timestamp': pd.Timestamp.now().isoformat()
#         }
        
#         return jsonify(response)
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500


# def generate_insights(sip_amount, equity_pct, monthly_income, risk_tolerance, goal_achievement, inflation_rate):
#     """Generate personalized insights with inflation consideration"""
#     insights = []
    
#     # SIP affordability
#     sip_to_income_ratio = (sip_amount / monthly_income) * 100
#     if sip_to_income_ratio < 10:
#         insights.append({
#             'type': 'positive',
#             'message': f'Your SIP is {sip_to_income_ratio:.1f}% of income, leaving room for emergencies.'
#         })
#     elif sip_to_income_ratio > 30:
#         insights.append({
#             'type': 'warning',
#             'message': f'Your SIP is {sip_to_income_ratio:.1f}% of income. Consider optimizing expenses.'
#         })
    
#     # Inflation impact warning
#     if inflation_rate > 6.5:
#         insights.append({
#             'type': 'warning',
#             'message': f'Current inflation at {inflation_rate:.1f}% is high. Your investments should beat inflation for real wealth growth.'
#         })
#     elif inflation_rate > 5.5:
#         insights.append({
#             'type': 'info',
#             'message': f'Inflation at {inflation_rate:.1f}% - ensure returns exceed this to maintain purchasing power.'
#         })
    
#     # Equity allocation
#     if equity_pct > 70 and risk_tolerance == 'low':
#         insights.append({
#             'type': 'warning',
#             'message': 'High equity allocation may not suit your low risk tolerance.'
#         })
    
#     # Goal achievement
#     if goal_achievement >= 100:
#         insights.append({
#             'type': 'positive',
#             'message': f'Excellent! Projected to achieve {goal_achievement}% of your goal.'
#         })
#     elif goal_achievement >= 80:
#         insights.append({
#             'type': 'info',
#             'message': f'On track for {goal_achievement}% of goal. Small increases can bridge the gap.'
#         })
#     else:
#         insights.append({
#             'type': 'warning',
#             'message': f'Current SIP achieves {goal_achievement}% of goal. Increase SIP or extend timeline.'
#         })
    
#     insights.append({
#         'type': 'tip',
#         'message': 'Review portfolio annually and rebalance to maintain optimal allocation.'
#     })
    
#     return insights


# @app.route('/api/calculate-required-sip', methods=['POST'])
# def calculate_required_sip():
#     """Calculate required SIP to reach goal"""
#     try:
#         data = request.get_json()
        
#         goal_amount = data.get('goal_amount', 0)
#         duration_years = data.get('duration_years', 0)
#         expected_return = data.get('expected_return', 12) / 100
        
#         if goal_amount <= 0 or duration_years <= 0:
#             return jsonify({
#                 'success': False,
#                 'error': 'Goal amount and duration must be positive'
#             }), 400
        
#         r = expected_return / 12
#         n = duration_years * 12
        
#         required_sip = (goal_amount * r) / (np.power(1 + r, n) - 1)
        
#         return jsonify({
#             'success': True,
#             'data': {
#                 'required_monthly_sip': int(round(required_sip, -2)),
#                 'total_investment': int(required_sip * n),
#                 'expected_returns': expected_return * 100,
#                 'goal_amount': goal_amount,
#                 'duration_years': duration_years
#             }
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500


# @app.route('/api/compare-scenarios', methods=['POST'])
# def compare_scenarios():
#     """Compare different SIP scenarios"""
#     try:
#         data = request.get_json()
        
#         sip_amounts = data.get('sip_amounts', [5000, 10000, 15000])
#         duration_years = data.get('duration_years', 10)
#         equity_pct = data.get('equity_pct', 60)
#         debt_pct = data.get('debt_pct', 30)
#         hybrid_pct = data.get('hybrid_pct', 10)
        
#         scenarios = []
        
#         for sip in sip_amounts:
#             projection = calculate_projections(
#                 sip, equity_pct, debt_pct, hybrid_pct, duration_years, 0
#             )
            
#             scenarios.append({
#                 'sip_amount': sip,
#                 'total_investment': projection['total_investment'],
#                 'future_value': projection['future_value'],
#                 'wealth_gain': projection['wealth_gain'],
#                 'expected_returns': projection['expected_returns']
#             })
        
#         return jsonify({
#             'success': True,
#             'data': {
#                 'scenarios': scenarios,
#                 'duration_years': duration_years,
#                 'allocation': {
#                     'equity': equity_pct,
#                     'debt': debt_pct,
#                     'hybrid': hybrid_pct
#                 }
#             }
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500


# # ============================================================================
# # ERROR HANDLERS
# # ============================================================================

# @app.errorhandler(404)
# def not_found(e):
#     return jsonify({
#         'success': False,
#         'error': 'Endpoint not found'
#     }), 404


# @app.errorhandler(500)
# def internal_error(e):
#     return jsonify({
#         'success': False,
#         'error': 'Internal server error'
#     }), 500


# # ============================================================================
# # RUN SERVER
# # ============================================================================

# if __name__ == '__main__':
#     print("\n" + "=" * 80)
#     print("🚀 SIP INVESTMENT RECOMMENDATION API v2.0")
#     print("   WITH REAL-TIME INFLATION DATA INTEGRATION")
#     print("=" * 80)
#     print("\nAvailable Endpoints:")
#     print("  GET  /                          - Health check")
#     print("  GET  /api/market-data           - Market indicators (with real inflation)")
#     print("  GET  /api/inflation-info        - Current inflation details")
#     print("  GET  /api/inflation-trend       - Inflation trend analysis")
#     print("  GET  /api/funds                 - Available mutual funds")
#     print("  POST /api/predict               - Get SIP recommendations")
#     print("  POST /api/calculate-required-sip - Calculate required SIP")
#     print("  POST /api/compare-scenarios     - Compare scenarios")
#     print("\n" + "=" * 80)
    
#     app.run(debug=True, host='0.0.0.0', port=5001)