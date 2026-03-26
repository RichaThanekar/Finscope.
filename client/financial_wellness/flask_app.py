# 2026 changes

from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
from prophet import Prophet
import plotly.graph_objects as go
import plotly
import json
import numpy as np

app = Flask(__name__)
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Add CORS and iframe support
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    # Allow iframe embedding from localhost
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers.pop('X-Frame-Options', None)  # Remove if exists
    return response

# Main route - Home page with cards
@app.route('/')
def index():
    return render_template('index.html')

# Financial Advisor route
@app.route('/financial-advisor')
def financial_advisor():
    return render_template('financial_advisor.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process financial advisor analysis"""
    try:
        # Get form data
        data = request.get_json()
        
        age = int(data.get('age', 32))
        marital_status = data.get('marital_status', 'Single')
        dependents = int(data.get('dependents', 2))
        annual_income = float(data.get('annual_income', 800000))
        monthly_expenses = float(data.get('monthly_expenses', 40000))
        current_coverage = float(data.get('current_coverage', 5000000))
        annual_premium = float(data.get('annual_premium', 25000))
        accident_cover = float(data.get('accident_cover', 1000000))
        critical_illness = float(data.get('critical_illness', 500000))
        home_loan = float(data.get('home_loan', 2000000))
        other_debts = float(data.get('other_debts', 0))
        inflation_rate = float(data.get('inflation_rate', 6.5))
        
        # Perform calculations
        analysis = calculate_analysis(
            age, marital_status, dependents, annual_income, monthly_expenses,
            current_coverage, annual_premium, accident_cover, critical_illness,
            home_loan, other_debts, inflation_rate
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/generate-report', methods=['POST'])
def generate_report():
    """Generate detailed financial report"""
    try:
        data = request.get_json()
        
        annual_income = float(data.get('annual_income', 800000))
        monthly_expenses = float(data.get('monthly_expenses', 40000))
        current_coverage = float(data.get('current_coverage', 5000000))
        annual_premium = float(data.get('annual_premium', 25000))
        home_loan = float(data.get('home_loan', 2000000))
        age = int(data.get('age', 32))
        dependents = int(data.get('dependents', 2))
        critical_illness = float(data.get('critical_illness', 500000))
        accident_cover = float(data.get('accident_cover', 1000000))
        inflation_rate = float(data.get('inflation_rate', 6.5))
        
        report = generate_detailed_analysis(
            annual_income, monthly_expenses, current_coverage, annual_premium,
            home_loan, age, dependents, critical_illness, accident_cover, inflation_rate
        )
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def calculate_analysis(age, marital_status, dependents, annual_income, monthly_expenses,
                       current_coverage, annual_premium, accident_cover, critical_illness,
                       home_loan, other_debts, inflation_rate):
    """Calculate financial analysis metrics"""
    
    # Basic calculations
    annual_expenses = monthly_expenses * 12
    net_savings = annual_income - annual_expenses
    recommended_min = annual_income * 10
    recommended_max = annual_income * 15
    premium_percentage = (annual_premium / annual_income) * 100 if annual_income > 0 else 0
    total_debts = home_loan + other_debts
    
    # Coverage assessment
    coverage_gap = max(0, recommended_min - current_coverage)
    is_underinsured = coverage_gap > 0
    
    # Premium affordability
    max_affordable_premium = annual_income * 0.1  # 10% of income
    additional_premium_capacity = max_affordable_premium - annual_premium
    
    # Future expenses with inflation
    future_expenses_10y = annual_expenses * ((1 + inflation_rate/100) ** 10)
    
    # Recommended critical illness cover
    recommended_ci = annual_income * 3
    
    # Calculate scores
    coverage_score = min(10, (current_coverage / recommended_min) * 10)
    premium_score = 10 if premium_percentage < 5 else 8 if premium_percentage < 10 else 5
    debt_score = 10 if total_debts < annual_income else 7 if total_debts < annual_income * 2 else 4
    savings_score = 10 if net_savings > annual_income * 0.3 else 7 if net_savings > annual_income * 0.2 else 4
    overall_score = (coverage_score + premium_score + debt_score + savings_score) / 4
    
    # Savings and debt metrics
    savings_rate = (net_savings / annual_income * 100) if annual_income > 0 else 0
    debt_to_income = (total_debts / annual_income) if annual_income > 0 else 0
    
    # Affordability status
    affordability_status = "Highly Affordable" if premium_percentage < 5 else "Affordable" if premium_percentage < 10 else "High"
    
    # Critical illness gap
    ci_gap = max(0, recommended_ci - critical_illness)
    
    # Recommendations
    recommendations = []
    
    if is_underinsured:
        recommendations.append(f"🎯 **Increase Life Insurance Coverage** to ₹{recommended_min:,.0f} (minimum) to adequately protect your family.")
    
    if critical_illness < recommended_ci:
        recommendations.append(f"🏥 **Enhance Critical Illness Cover** to ₹{recommended_ci:,.0f} (3x your annual income).")
    
    if net_savings < annual_income * 0.2:
        recommendations.append("💰 **Improve Savings Rate** - Aim to save at least 20% of your income for long-term financial security.")
    
    if total_debts > annual_income * 2:
        recommendations.append("📉 **Debt Management** - Your debt-to-income ratio is high. Consider debt consolidation or prepayment strategies.")
    
    recommendations.append("📊 **Build Emergency Fund** - Maintain 6 months of expenses as emergency fund.")
    recommendations.append("🔄 **Review Annually** - Review and adjust your insurance coverage every year to account for inflation and life changes.")
    
    return {
        'annual_expenses': annual_expenses,
        'net_savings': net_savings,
        'recommended_min': recommended_min,
        'recommended_max': recommended_max,
        'premium_percentage': premium_percentage,
        'total_debts': total_debts,
        'coverage_gap': coverage_gap,
        'is_underinsured': is_underinsured,
        'additional_premium_capacity': additional_premium_capacity,
        'future_expenses_10y': future_expenses_10y,
        'recommended_ci': recommended_ci,
        'coverage_score': coverage_score,
        'premium_score': premium_score,
        'debt_score': debt_score,
        'savings_score': savings_score,
        'overall_score': overall_score,
        'savings_rate': savings_rate,
        'debt_to_income': debt_to_income,
        'affordability_status': affordability_status,
        'ci_gap': ci_gap,
        'recommendations': recommendations,
        'max_affordable_premium': max_affordable_premium
    }

def generate_detailed_analysis(annual_income, monthly_expenses, current_coverage, annual_premium, 
                              home_loan, age, dependents, critical_illness, accident_cover, inflation_rate):
    """Generate detailed analysis using financial rules"""
    
    # Calculations
    annual_expenses = monthly_expenses * 12
    recommended_min = annual_income * 10
    recommended_max = annual_income * 15
    premium_percentage = (annual_premium / annual_income) * 100
    
    # Coverage gap
    coverage_gap = max(0, recommended_min - current_coverage)
    
    # Future expenses with inflation
    inflation_decimal = inflation_rate / 100
    future_expenses_10y = annual_expenses * ((1 + inflation_decimal) ** 10)
    
    # Generate detailed report
    report = f"""
## 🏦 FINANCIAL ADVISORY ANALYSIS REPORT

### 1. COVERAGE ADEQUACY ASSESSMENT
---
**Current Coverage:** ₹{current_coverage:,} ({current_coverage/annual_income:.1f}x income)  
**Recommended Range:** ₹{recommended_min:,} - ₹{recommended_max:,} (10-15x income)  
**Assessment:** {"**⚠️ UNDERINSURED**" if coverage_gap > 0 else "**✅ ADEQUATE**"}  
**Coverage Gap:** ₹{coverage_gap:,}  
**Risk Factors:** Home loan ₹{home_loan:,} + {dependents} dependents  

{"🎯 **RECOMMENDATION:** Increase coverage by ₹" + f"{coverage_gap:,}" if coverage_gap > 0 else "✅ **STATUS:** Current coverage is adequate"}

### 2. PREMIUM AFFORDABILITY ANALYSIS
---
**Current Premium:** ₹{annual_premium:,} ({premium_percentage:.1f}% of income)  
**Affordability:** {"**Highly Affordable** 🟢" if premium_percentage < 5 else "**Affordable** 🟡" if premium_percentage < 10 else "**High** 🔴"}  
**Maximum Recommended:** ₹{annual_income * 0.1:,} (10% of income)  
**Additional Capacity:** ₹{(annual_income * 0.1) - annual_premium:,}  

💡 **RECOMMENDATION:** You can afford additional ₹{(annual_income * 0.1) - annual_premium:,} in premiums for more coverage

### 3. RIDER ANALYSIS
---
**Critical Illness Cover:** ₹{critical_illness:,} (Current)  
**Recommended CI Cover:** ₹{annual_income * 3:,} (3x income)  
**Accidental Death:** ₹{accident_cover:,} {"✅ (Adequate)" if accident_cover >= current_coverage * 2 else "⚠️ (Consider increasing)"}  

🏥 **RECOMMENDATION:** {"Increase Critical Illness cover to ₹" + f"{annual_income * 3:,}" if critical_illness < annual_income * 3 else "Critical illness coverage is adequate"}

### 4. INFLATION PROTECTION STRATEGY
---
**Current Annual Expenses:** ₹{annual_expenses:,}  
**Expenses in 10 years ({inflation_rate}% inflation):** ₹{future_expenses_10y:,}  
**Inflation Impact:** {((future_expenses_10y/annual_expenses - 1) * 100):.1f}% increase over 10 years  

📈 **STRATEGIES:**
- Increase coverage by 8-10% every 3 years
- Start SIP of ₹15,000/month in equity mutual funds
- Maximize PPF contribution (₹1.5L annually)
- Consider ULIP with top-up facility

### 5. IMMEDIATE ACTION PLAN
---
**🎯 Priority 1 (Next 30 days):**
- Increase term insurance to ₹{recommended_min:,}
- Build emergency fund: ₹{monthly_expenses * 6:,} (6 months expenses)

**📋 Priority 2 (Next 90 days):**
- Enhance Critical Illness cover to ₹{annual_income * 3:,}
- Start monthly SIP of ₹10,000 in diversified equity funds

**📅 Priority 3 (Next 6 months):**
- Review and optimize home loan prepayment strategy
- Set up automatic premium payments with annual increases

### 6. FINANCIAL HEALTH SCORE
---
"""
    
    # Calculate scores
    insurance_score = min(10, (current_coverage / recommended_min) * 10)
    premium_score = 9 if premium_percentage < 5 else 7 if premium_percentage < 10 else 4
    debt_score = 7 if home_loan < annual_income * 2 else 5 if home_loan < annual_income * 3 else 3
    overall_score = (insurance_score + premium_score + debt_score) / 3
    
    report += f"""
**Insurance Coverage:** {insurance_score:.1f}/10 {"(Underinsured)" if insurance_score < 8 else "(Good)" if insurance_score < 10 else "(Excellent)"}  
**Premium Affordability:** {premium_score:.1f}/10 {"(Highly affordable)" if premium_score >= 8 else "(Affordable)" if premium_score >= 6 else "(High)"}  
**Debt Management:** {debt_score:.1f}/10 {"(Manageable)" if debt_score >= 6 else "(Needs attention)"}  
**Overall Score:** {overall_score:.1f}/10 {"🟢 **Good foundation, needs enhancement**" if overall_score >= 6 else "🟡 **Needs improvement**"}

---
*This analysis is based on standard financial planning principles. Please consult a certified financial planner for personalized advice.*
"""
    
    return report

# Inflation Forecast route
@app.route('/inflation-forecast')
def inflation_forecast():
    return render_template('inflation_forecast.html')

@app.route('/test-inflation')
def test_inflation():
    return render_template('test_inflation.html')

@app.route('/api/inflation-data')
def get_inflation_data():
    """Get inflation forecast data"""
    try:
        # Load data
        df_all = pd.read_excel("data/df_all.xlsx", parse_dates=['Month'])
        
        # Check available columns
        print(f"Available columns: {df_all.columns.tolist()}")
        
        # Find the inflation column (case-insensitive)
        inflation_col = None
        for col in df_all.columns:
            if 'inflation' in col.lower():
                inflation_col = col
                break
        
        if inflation_col is None:
            return jsonify({
                'success': False,
                'error': f'Inflation column not found. Available columns: {df_all.columns.tolist()}'
            }), 400
        
        # Prepare data for Prophet
        df_prophet = df_all[['Month', inflation_col]].copy()
        df_prophet['y'] = pd.to_numeric(df_prophet[inflation_col], errors='coerce')
        
        # Remove NaN and fill forward
        df_prophet = df_prophet.dropna()
        if len(df_prophet) == 0:
            return jsonify({'success': False, 'error': 'No valid data found'}), 400
            
        df_prophet['y'] = df_prophet['y'].ffill()
        df_prophet = df_prophet.rename(columns={'Month': 'ds'})
        df_prophet = df_prophet.dropna()
        
        print(f"Prepared {len(df_prophet)} data points for forecasting")
        print(f"Data range: {df_prophet['y'].min()} to {df_prophet['y'].max()}")
        print(f"Date range: {df_prophet['ds'].min()} to {df_prophet['ds'].max()}")
        
        # Train model with better parameters for inflation data
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.5,  # More flexible to detect changes
            seasonality_mode='additive',   # Better for inflation
            seasonality_prior_scale=10.0    # Stronger seasonality
        )
        model.fit(df_prophet[['ds', 'y']])
        
        # Forecast
        future = model.make_future_dataframe(periods=12, freq='MS')
        forecast = model.predict(future)
        
        # Separate historical and forecast data
        historical_len = len(df_prophet)
        forecast_future = forecast.iloc[historical_len:]
        
        # Create plot
        fig = go.Figure()
        
        # Convert dates to strings for better JSON handling
        historical_dates = [d.strftime('%Y-%m-%d') for d in df_prophet['ds']]
        forecast_dates = [d.strftime('%Y-%m-%d') for d in forecast_future['ds']]
        
        # Historical actual data
        fig.add_trace(go.Scatter(
            x=historical_dates,
            y=df_prophet['y'].tolist(),
            mode='lines+markers',
            name='Historical Inflation',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=4)
        ))
        
        # Historical fitted values
        fig.add_trace(go.Scatter(
            x=historical_dates,
            y=forecast.iloc[:historical_len]['yhat'].tolist(),
            mode='lines',
            name='Fitted Values',
            line=dict(color='#2ca02c', width=2, dash='dash')
        ))
        
        # Future forecast
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_future['yhat'].tolist(),
            mode='lines+markers',
            name='Forecast (Next 12 Months)',
            line=dict(color='#d62728', width=3),
            marker=dict(size=6)
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_dates + forecast_dates[::-1],
            y=forecast_future['yhat_upper'].tolist() + forecast_future['yhat_lower'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(214,39,40,0.2)',
            line=dict(width=0),
            showlegend=True,
            name='Confidence Interval'
        ))
        
        fig.update_layout(
            title=dict(
                text='📈 Inflation Forecast - Actual, Fitted & Next 12 Months',
                x=0.5,
                xanchor='center',
                font=dict(size=20)
            ),
            xaxis_title='Date',
            yaxis_title='Inflation Rate (%)',
            hovermode='x unified',
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5
            )
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Get summary stats
        latest_actual = float(df_prophet['y'].iloc[-1])
        avg_forecast = float(forecast_future['yhat'].mean())
        max_forecast = float(forecast_future['yhat'].max())
        min_forecast = float(forecast_future['yhat'].min())
        trend = "increasing" if avg_forecast > latest_actual else "decreasing"
        
        # Convert forecast data for table
        forecast_table = []
        for _, row in forecast_future.iterrows():
            forecast_table.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted': float(row['yhat']),
                'lower': float(row['yhat_lower']),
                'upper': float(row['yhat_upper'])
            })
        
        return jsonify({
            'success': True,
            'graph': graphJSON,
            'latest_actual': latest_actual,
            'avg_forecast': avg_forecast,
            'max_forecast': max_forecast,
            'min_forecast': min_forecast,
            'trend': trend,
            'forecast_data': forecast_table,
            'data_points': len(df_prophet)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# GDP Forecast route
@app.route('/gdp-forecast')
def gdp_forecast():
    return render_template('gdp_forecast.html')

@app.route('/api/gdp-data')
def get_gdp_data():
    """Get GDP forecast data"""
    try:
        df_gdp = pd.read_excel("data/gdp_data.xlsx", parse_dates=['Date'])
        
        print(f"GDP data columns: {df_gdp.columns.tolist()}")
        print(f"GDP data shape: {df_gdp.shape}")
        
        # Prepare data
        df_prophet = df_gdp[['Date', 'GDP_Growth_Rate']].copy()
        df_prophet['y'] = pd.to_numeric(df_prophet['GDP_Growth_Rate'], errors='coerce')
        df_prophet['y'] = df_prophet['y'].ffill()
        df_prophet = df_prophet.rename(columns={'Date': 'ds'})
        df_prophet = df_prophet.dropna()
        
        print(f"Prepared {len(df_prophet)} GDP data points")
        print(f"GDP range: {df_prophet['y'].min()} to {df_prophet['y'].max()}")
        
        # Train model with better parameters
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.5,
            seasonality_mode='additive',
            seasonality_prior_scale=10.0
        )
        model.fit(df_prophet[['ds', 'y']])
        
        # Forecast
        future = model.make_future_dataframe(periods=12, freq='MS')
        forecast = model.predict(future)
        
        # Separate historical and forecast data
        historical_len = len(df_prophet)
        forecast_future = forecast.iloc[historical_len:]
        
        # Create plot with proper date conversion
        fig = go.Figure()
        
        # Convert dates to strings
        historical_dates = [d.strftime('%Y-%m-%d') for d in df_prophet['ds']]
        forecast_dates = [d.strftime('%Y-%m-%d') for d in forecast_future['ds']]
        
        # Historical actual data
        fig.add_trace(go.Scatter(
            x=historical_dates,
            y=df_prophet['y'].tolist(),
            mode='lines+markers',
            name='Historical GDP Growth',
            line=dict(color='#2ca02c', width=2),
            marker=dict(size=4)
        ))
        
        # Historical fitted values
        fig.add_trace(go.Scatter(
            x=historical_dates,
            y=forecast.iloc[:historical_len]['yhat'].tolist(),
            mode='lines',
            name='Fitted Values',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ))
        
        # Future forecast
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_future['yhat'].tolist(),
            mode='lines+markers',
            name='Forecast (Next 12 Months)',
            line=dict(color='#d62728', width=3),
            marker=dict(size=6)
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_dates + forecast_dates[::-1],
            y=forecast_future['yhat_upper'].tolist() + forecast_future['yhat_lower'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(214,39,40,0.2)',
            line=dict(width=0),
            showlegend=True,
            name='Confidence Interval'
        ))
        
        fig.update_layout(
            title=dict(
                text='📊 GDP Growth Forecast - Actual, Fitted & Next 12 Months',
                x=0.5,
                xanchor='center',
                font=dict(size=20)
            ),
            xaxis_title='Date',
            yaxis_title='GDP Growth Rate (%)',
            hovermode='x unified',
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5
            )
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        latest_actual = float(df_prophet['y'].iloc[-1])
        avg_forecast = float(forecast_future['yhat'].mean())
        max_forecast = float(forecast_future['yhat'].max())
        min_forecast = float(forecast_future['yhat'].min())
        trend = "increasing" if avg_forecast > latest_actual else "decreasing"
        
        # Convert forecast data for table
        forecast_table = []
        for _, row in forecast_future.iterrows():
            forecast_table.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted': float(row['yhat']),
                'lower': float(row['yhat_lower']),
                'upper': float(row['yhat_upper'])
            })
        
        return jsonify({
            'success': True,
            'graph': graphJSON,
            'latest_actual': latest_actual,
            'avg_forecast': avg_forecast,
            'max_forecast': max_forecast,
            'min_forecast': min_forecast,
            'trend': trend,
            'forecast_data': forecast_table,
            'data_points': len(df_prophet)
        })
        
    except Exception as e:
        print(f"Error in GDP forecast: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# Interest Rates Forecast route
@app.route('/interest-rates-forecast')
def interest_rates_forecast():
    return render_template('interest_rates_forecast.html')

@app.route('/api/interest-rates-data')
def get_interest_rates_data():
    """Get interest rates forecast data"""
    try:
        rate_type = request.args.get('rate_type', 'Repo_Rate')
        
        df_rates = pd.read_excel("data/interest_rates_data.xlsx", parse_dates=['Date'])
        
        print(f"Interest rates data columns: {df_rates.columns.tolist()}")
        print(f"Rate type requested: {rate_type}")
        
        # Prepare data
        df_prophet = df_rates[['Date', rate_type]].copy()
        df_prophet['y'] = pd.to_numeric(df_prophet[rate_type], errors='coerce')
        df_prophet['y'] = df_prophet['y'].ffill()
        df_prophet = df_prophet.rename(columns={'Date': 'ds'})
        df_prophet = df_prophet.dropna()
        
        print(f"Prepared {len(df_prophet)} interest rate data points")
        print(f"Rate range: {df_prophet['y'].min()} to {df_prophet['y'].max()}")
        
        # Train model with better parameters
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.5,
            seasonality_mode='additive',
            seasonality_prior_scale=10.0
        )
        model.fit(df_prophet[['ds', 'y']])
        
        # Forecast
        future = model.make_future_dataframe(periods=12, freq='MS')
        forecast = model.predict(future)
        
        # Separate historical and forecast data
        historical_len = len(df_prophet)
        forecast_future = forecast.iloc[historical_len:]
        
        # Create plot with proper date conversion
        fig = go.Figure()
        
        # Convert dates to strings
        historical_dates = [d.strftime('%Y-%m-%d') for d in df_prophet['ds']]
        forecast_dates = [d.strftime('%Y-%m-%d') for d in forecast_future['ds']]
        
        # Historical actual data
        fig.add_trace(go.Scatter(
            x=historical_dates,
            y=df_prophet['y'].tolist(),
            mode='lines+markers',
            name=f'Historical {rate_type.replace("_", " ")}',
            line=dict(color='#9467bd', width=2),
            marker=dict(size=4)
        ))
        
        # Historical fitted values
        fig.add_trace(go.Scatter(
            x=historical_dates,
            y=forecast.iloc[:historical_len]['yhat'].tolist(),
            mode='lines',
            name='Fitted Values',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ))
        
        # Future forecast
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_future['yhat'].tolist(),
            mode='lines+markers',
            name='Forecast (Next 12 Months)',
            line=dict(color='#d62728', width=3),
            marker=dict(size=6)
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_dates + forecast_dates[::-1],
            y=forecast_future['yhat_upper'].tolist() + forecast_future['yhat_lower'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(214,39,40,0.2)',
            line=dict(width=0),
            showlegend=True,
            name='Confidence Interval'
        ))
        
        fig.update_layout(
            title=dict(
                text=f'💰 {rate_type.replace("_", " ")} Forecast - Actual, Fitted & Next 12 Months',
                x=0.5,
                xanchor='center',
                font=dict(size=20)
            ),
            xaxis_title='Date',
            yaxis_title='Interest Rate (%)',
            hovermode='x unified',
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5
            )
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        latest_actual = float(df_prophet['y'].iloc[-1])
        avg_forecast = float(forecast_future['yhat'].mean())
        max_forecast = float(forecast_future['yhat'].max())
        min_forecast = float(forecast_future['yhat'].min())
        trend = "increasing" if avg_forecast > latest_actual else "decreasing"
        
        # Convert forecast data for table
        forecast_table = []
        for _, row in forecast_future.iterrows():
            forecast_table.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted': float(row['yhat']),
                'lower': float(row['yhat_lower']),
                'upper': float(row['yhat_upper'])
            })
        
        return jsonify({
            'success': True,
            'graph': graphJSON,
            'latest_actual': latest_actual,
            'avg_forecast': avg_forecast,
            'max_forecast': max_forecast,
            'min_forecast': min_forecast,
            'trend': trend,
            'rate_type': rate_type.replace('_', ' '),
            'forecast_data': forecast_table,
            'data_points': len(df_prophet)
        })
        
    except Exception as e:
        print(f"Error in interest rates forecast: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# Policy Recommendations route
@app.route('/policy-recommendations')
def policy_recommendations():
    return render_template('policy_recommendations.html')

@app.route('/api/policy-recommend', methods=['POST'])
def get_policy_recommendation():
    """Generate policy recommendations based on user profile"""
    try:
        from risk_assesment import calculate_risk_score
        from search_serp import get_policy_recommendations_from_serpapi
        from utils import build_prompt_with_search
        from gemini_llm import query_gemini

        data = request.get_json()

        # Extract safely
        age = int(data.get('age', 30))
        gender = data.get('gender', 'Male')
        occupation = data.get('occupation', 'Employee')
        income = float(data.get('income', 500000))
        smoker = data.get('smoker', 'No')
        driving_record = data.get('driving_record', 'Clean')
        policy_type = data.get('policy_type', 'Health Insurance')
        disease = data.get('disease', 'None')
        dependents = int(data.get('dependents', 0))

        # 1️⃣ Calculate risk
        risk_category = calculate_risk_score(age, income, driving_record, smoker, disease, dependents)

        # 2️⃣ Build profile
        user_profile = {
            "Age": age,
            "Gender": gender,
            "Occupation": occupation,
            "Income Level": income,
            "Insurance Type": policy_type,
            "Smoker": smoker,
            "Driving Record": driving_record,
            "Pre-existing Condition": disease,
            "Dependents": dependents,
            "Risk Category": risk_category,
        }

        # 3️⃣ SERP results
        search_results = get_policy_recommendations_from_serpapi(user_profile)
        if not search_results:
            search_results = [{"title": "No results found", "link": "", "snippet": ""}]

        # 4️⃣ Prompt + LLM
        prompt = build_prompt_with_search(user_profile, search_results)
        recommendation = query_gemini(prompt)

        # 5️⃣ Return response
        return jsonify({
            "success": True,
            "risk_category": risk_category,
            "recommendation": recommendation
        }), 200

    except Exception as e:
        print("Error in /api/policy-recommend:", str(e))
        return jsonify({
            "success": False,
            "error": str(e),
            "recommendation": f"""

"""
        }), 200




@app.route('/api/predict', methods=['POST'])
def predict_sip():
    """Get SIP investment recommendations"""
    try:
        data = request.get_json()
        
        # Extract data with defaults
        age = int(data.get('age', 30))
        monthly_income = float(data.get('monthly_income', 80000))
        monthly_expenses = float(data.get('monthly_expenses', 45000))
        existing_EMIs = float(data.get('existing_EMIs', 5000))
        current_savings = float(data.get('current_savings', 100000))
        current_investments_value = float(data.get('current_investments_value', 50000))
        goal_type = data.get('goal_type', 'retirement')
        goal_amount = float(data.get('goal_amount', 5000000))
        goal_duration_years = int(data.get('goal_duration_years', 25))
        risk_tolerance = data.get('risk_tolerance', 'medium')
        
        # Calculate monthly surplus
        monthly_surplus = monthly_income - monthly_expenses - existing_EMIs
        
        # Calculate recommended SIP based on goal
        # Assuming average return rates: low=8%, medium=12%, high=15%
        if risk_tolerance == 'low':
            expected_return = 0.08
            allocation = {'equity': 20, 'debt': 70, 'gold': 10}
        elif risk_tolerance == 'high':
            expected_return = 0.15
            allocation = {'equity': 80, 'debt': 15, 'gold': 5}
        else:  # medium
            expected_return = 0.12
            allocation = {'equity': 60, 'debt': 30, 'gold': 10}
        
        # Calculate required monthly SIP using future value formula
        # FV = SIP * [((1 + r)^n - 1) / r] * (1 + r)
        months = goal_duration_years * 12
        monthly_rate = expected_return / 12
        
        # Future value of current investments
        fv_current = current_investments_value * ((1 + expected_return) ** goal_duration_years)
        
        # Required future value from SIP
        required_fv = goal_amount - fv_current
        
        if required_fv > 0 and months > 0:
            # Calculate required SIP
            sip_factor = (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
            recommended_sip = int(required_fv / sip_factor)
        else:
            recommended_sip = int(monthly_surplus * 0.3)  # Default to 30% of surplus
        
        # Cap SIP at 60% of monthly surplus
        max_sip = int(monthly_surplus * 0.6)
        if recommended_sip > max_sip:
            recommended_sip = max_sip
            achievable = False
        else:
            achievable = True
        
        # Ensure minimum SIP
        if recommended_sip < 500:
            recommended_sip = 500
        
        # Calculate projections
        projected_corpus = recommended_sip * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate) + fv_current
        
        # Generate fund recommendations based on risk tolerance
        if risk_tolerance == 'low':
            funds = [
                {'name': 'HDFC Balanced Advantage Fund', 'category': 'Hybrid', 'sub_category': 'Dynamic Asset Allocation', 'risk': 'Low', 'returns': '8-10%', 'returns_3y': '9', 'expense_ratio': '0.85', 'allocation': 40, 'allocation_percentage': 40},
                {'name': 'ICICI Prudential Corporate Bond Fund', 'category': 'Debt', 'sub_category': 'Corporate Bond', 'risk': 'Low', 'returns': '7-8%', 'returns_3y': '7.5', 'expense_ratio': '0.65', 'allocation': 30, 'allocation_percentage': 30},
                {'name': 'SBI Magnum Gilt Fund', 'category': 'Debt', 'sub_category': 'Gilt', 'risk': 'Low', 'returns': '7-9%', 'returns_3y': '8', 'expense_ratio': '0.75', 'allocation': 20, 'allocation_percentage': 20},
                {'name': 'Nippon India Gold Savings Fund', 'category': 'Gold', 'sub_category': 'Gold ETF', 'risk': 'Low', 'returns': '6-8%', 'returns_3y': '7', 'expense_ratio': '0.50', 'allocation': 10, 'allocation_percentage': 10}
            ]
        elif risk_tolerance == 'high':
            funds = [
                {'name': 'Axis Bluechip Fund', 'category': 'Equity', 'sub_category': 'Large Cap', 'risk': 'High', 'returns': '15-18%', 'returns_3y': '16.5', 'expense_ratio': '0.50', 'allocation': 40, 'allocation_percentage': 40},
                {'name': 'Parag Parikh Flexi Cap Fund', 'category': 'Equity', 'sub_category': 'Flexi Cap', 'risk': 'High', 'returns': '14-17%', 'returns_3y': '15.8', 'expense_ratio': '0.72', 'allocation': 30, 'allocation_percentage': 30},
                {'name': 'Mirae Asset Emerging Bluechip', 'category': 'Equity', 'sub_category': 'Large & Mid Cap', 'risk': 'High', 'returns': '15-20%', 'returns_3y': '17.2', 'expense_ratio': '0.69', 'allocation': 25, 'allocation_percentage': 25},
                {'name': 'ICICI Prudential Corporate Bond Fund', 'category': 'Debt', 'sub_category': 'Corporate Bond', 'risk': 'Low', 'returns': '7-8%', 'returns_3y': '7.5', 'expense_ratio': '0.65', 'allocation': 5, 'allocation_percentage': 5}
            ]
        else:  # medium
            funds = [
                {'name': 'Axis Bluechip Fund', 'category': 'Equity', 'sub_category': 'Large Cap', 'risk': 'Medium', 'returns': '12-15%', 'returns_3y': '13.8', 'expense_ratio': '0.50', 'allocation': 35, 'allocation_percentage': 35},
                {'name': 'Mirae Asset Large Cap Fund', 'category': 'Equity', 'sub_category': 'Large Cap', 'risk': 'Medium', 'returns': '11-14%', 'returns_3y': '12.5', 'expense_ratio': '0.52', 'allocation': 25, 'allocation_percentage': 25},
                {'name': 'HDFC Corporate Bond Fund', 'category': 'Debt', 'sub_category': 'Corporate Bond', 'risk': 'Low', 'returns': '7-9%', 'returns_3y': '8.2', 'expense_ratio': '0.68', 'allocation': 20, 'allocation_percentage': 20},
                {'name': 'SBI Magnum Medium Duration Fund', 'category': 'Debt', 'sub_category': 'Medium Duration', 'risk': 'Low', 'returns': '7-8%', 'returns_3y': '7.8', 'expense_ratio': '0.70', 'allocation': 15, 'allocation_percentage': 15},
                {'name': 'Nippon India Gold Savings Fund', 'category': 'Gold', 'sub_category': 'Gold ETF', 'risk': 'Low', 'returns': '6-8%', 'returns_3y': '7', 'expense_ratio': '0.50', 'allocation': 5, 'allocation_percentage': 5}
            ]
        
        # Generate insights
        insights = []
        
        if monthly_surplus < recommended_sip:
            insights.append({
                'type': 'warning',
                'message': f'Your monthly surplus (₹{int(monthly_surplus):,}) is less than recommended SIP. Consider reducing expenses or increasing income.'
            })
        else:
            insights.append({
                'type': 'positive',
                'message': f'Great! You have sufficient monthly surplus (₹{int(monthly_surplus):,}) to meet your SIP goal.'
            })
        
        if age < 35:
            insights.append({
                'type': 'tip',
                'message': 'You have time on your side! Consider aggressive equity allocation for higher returns.'
            })
        elif age > 50:
            insights.append({
                'type': 'info',
                'message': 'Focus on capital preservation with higher debt allocation as you approach retirement.'
            })
        
        if goal_duration_years < 5:
            insights.append({
                'type': 'warning',
                'message': 'Short investment horizon. Consider balanced funds over pure equity.'
            })
        
        if current_savings < monthly_income * 3:
            insights.append({
                'type': 'warning',
                'message': 'Build an emergency fund of 6 months expenses before investing heavily in SIP.'
            })
        
        if achievable:
            insights.append({
                'type': 'positive',
                'message': f'Your goal of ₹{int(goal_amount):,} is achievable with disciplined SIP investing!'
            })
        else:
            insights.append({
                'type': 'info',
                'message': f'To achieve ₹{int(goal_amount):,}, consider increasing investment duration or reducing goal amount.'
            })
        
        response_data = {
            'recommended_SIP_amount': recommended_sip,
            'recommended_sip': recommended_sip,  # Keep both for compatibility
            'monthly_surplus': int(monthly_surplus),
            'goal_achievable': achievable,
            'projected_corpus': int(projected_corpus),
            'expected_return': f'{expected_return * 100:.0f}%',
            'investment_duration': f'{goal_duration_years} years',
            'asset_allocation': allocation,
            'fund_recommendations': funds,
            'insights': insights,
            'breakdown': {
                'monthly_income': int(monthly_income),
                'monthly_expenses': int(monthly_expenses),
                'existing_EMIs': int(existing_EMIs),
                'available_for_investment': int(monthly_surplus)
            },
            'projections': {
                'total_investment': int(recommended_sip * months),
                'future_value': int(projected_corpus),
                'wealth_gain': int(projected_corpus - (recommended_sip * months)),
                'goal_achievement': min(100, int((projected_corpus / goal_amount) * 100))
            }
        }
        
        return jsonify({
            'success': True,
            'data': response_data
        })
        
    except Exception as e:
        print(f"Error in SIP prediction: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)