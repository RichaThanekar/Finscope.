# from flask import Flask, render_template, request, jsonify
# import pandas as pd
# from datetime import datetime
# from prophet import Prophet
# import plotly.graph_objects as go
# import plotly
# import json
# import numpy as np

# app = Flask(__name__)

# # Main route - Home page with cards
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Financial Advisor route
# @app.route('/financial-advisor')
# def financial_advisor():
#     return render_template('financial_advisor.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     """Process financial advisor analysis"""
#     try:
#         # Get form data
#         data = request.get_json()
        
#         age = int(data.get('age', 32))
#         marital_status = data.get('marital_status', 'Single')
#         dependents = int(data.get('dependents', 2))
#         annual_income = float(data.get('annual_income', 800000))
#         monthly_expenses = float(data.get('monthly_expenses', 40000))
#         current_coverage = float(data.get('current_coverage', 5000000))
#         annual_premium = float(data.get('annual_premium', 25000))
#         accident_cover = float(data.get('accident_cover', 1000000))
#         critical_illness = float(data.get('critical_illness', 500000))
#         home_loan = float(data.get('home_loan', 2000000))
#         other_debts = float(data.get('other_debts', 0))
#         inflation_rate = float(data.get('inflation_rate', 6.5))
        
#         # Perform calculations
#         analysis = calculate_analysis(
#             age, marital_status, dependents, annual_income, monthly_expenses,
#             current_coverage, annual_premium, accident_cover, critical_illness,
#             home_loan, other_debts, inflation_rate
#         )
        
#         return jsonify({
#             'success': True,
#             'analysis': analysis
#         })
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/generate-report', methods=['POST'])
# def generate_report():
#     """Generate detailed financial report"""
#     try:
#         data = request.get_json()
        
#         annual_income = float(data.get('annual_income', 800000))
#         monthly_expenses = float(data.get('monthly_expenses', 40000))
#         current_coverage = float(data.get('current_coverage', 5000000))
#         annual_premium = float(data.get('annual_premium', 25000))
#         home_loan = float(data.get('home_loan', 2000000))
#         age = int(data.get('age', 32))
#         dependents = int(data.get('dependents', 2))
#         critical_illness = float(data.get('critical_illness', 500000))
#         accident_cover = float(data.get('accident_cover', 1000000))
#         inflation_rate = float(data.get('inflation_rate', 6.5))
        
#         report = generate_detailed_analysis(
#             annual_income, monthly_expenses, current_coverage, annual_premium,
#             home_loan, age, dependents, critical_illness, accident_cover, inflation_rate
#         )
        
#         return jsonify({
#             'success': True,
#             'report': report
#         })
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# def calculate_analysis(age, marital_status, dependents, annual_income, monthly_expenses,
#                        current_coverage, annual_premium, accident_cover, critical_illness,
#                        home_loan, other_debts, inflation_rate):
#     """Calculate financial analysis metrics"""
    
#     # Basic calculations
#     annual_expenses = monthly_expenses * 12
#     net_savings = annual_income - annual_expenses
#     recommended_min = annual_income * 10
#     recommended_max = annual_income * 15
#     premium_percentage = (annual_premium / annual_income) * 100 if annual_income > 0 else 0
#     total_debts = home_loan + other_debts
    
#     # Coverage assessment
#     coverage_gap = max(0, recommended_min - current_coverage)
#     is_underinsured = coverage_gap > 0
    
#     # Premium affordability
#     max_affordable_premium = annual_income * 0.1  # 10% of income
#     additional_premium_capacity = max_affordable_premium - annual_premium
    
#     # Future expenses with inflation
#     future_expenses_10y = annual_expenses * ((1 + inflation_rate/100) ** 10)
    
#     # Recommended critical illness cover
#     recommended_ci = annual_income * 3
    
#     # Calculate scores
#     coverage_score = min(10, (current_coverage / recommended_min) * 10)
#     premium_score = 10 if premium_percentage < 5 else 8 if premium_percentage < 10 else 5
#     debt_score = 10 if total_debts < annual_income else 7 if total_debts < annual_income * 2 else 4
#     savings_score = 10 if net_savings > annual_income * 0.3 else 7 if net_savings > annual_income * 0.2 else 4
#     overall_score = (coverage_score + premium_score + debt_score + savings_score) / 4
    
#     # Savings and debt metrics
#     savings_rate = (net_savings / annual_income * 100) if annual_income > 0 else 0
#     debt_to_income = (total_debts / annual_income) if annual_income > 0 else 0
    
#     # Affordability status
#     affordability_status = "Highly Affordable" if premium_percentage < 5 else "Affordable" if premium_percentage < 10 else "High"
    
#     # Critical illness gap
#     ci_gap = max(0, recommended_ci - critical_illness)
    
#     # Recommendations
#     recommendations = []
    
#     if is_underinsured:
#         recommendations.append(f"🎯 **Increase Life Insurance Coverage** to ₹{recommended_min:,.0f} (minimum) to adequately protect your family.")
    
#     if critical_illness < recommended_ci:
#         recommendations.append(f"🏥 **Enhance Critical Illness Cover** to ₹{recommended_ci:,.0f} (3x your annual income).")
    
#     if net_savings < annual_income * 0.2:
#         recommendations.append("💰 **Improve Savings Rate** - Aim to save at least 20% of your income for long-term financial security.")
    
#     if total_debts > annual_income * 2:
#         recommendations.append("📉 **Debt Management** - Your debt-to-income ratio is high. Consider debt consolidation or prepayment strategies.")
    
#     recommendations.append("📊 **Build Emergency Fund** - Maintain 6 months of expenses as emergency fund.")
#     recommendations.append("🔄 **Review Annually** - Review and adjust your insurance coverage every year to account for inflation and life changes.")
    
#     return {
#         'annual_expenses': annual_expenses,
#         'net_savings': net_savings,
#         'recommended_min': recommended_min,
#         'recommended_max': recommended_max,
#         'premium_percentage': premium_percentage,
#         'total_debts': total_debts,
#         'coverage_gap': coverage_gap,
#         'is_underinsured': is_underinsured,
#         'additional_premium_capacity': additional_premium_capacity,
#         'future_expenses_10y': future_expenses_10y,
#         'recommended_ci': recommended_ci,
#         'coverage_score': coverage_score,
#         'premium_score': premium_score,
#         'debt_score': debt_score,
#         'savings_score': savings_score,
#         'overall_score': overall_score,
#         'savings_rate': savings_rate,
#         'debt_to_income': debt_to_income,
#         'affordability_status': affordability_status,
#         'ci_gap': ci_gap,
#         'recommendations': recommendations,
#         'max_affordable_premium': max_affordable_premium
#     }

# def generate_detailed_analysis(annual_income, monthly_expenses, current_coverage, annual_premium, 
#                               home_loan, age, dependents, critical_illness, accident_cover, inflation_rate):
#     """Generate detailed analysis using financial rules"""
    
#     # Calculations
#     annual_expenses = monthly_expenses * 12
#     recommended_min = annual_income * 10
#     recommended_max = annual_income * 15
#     premium_percentage = (annual_premium / annual_income) * 100
    
#     # Coverage gap
#     coverage_gap = max(0, recommended_min - current_coverage)
    
#     # Future expenses with inflation
#     inflation_decimal = inflation_rate / 100
#     future_expenses_10y = annual_expenses * ((1 + inflation_decimal) ** 10)
    
#     # Generate detailed report
#     report = f"""
# ## 🏦 FINANCIAL ADVISORY ANALYSIS REPORT

# ### 1. COVERAGE ADEQUACY ASSESSMENT
# ---
# **Current Coverage:** ₹{current_coverage:,} ({current_coverage/annual_income:.1f}x income)  
# **Recommended Range:** ₹{recommended_min:,} - ₹{recommended_max:,} (10-15x income)  
# **Assessment:** {"**⚠️ UNDERINSURED**" if coverage_gap > 0 else "**✅ ADEQUATE**"}  
# **Coverage Gap:** ₹{coverage_gap:,}  
# **Risk Factors:** Home loan ₹{home_loan:,} + {dependents} dependents  

# {"🎯 **RECOMMENDATION:** Increase coverage by ₹" + f"{coverage_gap:,}" if coverage_gap > 0 else "✅ **STATUS:** Current coverage is adequate"}

# ### 2. PREMIUM AFFORDABILITY ANALYSIS
# ---
# **Current Premium:** ₹{annual_premium:,} ({premium_percentage:.1f}% of income)  
# **Affordability:** {"**Highly Affordable** 🟢" if premium_percentage < 5 else "**Affordable** 🟡" if premium_percentage < 10 else "**High** 🔴"}  
# **Maximum Recommended:** ₹{annual_income * 0.1:,} (10% of income)  
# **Additional Capacity:** ₹{(annual_income * 0.1) - annual_premium:,}  

# 💡 **RECOMMENDATION:** You can afford additional ₹{(annual_income * 0.1) - annual_premium:,} in premiums for more coverage

# ### 3. RIDER ANALYSIS
# ---
# **Critical Illness Cover:** ₹{critical_illness:,} (Current)  
# **Recommended CI Cover:** ₹{annual_income * 3:,} (3x income)  
# **Accidental Death:** ₹{accident_cover:,} {"✅ (Adequate)" if accident_cover >= current_coverage * 2 else "⚠️ (Consider increasing)"}  

# 🏥 **RECOMMENDATION:** {"Increase Critical Illness cover to ₹" + f"{annual_income * 3:,}" if critical_illness < annual_income * 3 else "Critical illness coverage is adequate"}

# ### 4. INFLATION PROTECTION STRATEGY
# ---
# **Current Annual Expenses:** ₹{annual_expenses:,}  
# **Expenses in 10 years ({inflation_rate}% inflation):** ₹{future_expenses_10y:,}  
# **Inflation Impact:** {((future_expenses_10y/annual_expenses - 1) * 100):.1f}% increase over 10 years  

# 📈 **STRATEGIES:**
# - Increase coverage by 8-10% every 3 years
# - Start SIP of ₹15,000/month in equity mutual funds
# - Maximize PPF contribution (₹1.5L annually)
# - Consider ULIP with top-up facility

# ### 5. IMMEDIATE ACTION PLAN
# ---
# **🎯 Priority 1 (Next 30 days):**
# - Increase term insurance to ₹{recommended_min:,}
# - Build emergency fund: ₹{monthly_expenses * 6:,} (6 months expenses)

# **📋 Priority 2 (Next 90 days):**
# - Enhance Critical Illness cover to ₹{annual_income * 3:,}
# - Start monthly SIP of ₹10,000 in diversified equity funds

# **📅 Priority 3 (Next 6 months):**
# - Review and optimize home loan prepayment strategy
# - Set up automatic premium payments with annual increases

# ### 6. FINANCIAL HEALTH SCORE
# ---
# """
    
#     # Calculate scores
#     insurance_score = min(10, (current_coverage / recommended_min) * 10)
#     premium_score = 9 if premium_percentage < 5 else 7 if premium_percentage < 10 else 4
#     debt_score = 7 if home_loan < annual_income * 2 else 5 if home_loan < annual_income * 3 else 3
#     overall_score = (insurance_score + premium_score + debt_score) / 3
    
#     report += f"""
# **Insurance Coverage:** {insurance_score:.1f}/10 {"(Underinsured)" if insurance_score < 8 else "(Good)" if insurance_score < 10 else "(Excellent)"}  
# **Premium Affordability:** {premium_score:.1f}/10 {"(Highly affordable)" if premium_score >= 8 else "(Affordable)" if premium_score >= 6 else "(High)"}  
# **Debt Management:** {debt_score:.1f}/10 {"(Manageable)" if debt_score >= 6 else "(Needs attention)"}  
# **Overall Score:** {overall_score:.1f}/10 {"🟢 **Good foundation, needs enhancement**" if overall_score >= 6 else "🟡 **Needs improvement**"}

# ---
# *This analysis is based on standard financial planning principles. Please consult a certified financial planner for personalized advice.*
# """
    
#     return report

# # Inflation Forecast route
# @app.route('/inflation-forecast')
# def inflation_forecast():
#     return render_template('inflation_forecast.html')

# @app.route('/api/inflation-data')
# def get_inflation_data():
#     """Get inflation forecast data"""
#     try:
#         df_all = pd.read_excel("data/df_all.xlsx", parse_dates=['Month'])
        
#         # Prepare data for Prophet
#         df_prophet = df_all[['Month', 'Combined Inflation (%)']].copy()
#         df_prophet['y'] = pd.to_numeric(df_prophet['Combined Inflation (%)'], errors='coerce')
#         df_prophet['y'] = df_prophet['y'].ffill()
#         df_prophet = df_prophet.rename(columns={'Month': 'ds'})
        
#         # Train model
#         model = Prophet(
#             yearly_seasonality=True,
#             weekly_seasonality=False,
#             daily_seasonality=False,
#             changepoint_prior_scale=1.0,
#             seasonality_mode='multiplicative'
#         )
#         model.add_seasonality(name='monthly', period=12, fourier_order=8)
#         model.fit(df_prophet)
        
#         # Forecast
#         future = model.make_future_dataframe(periods=12, freq='MS')
#         forecast = model.predict(future)
        
#         # Create plot
#         fig = go.Figure()
        
#         # Historical data
#         fig.add_trace(go.Scatter(
#             x=df_prophet['ds'],
#             y=df_prophet['y'],
#             mode='lines',
#             name='Historical Inflation',
#             line=dict(color='blue', width=2)
#         ))
        
#         # Forecast
#         forecast_future = forecast[len(df_prophet):]
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat'],
#             mode='lines',
#             name='Forecast',
#             line=dict(color='red', width=2, dash='dash')
#         ))
        
#         # Confidence interval
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat_upper'],
#             mode='lines',
#             name='Upper Bound',
#             line=dict(width=0),
#             showlegend=False
#         ))
        
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat_lower'],
#             mode='lines',
#             name='Lower Bound',
#             fill='tonexty',
#             fillcolor='rgba(255,0,0,0.2)',
#             line=dict(width=0),
#             showlegend=False
#         ))
        
#         fig.update_layout(
#             title='Inflation Forecast - Next 12 Months',
#             xaxis_title='Date',
#             yaxis_title='Inflation Rate (%)',
#             hovermode='x unified',
#             template='plotly_white'
#         )
        
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
#         # Get summary stats
#         latest_actual = df_prophet['y'].iloc[-1]
#         avg_forecast = forecast_future['yhat'].mean()
#         trend = "increasing" if avg_forecast > latest_actual else "decreasing"
        
#         return jsonify({
#             'success': True,
#             'graph': graphJSON,
#             'latest_actual': float(latest_actual),
#             'avg_forecast': float(avg_forecast),
#             'trend': trend,
#             'forecast_data': forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')
#         })
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 400

# # GDP Forecast route
# @app.route('/gdp-forecast')
# def gdp_forecast():
#     return render_template('gdp_forecast.html')

# @app.route('/api/gdp-data')
# def get_gdp_data():
#     """Get GDP forecast data"""
#     try:
#         df_gdp = pd.read_excel("data/gdp_data.xlsx", parse_dates=['Date'])
        
#         # Prepare data
#         df_prophet = df_gdp[['Date', 'GDP_Growth_Rate']].copy()
#         df_prophet['y'] = pd.to_numeric(df_prophet['GDP_Growth_Rate'], errors='coerce')
#         df_prophet['y'] = df_prophet['y'].ffill()
#         df_prophet = df_prophet.rename(columns={'Date': 'ds'})
#         df_prophet = df_prophet.dropna()
        
#         # Train model
#         model = Prophet(
#             yearly_seasonality=True,
#             weekly_seasonality=False,
#             daily_seasonality=False,
#             changepoint_prior_scale=0.8,
#             seasonality_mode='additive'
#         )
#         model.fit(df_prophet)
        
#         # Forecast
#         future = model.make_future_dataframe(periods=12, freq='MS')
#         forecast = model.predict(future)
        
#         # Create plot
#         fig = go.Figure()
        
#         fig.add_trace(go.Scatter(
#             x=df_prophet['ds'],
#             y=df_prophet['y'],
#             mode='lines+markers',
#             name='Historical GDP Growth',
#             line=dict(color='green', width=2)
#         ))
        
#         forecast_future = forecast[len(df_prophet):]
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat'],
#             mode='lines',
#             name='Forecast',
#             line=dict(color='orange', width=2, dash='dash')
#         ))
        
#         fig.update_layout(
#             title='GDP Growth Forecast',
#             xaxis_title='Date',
#             yaxis_title='GDP Growth Rate (%)',
#             hovermode='x unified',
#             template='plotly_white'
#         )
        
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
#         latest_actual = df_prophet['y'].iloc[-1]
#         avg_forecast = forecast_future['yhat'].mean()
        
#         return jsonify({
#             'success': True,
#             'graph': graphJSON,
#             'latest_actual': float(latest_actual),
#             'avg_forecast': float(avg_forecast),
#             'forecast_data': forecast_future[['ds', 'yhat']].to_dict('records')
#         })
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 400

# # Interest Rates Forecast route
# @app.route('/interest-rates-forecast')
# def interest_rates_forecast():
#     return render_template('interest_rates_forecast.html')

# @app.route('/api/interest-rates-data')
# def get_interest_rates_data():
#     """Get interest rates forecast data"""
#     try:
#         rate_type = request.args.get('rate_type', 'Repo_Rate')
        
#         df_rates = pd.read_excel("data/interest_rates_data.xlsx", parse_dates=['Date'])
        
#         # Prepare data
#         df_prophet = df_rates[['Date', rate_type]].copy()
#         df_prophet['y'] = pd.to_numeric(df_prophet[rate_type], errors='coerce')
#         df_prophet['y'] = df_prophet['y'].ffill()
#         df_prophet = df_prophet.rename(columns={'Date': 'ds'})
#         df_prophet = df_prophet.dropna()
        
#         # Train model
#         model = Prophet(
#             yearly_seasonality=True,
#             weekly_seasonality=False,
#             daily_seasonality=False,
#             changepoint_prior_scale=0.5,
#             seasonality_mode='additive'
#         )
#         model.fit(df_prophet)
        
#         # Forecast
#         future = model.make_future_dataframe(periods=12, freq='MS')
#         forecast = model.predict(future)
        
#         # Create plot
#         fig = go.Figure()
        
#         fig.add_trace(go.Scatter(
#             x=df_prophet['ds'],
#             y=df_prophet['y'],
#             mode='lines',
#             name=f'Historical {rate_type}',
#             line=dict(color='purple', width=2)
#         ))
        
#         forecast_future = forecast[len(df_prophet):]
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat'],
#             mode='lines',
#             name='Forecast',
#             line=dict(color='red', width=2, dash='dash')
#         ))
        
#         fig.update_layout(
#             title=f'{rate_type} Forecast',
#             xaxis_title='Date',
#             yaxis_title='Rate (%)',
#             hovermode='x unified',
#             template='plotly_white'
#         )
        
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
#         latest_actual = df_prophet['y'].iloc[-1]
#         avg_forecast = forecast_future['yhat'].mean()
        
#         return jsonify({
#             'success': True,
#             'graph': graphJSON,
#             'latest_actual': float(latest_actual),
#             'avg_forecast': float(avg_forecast),
#             'forecast_data': forecast_future[['ds', 'yhat']].to_dict('records')
#         })
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 400

# # Policy Recommendations route
# @app.route('/policy-recommendations')
# def policy_recommendations():
#     return render_template('policy_recommendations.html')

# @app.route('/api/policy-recommend', methods=['POST'])
# def get_policy_recommendation():
#     """Get policy recommendations based on user profile"""
#     try:
#         data = request.get_json()
        
#         age = int(data.get('age', 30))
#         income = float(data.get('income', 500000))
#         driving_record = data.get('driving_record', 'Clean')
#         smoker = data.get('smoker', 'No')
#         policy_type = data.get('policy_type', 'Health Insurance')
        
#         # Calculate risk score using existing function
#         from risk_assesment import calculate_risk_score
#         risk_score = calculate_risk_score(age, income, driving_record, smoker)
        
#         # Create a comprehensive recommendation without external API dependencies
#         recommendation = generate_policy_recommendation(age, income, driving_record, smoker, policy_type, risk_score)
        
#         return jsonify({
#             'success': True,
#             'risk_score': float(risk_score),
#             'recommendation': recommendation
#         })
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500

# def generate_policy_recommendation(age, income, driving_record, smoker, policy_type, risk_score):
#     """Generate comprehensive policy recommendation based on user profile"""
    
#     # Determine risk category
#     if risk_score <= 3:
#         risk_category = "Low"
#         risk_multiplier = 1.0
#     elif risk_score <= 6:
#         risk_category = "Medium"
#         risk_multiplier = 1.2
#     else:
#         risk_category = "High"
#         risk_multiplier = 1.5
    
#     # Calculate recommended coverage and premium based on policy type
#     if policy_type == "Life Insurance":
#         recommended_coverage = income * 10
#         base_premium = income * 0.02  # 2% of income
#         coverage_description = "10x your annual income for family protection"
        
#     elif policy_type == "Health Insurance":
#         if income < 300000:
#             recommended_coverage = 500000
#         elif income < 800000:
#             recommended_coverage = 1000000
#         else:
#             recommended_coverage = 1500000
#         base_premium = recommended_coverage * 0.015  # 1.5% of coverage
#         coverage_description = "Family floater with comprehensive coverage"
        
#     elif policy_type == "Motor Insurance":
#         # Assuming vehicle value is 20-30% of annual income
#         vehicle_value = income * 0.25
#         recommended_coverage = vehicle_value
#         base_premium = vehicle_value * 0.03  # 3% of vehicle value
#         coverage_description = "Comprehensive motor insurance with zero depreciation"
        
#     else:  # General insurance
#         recommended_coverage = income * 2
#         base_premium = income * 0.01
#         coverage_description = "General insurance coverage"
    
#     # Adjust premium based on risk factors
#     final_premium = base_premium * risk_multiplier
    
#     # Age adjustments
#     if age < 25:
#         final_premium *= 1.1
#     elif age > 50:
#         final_premium *= 1.2
    
#     # Smoking adjustment
#     if smoker == "Yes":
#         final_premium *= 1.3
    
#     # Driving record adjustment for motor insurance
#     if policy_type == "Motor Insurance":
#         if driving_record == "DUI":
#             final_premium *= 2.0
#         elif driving_record == "Accident":
#             final_premium *= 1.5
#         elif driving_record == "Major Violations":
#             final_premium *= 1.8
    
#     # Generate policy recommendations
#     recommendations = []
    
#     if policy_type == "Life Insurance":
#         recommendations = [
#             {
#                 "name": "HDFC Life Click2Protect Super",
#                 "coverage": f"₹{recommended_coverage:,.0f}",
#                 "premium": f"₹{final_premium * 0.8:,.0f}/year",
#                 "features": "Online term plan, high claim settlement ratio",
#                 "best_for": "Young professionals with family responsibilities"
#             },
#             {
#                 "name": "ICICI Prudential iProtect Smart",
#                 "coverage": f"₹{recommended_coverage:,.0f}",
#                 "premium": f"₹{final_premium * 0.9:,.0f}/year",
#                 "features": "Return of premium option, comprehensive coverage",
#                 "best_for": "Those seeking premium return benefits"
#             },
#             {
#                 "name": "SBI Life eShield",
#                 "coverage": f"₹{recommended_coverage:,.0f}",
#                 "premium": f"₹{final_premium:,.0f}/year",
#                 "features": "Government backing, reliable claim settlement",
#                 "best_for": "Conservative investors preferring government backing"
#             }
#         ]
    
#     elif policy_type == "Health Insurance":
#         recommendations = [
#             {
#                 "name": "HDFC ERGO My Health Suraksha",
#                 "coverage": f"₹{recommended_coverage:,.0f}",
#                 "premium": f"₹{final_premium * 0.85:,.0f}/year",
#                 "features": "No room rent limit, day-care procedures covered",
#                 "best_for": "Families seeking comprehensive health coverage"
#             },
#             {
#                 "name": "ICICI Lombard Complete Health Insurance",
#                 "coverage": f"₹{recommended_coverage:,.0f}",
#                 "premium": f"₹{final_premium:,.0f}/year",
#                 "features": "Pre-existing disease coverage, wellness benefits",
#                 "best_for": "Individuals with pre-existing conditions"
#             },
#             {
#                 "name": "Star Health Family Health Optima",
#                 "coverage": f"₹{recommended_coverage:,.0f}",
#                 "premium": f"₹{final_premium * 1.1:,.0f}/year",
#                 "features": "Unlimited restoration, cumulative bonus",
#                 "best_for": "Large families with multiple members"
#             }
#         ]
    
#     elif policy_type == "Motor Insurance":
#         recommendations = [
#             {
#                 "name": "HDFC ERGO Motor Insurance",
#                 "coverage": f"₹{recommended_coverage:,.0f}",
#                 "premium": f"₹{final_premium * 0.9:,.0f}/year",
#                 "features": "Zero depreciation, roadside assistance",
#                 "best_for": "New car owners seeking comprehensive coverage"
#             },
#             {
#                 "name": "ICICI Lombard Bumper to Bumper",
#                 "coverage": f"₹{recommended_coverage:,.0f}",
#                 "premium": f"₹{final_premium:,.0f}/year",
#                 "features": "Complete car protection, engine protection",
#                 "best_for": "Those wanting maximum protection for their vehicle"
#             },
#             {
#                 "name": "Bajaj Allianz Motor Insurance",
#                 "coverage": f"₹{recommended_coverage:,.0f}",
#                 "premium": f"₹{final_premium * 1.05:,.0f}/year",
#                 "features": "Quick claim settlement, extensive garage network",
#                 "best_for": "Frequent travelers and commercial vehicle users"
#             }
#         ]
    
#     # Create the formatted recommendation
#     recommendation_text = f"""
# ## 🛡️ Policy Recommendations for {policy_type}

# ### 📊 Risk Assessment
# - **Age Group**: {age} years
# - **Income Level**: ₹{income:,}/year
# - **Risk Category**: {risk_category}
# - **Risk Score**: {risk_score}/10
# - **Driving Record**: {driving_record}
# - **Smoker**: {smoker}

# ### 💡 Recommended Coverage
# - **Suggested Coverage**: ₹{recommended_coverage:,}
# - **Estimated Premium Range**: ₹{final_premium * 0.8:,.0f} - ₹{final_premium * 1.2:,.0f}/year
# - **Coverage Type**: {coverage_description}

# ### 🏆 Top 3 Policy Recommendations

# """
    
#     for i, policy in enumerate(recommendations, 1):
#         recommendation_text += f"""
# **{i}. {policy['name']}**
# - 💰 **Coverage**: {policy['coverage']}
# - 💸 **Premium**: {policy['premium']}
# - ✨ **Key Features**: {policy['features']}
# - 🎯 **Best For**: {policy['best_for']}
# """
    
#     recommendation_text += f"""

# ### 📋 Next Steps
# 1. **Compare Quotes**: Get personalized quotes from multiple insurers
# 2. **Read Policy Terms**: Carefully review coverage details and exclusions
# 3. **Check Claim Ratio**: Verify insurer's claim settlement ratio
# 4. **Consider Riders**: Add relevant riders for comprehensive protection
# 5. **Annual Review**: Review your policy annually and adjust coverage as needed

# ### ⚠️ Important Notes
# - Premiums may vary based on exact age, health, and other underwriting factors
# - Always disclose accurate information during application
# - Consider increasing coverage with income growth
# - Review policy terms and conditions before purchase

# *This recommendation is based on general guidelines. Please consult with a certified insurance advisor for personalized advice.*
# """
    
#     return recommendation_text

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

# from flask import Flask, render_template, request, jsonify
# import pandas as pd
# from datetime import datetime
# from prophet import Prophet
# import plotly.graph_objects as go
# import plotly
# import json
# import numpy as np
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # ✅ fixes browser "Failed to fetch" due to CORS

# # Main route - Home page with cards
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Financial Advisor route
# @app.route('/financial-advisor')
# def financial_advisor():
#     return render_template('financial_advisor.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     """Process financial advisor analysis"""
#     try:
#         # Get form data
#         data = request.get_json()
        
#         age = int(data.get('age', 32))
#         marital_status = data.get('marital_status', 'Single')
#         dependents = int(data.get('dependents', 2))
#         annual_income = float(data.get('annual_income', 800000))
#         monthly_expenses = float(data.get('monthly_expenses', 40000))
#         current_coverage = float(data.get('current_coverage', 5000000))
#         annual_premium = float(data.get('annual_premium', 25000))
#         accident_cover = float(data.get('accident_cover', 1000000))
#         critical_illness = float(data.get('critical_illness', 500000))
#         home_loan = float(data.get('home_loan', 2000000))
#         other_debts = float(data.get('other_debts', 0))
#         inflation_rate = float(data.get('inflation_rate', 6.5))
        
#         # Perform calculations
#         analysis = calculate_analysis(
#             age, marital_status, dependents, annual_income, monthly_expenses,
#             current_coverage, annual_premium, accident_cover, critical_illness,
#             home_loan, other_debts, inflation_rate
#         )
        
#         return jsonify({
#             'success': True,
#             'analysis': analysis
#         })
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/generate-report', methods=['POST'])
# def generate_report():
#     """Generate detailed financial report"""
#     try:
#         data = request.get_json()
        
#         age = int(data.get('age', 32))
#         marital_status = data.get('marital_status', 'Single')
#         dependents = int(data.get('dependents', 2))
#         annual_income = float(data.get('annual_income', 800000))
#         monthly_expenses = float(data.get('monthly_expenses', 40000))
#         current_coverage = float(data.get('current_coverage', 5000000))
#         annual_premium = float(data.get('annual_premium', 25000))
#         home_loan = float(data.get('home_loan', 2000000))
#         other_debts = float(data.get('other_debts', 0))
#         critical_illness = float(data.get('critical_illness', 500000))
#         accident_cover = float(data.get('accident_cover', 1000000))
#         inflation_rate = float(data.get('inflation_rate', 6.5))
        
#         report = generate_detailed_analysis(
#             age, marital_status, dependents, annual_income, monthly_expenses, 
#             current_coverage, annual_premium, home_loan, other_debts,
#             critical_illness, accident_cover, inflation_rate
#         )
        
#         return jsonify({
#             'success': True,
#             'report': report
#         })
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# def calculate_analysis(age, marital_status, dependents, annual_income, monthly_expenses,
#                        current_coverage, annual_premium, accident_cover, critical_illness,
#                        home_loan, other_debts, inflation_rate):
#     """Calculate financial analysis metrics"""
    
#     # Basic calculations
#     annual_expenses = monthly_expenses * 12
#     net_savings = annual_income - annual_expenses
    
#     # Adjust recommended coverage based on age, marital status, and dependents
#     base_multiplier = 10
#     if marital_status == 'Married':
#         base_multiplier += 2
#     if dependents > 0:
#         base_multiplier += (dependents * 1)
#     if age < 30:
#         base_multiplier += 1
#     elif age > 50:
#         base_multiplier -= 1
    
#     recommended_min = annual_income * base_multiplier
#     recommended_max = annual_income * (base_multiplier + 5)
    
#     premium_percentage = (annual_premium / annual_income) * 100 if annual_income > 0 else 0
#     total_debts = home_loan + other_debts
    
#     # Coverage assessment
#     coverage_gap = max(0, recommended_min - current_coverage)
#     is_underinsured = coverage_gap > 0
    
#     # Premium affordability
#     max_affordable_premium = annual_income * 0.1  # 10% of income
#     additional_premium_capacity = max_affordable_premium - annual_premium
    
#     # Future expenses with inflation
#     future_expenses_10y = annual_expenses * ((1 + inflation_rate/100) ** 10)
    
#     # Recommended critical illness cover (adjusted for age)
#     recommended_ci = annual_income * 3
#     if age > 45:
#         recommended_ci = annual_income * 4  # Higher for older age
    
#     # Calculate scores
#     coverage_score = min(10, (current_coverage / recommended_min) * 10)
#     premium_score = 10 if premium_percentage < 5 else 8 if premium_percentage < 10 else 5
#     debt_score = 10 if total_debts < annual_income else 7 if total_debts < annual_income * 2 else 4
#     savings_score = 10 if net_savings > annual_income * 0.3 else 7 if net_savings > annual_income * 0.2 else 4
#     overall_score = (coverage_score + premium_score + debt_score + savings_score) / 4
    
#     # Savings and debt metrics
#     savings_rate = (net_savings / annual_income * 100) if annual_income > 0 else 0
#     debt_to_income = (total_debts / annual_income) if annual_income > 0 else 0
    
#     # Affordability status
#     affordability_status = "Highly Affordable" if premium_percentage < 5 else "Affordable" if premium_percentage < 10 else "High"
    
#     # Critical illness gap
#     ci_gap = max(0, recommended_ci - critical_illness)
    
#     # Recommendations based on profile
#     recommendations = []
    
#     if is_underinsured:
#         recommendations.append(f"🎯 **Increase Life Insurance Coverage** to ₹{recommended_min:,.0f} (minimum) to adequately protect your family.")
    
#     if marital_status == 'Married' and dependents > 0:
#         recommendations.append(f"👨‍👩‍👧 **Family Protection Priority** - As you have {dependents} dependent(s), ensure adequate coverage for their future needs.")
    
#     if critical_illness < recommended_ci:
#         recommendations.append(f"🏥 **Enhance Critical Illness Cover** to ₹{recommended_ci:,.0f} ({'4x' if age > 45 else '3x'} your annual income).")
    
#     if age < 35:
#         recommendations.append("💼 **Start Early Advantage** - Lock in lower premiums while you're young and healthy.")
#     elif age > 50:
#         recommendations.append("⏰ **Age Factor** - Consider comprehensive health riders as medical risks increase with age.")
    
#     if net_savings < annual_income * 0.2:
#         recommendations.append("💰 **Improve Savings Rate** - Aim to save at least 20% of your income for long-term financial security.")
    
#     if total_debts > annual_income * 2:
#         recommendations.append("📉 **Debt Management** - Your debt-to-income ratio is high. Ensure coverage includes debt protection.")
    
#     recommendations.append("📊 **Build Emergency Fund** - Maintain 6 months of expenses as emergency fund.")
#     recommendations.append("🔄 **Review Annually** - Review and adjust your insurance coverage every year to account for inflation and life changes.")
    
#     return {
#         'age': age,
#         'marital_status': marital_status,
#         'dependents': dependents,
#         'annual_expenses': annual_expenses,
#         'net_savings': net_savings,
#         'recommended_min': recommended_min,
#         'recommended_max': recommended_max,
#         'base_multiplier': base_multiplier,
#         'premium_percentage': premium_percentage,
#         'total_debts': total_debts,
#         'coverage_gap': coverage_gap,
#         'is_underinsured': is_underinsured,
#         'additional_premium_capacity': additional_premium_capacity,
#         'future_expenses_10y': future_expenses_10y,
#         'recommended_ci': recommended_ci,
#         'coverage_score': coverage_score,
#         'premium_score': premium_score,
#         'debt_score': debt_score,
#         'savings_score': savings_score,
#         'overall_score': overall_score,
#         'savings_rate': savings_rate,
#         'debt_to_income': debt_to_income,
#         'affordability_status': affordability_status,
#         'ci_gap': ci_gap,
#         'recommendations': recommendations,
#         'max_affordable_premium': max_affordable_premium
#     }

# def generate_detailed_analysis(age, marital_status, dependents, annual_income, monthly_expenses, 
#                               current_coverage, annual_premium, home_loan, other_debts,
#                               critical_illness, accident_cover, inflation_rate):
#     """Generate detailed analysis using financial rules"""
    
#     # Calculations
#     annual_expenses = monthly_expenses * 12
    
#     # Adjust multiplier based on profile
#     base_multiplier = 10
#     if marital_status == 'Married':
#         base_multiplier += 2
#     if dependents > 0:
#         base_multiplier += (dependents * 1)
#     if age < 30:
#         base_multiplier += 1
#     elif age > 50:
#         base_multiplier -= 1
    
#     recommended_min = annual_income * base_multiplier
#     recommended_max = annual_income * (base_multiplier + 5)
#     premium_percentage = (annual_premium / annual_income) * 100
#     total_debts = home_loan + other_debts
    
#     # Coverage gap
#     coverage_gap = max(0, recommended_min - current_coverage)
    
#     # Future expenses with inflation
#     inflation_decimal = inflation_rate / 100
#     future_expenses_10y = annual_expenses * ((1 + inflation_decimal) ** 10)
    
#     # Recommended critical illness cover
#     recommended_ci = annual_income * 3 if age <= 45 else annual_income * 4
    
#     # Generate detailed report
#     report = f"""
# ## 🏦 FINANCIAL ADVISORY ANALYSIS REPORT

# ### CLIENT PROFILE
# ---
# **Age:** {age} years  
# **Marital Status:** {marital_status}  
# **Dependents:** {dependents}  
# **Annual Income:** ₹{annual_income:,}  
# **Life Stage:** {"Young Professional" if age < 35 else "Mid-Career" if age < 50 else "Pre-Retirement"}

# ### 1. COVERAGE ADEQUACY ASSESSMENT
# ---
# **Current Coverage:** ₹{current_coverage:,} ({current_coverage/annual_income:.1f}x income)  
# **Recommended Range:** ₹{recommended_min:,} - ₹{recommended_max:,} ({base_multiplier}-{base_multiplier+5}x income)  
# **Multiplier Applied:** {base_multiplier}x (Base 10x + Adjustments)  
# **Assessment:** {"**⚠️ UNDERINSURED**" if coverage_gap > 0 else "**✅ ADEQUATE**"}  
# **Coverage Gap:** ₹{coverage_gap:,}  
# **Risk Factors:** Home loan ₹{home_loan:,} + Other debts ₹{other_debts:,} + {dependents} dependents  

# **Multiplier Breakdown:**
# - Base Coverage: 10x income
# {f"- Married: +2x income" if marital_status == "Married" else ""}
# {f"- Dependents ({dependents}): +{dependents}x income" if dependents > 0 else ""}
# {f"- Young Age Bonus: +1x income" if age < 30 else f"- Age Adjustment: -1x income" if age > 50 else ""}

# {"🎯 **RECOMMENDATION:** Increase coverage by ₹" + f"{coverage_gap:,}" if coverage_gap > 0 else "✅ **STATUS:** Current coverage is adequate"}

# ### 2. PREMIUM AFFORDABILITY ANALYSIS
# ---
# **Current Premium:** ₹{annual_premium:,} ({premium_percentage:.1f}% of income)  
# **Affordability:** {"**Highly Affordable** 🟢" if premium_percentage < 5 else "**Affordable** 🟡" if premium_percentage < 10 else "**High** 🔴"}  
# **Maximum Recommended:** ₹{annual_income * 0.1:,} (10% of income)  
# **Additional Capacity:** ₹{(annual_income * 0.1) - annual_premium:,}  

# 💡 **RECOMMENDATION:** You can afford additional ₹{(annual_income * 0.1) - annual_premium:,} in premiums for more coverage

# ### 3. RIDER ANALYSIS
# ---
# **Critical Illness Cover:** ₹{critical_illness:,} (Current)  
# **Recommended CI Cover:** ₹{recommended_ci:,} ({'4x income (age >45)' if age > 45 else '3x income'})  
# **Accidental Death:** ₹{accident_cover:,} {"✅ (Adequate)" if accident_cover >= current_coverage * 2 else "⚠️ (Consider increasing)"}  

# 🏥 **RECOMMENDATION:** {"Increase Critical Illness cover to ₹" + f"{recommended_ci:,}" if critical_illness < recommended_ci else "Critical illness coverage is adequate"}

# ### 4. FAMILY PROTECTION ANALYSIS
# ---
# **Marital Status:** {marital_status}  
# **Number of Dependents:** {dependents}  
# **Monthly Family Expenses:** ₹{monthly_expenses:,}  
# **Annual Family Expenses:** ₹{annual_expenses:,}  
# **Total Debt Burden:** ₹{total_debts:,}  

# 📊 **FAMILY PROTECTION NEEDS:**
# {f"- Spouse support for {65 - age} years" if marital_status == "Married" else ""}
# {f"- Child education & marriage: ₹{dependents * 2000000:,}" if dependents > 0 else ""}
# - Emergency fund: ₹{monthly_expenses * 6:,} (6 months)
# - Debt coverage: ₹{total_debts:,}

# ### 5. INFLATION PROTECTION STRATEGY
# ---
# **Current Annual Expenses:** ₹{annual_expenses:,}  
# **Expenses in 10 years ({inflation_rate}% inflation):** ₹{future_expenses_10y:,}  
# **Inflation Impact:** {((future_expenses_10y/annual_expenses - 1) * 100):.1f}% increase over 10 years  

# 📈 **STRATEGIES:**
# - Increase coverage by 8-10% every 3 years
# - Start SIP of ₹{int(annual_income * 0.02):,}/month in equity mutual funds
# - Maximize PPF contribution (₹1.5L annually)
# - Consider ULIP with top-up facility

# ### 6. AGE-BASED RECOMMENDATIONS
# ---
# **Current Age:** {age} years  
# **Retirement Age:** 60 years  
# **Years to Retirement:** {60 - age} years  

# """

#     if age < 35:
#         report += """
# **🌟 YOUNG PROFESSIONAL ADVANTAGES:**
# - Lock in lower premiums now (premiums increase 3-5% per age year)
# - Longer investment horizon for wealth building
# - Higher risk appetite for equity investments
# - Time to build substantial corpus through compounding
# - Consider 30-40 year term plans for maximum protection
# """
#     elif age < 50:
#         report += """
# **💼 MID-CAREER FOCUS:**
# - Peak earning years - maximize savings and investments
# - Review and increase coverage to match income growth
# - Balance between protection and wealth accumulation
# - Consider 20-25 year term plans
# - Focus on debt reduction strategies
# """
#     else:
#         report += """
# **⏰ PRE-RETIREMENT PRIORITIES:**
# - Ensure adequate health insurance coverage
# - Focus on debt elimination before retirement
# - Build retirement corpus aggressively
# - Consider 10-15 year term plans
# - Increase critical illness and health riders
# """

#     report += f"""

# ### 7. IMMEDIATE ACTION PLAN
# ---
# **🎯 Priority 1 (Next 30 days):**
# - Increase term insurance to ₹{recommended_min:,}
# - Build emergency fund: ₹{monthly_expenses * 6:,} (6 months expenses)
# {f"- Review family health insurance for {dependents + (2 if marital_status == 'Married' else 1)} members" if dependents > 0 or marital_status == "Married" else ""}

# **📋 Priority 2 (Next 90 days):**
# - Enhance Critical Illness cover to ₹{recommended_ci:,}
# - Start monthly SIP of ₹{int(annual_income * 0.02):,} in diversified equity funds
# {f"- Create education fund for {dependents} dependent(s)" if dependents > 0 else ""}

# **📅 Priority 3 (Next 6 months):**
# - Review and optimize home loan prepayment strategy
# - Set up automatic premium payments with annual increases
# - Create succession planning documents (will, nominations)

# ### 8. FINANCIAL HEALTH SCORE
# ---
# """
    
#     # Calculate scores
#     insurance_score = min(10, (current_coverage / recommended_min) * 10)
#     premium_score = 9 if premium_percentage < 5 else 7 if premium_percentage < 10 else 4
#     debt_score = 7 if total_debts < annual_income * 2 else 5 if total_debts < annual_income * 3 else 3
#     net_savings = annual_income - annual_expenses
#     savings_score = 9 if net_savings > annual_income * 0.3 else 7 if net_savings > annual_income * 0.2 else 4
#     overall_score = (insurance_score + premium_score + debt_score + savings_score) / 4
    
#     report += f"""
# **Insurance Coverage:** {insurance_score:.1f}/10 {"(Underinsured)" if insurance_score < 8 else "(Good)" if insurance_score < 10 else "(Excellent)"}  
# **Premium Affordability:** {premium_score:.1f}/10 {"(Highly affordable)" if premium_score >= 8 else "(Affordable)" if premium_score >= 6 else "(High)"}  
# **Debt Management:** {debt_score:.1f}/10 {"(Manageable)" if debt_score >= 6 else "(Needs attention)"}  
# **Savings Rate:** {savings_score:.1f}/10 {"(Excellent)" if savings_score >= 8 else "(Good)" if savings_score >= 6 else "(Needs improvement)"}  
# **Overall Score:** {overall_score:.1f}/10 {"🟢 **Good foundation, needs enhancement**" if overall_score >= 6 else "🟡 **Needs improvement**"}

# ### 9. KEY TAKEAWAYS
# ---
# ✅ **Strengths:**
# {f"- Premium is highly affordable at {premium_percentage:.1f}% of income" if premium_percentage < 5 else f"- Premium is manageable at {premium_percentage:.1f}% of income" if premium_percentage < 10 else ""}
# {f"- Good debt management (Debt-to-Income: {total_debts/annual_income:.1f}x)" if total_debts < annual_income * 2 else ""}
# {f"- Strong savings rate: {(net_savings/annual_income*100):.1f}%" if net_savings > annual_income * 0.2 else ""}

# ⚠️ **Areas for Improvement:**
# {f"- Coverage gap of ₹{coverage_gap:,}" if coverage_gap > 0 else ""}
# {f"- Critical illness cover needs enhancement" if critical_illness < recommended_ci else ""}
# {f"- High debt-to-income ratio ({total_debts/annual_income:.1f}x)" if total_debts > annual_income * 2 else ""}
# {f"- Savings rate needs improvement ({(net_savings/annual_income*100):.1f}%)" if net_savings < annual_income * 0.2 else ""}

# ---
# *This analysis is based on standard financial planning principles and considers your age ({age}), marital status ({marital_status}), and dependents ({dependents}). Please consult a certified financial planner for personalized advice.*
# """
    
#     return report

# # Inflation Forecast route
# @app.route('/inflation-forecast')
# def inflation_forecast():
#     return render_template('inflation_forecast.html')

# @app.route('/api/inflation-data')
# def get_inflation_data():
#     """Get inflation forecast data"""
#     try:
#         df_all = pd.read_excel("data/df_all.xlsx", parse_dates=['Month'])
        
#         # Prepare data for Prophet
#         df_prophet = df_all[['Month', 'Combined Inflation (%)']].copy()
#         df_prophet['y'] = pd.to_numeric(df_prophet['Combined Inflation (%)'], errors='coerce')
#         df_prophet['y'] = df_prophet['y'].ffill()
#         df_prophet = df_prophet.rename(columns={'Month': 'ds'})
        
#         # Train model
#         model = Prophet(
#             yearly_seasonality=True,
#             weekly_seasonality=False,
#             daily_seasonality=False,
#             changepoint_prior_scale=1.0,
#             seasonality_mode='multiplicative'
#         )
#         model.add_seasonality(name='monthly', period=12, fourier_order=8)
#         model.fit(df_prophet)
        
#         # Forecast
#         future = model.make_future_dataframe(periods=12, freq='MS')
#         forecast = model.predict(future)
        
#         # Create plot
#         fig = go.Figure()
        
#         # Historical data
#         fig.add_trace(go.Scatter(
#             x=df_prophet['ds'],
#             y=df_prophet['y'],
#             mode='lines',
#             name='Historical Inflation',
#             line=dict(color='blue', width=2)
#         ))
        
#         # Forecast
#         forecast_future = forecast[len(df_prophet):]
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat'],
#             mode='lines',
#             name='Forecast',
#             line=dict(color='red', width=2, dash='dash')
#         ))
        
#         # Confidence interval
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat_upper'],
#             mode='lines',
#             name='Upper Bound',
#             line=dict(width=0),
#             showlegend=False
#         ))
        
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat_lower'],
#             mode='lines',
#             name='Lower Bound',
#             fill='tonexty',
#             fillcolor='rgba(255,0,0,0.2)',
#             line=dict(width=0),
#             showlegend=False
#         ))
        
#         fig.update_layout(
#             title='Inflation Forecast - Next 12 Months',
#             xaxis_title='Date',
#             yaxis_title='Inflation Rate (%)',
#             hovermode='x unified',
#             template='plotly_white'
#         )
        
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
#         # Get summary stats
#         latest_actual = df_prophet['y'].iloc[-1]
#         avg_forecast = forecast_future['yhat'].mean()
#         trend = "increasing" if avg_forecast > latest_actual else "decreasing"
        
#         return jsonify({
#             'success': True,
#             'graph': graphJSON,
#             'latest_actual': float(latest_actual),
#             'avg_forecast': float(avg_forecast),
#             'trend': trend,
#             'forecast_data': forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')
#         })
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 400

# # GDP Forecast route
# @app.route('/gdp-forecast')
# def gdp_forecast():
#     return render_template('gdp_forecast.html')

# @app.route('/api/gdp-data')
# def get_gdp_data():
#     """Get GDP forecast data"""
#     try:
#         df_gdp = pd.read_excel("data/gdp_data.xlsx", parse_dates=['Date'])
        
#         # Prepare data
#         df_prophet = df_gdp[['Date', 'GDP_Growth_Rate']].copy()
#         df_prophet['y'] = pd.to_numeric(df_prophet['GDP_Growth_Rate'], errors='coerce')
#         df_prophet['y'] = df_prophet['y'].ffill()
#         df_prophet = df_prophet.rename(columns={'Date': 'ds'})
#         df_prophet = df_prophet.dropna()
        
#         # Train model
#         model = Prophet(
#             yearly_seasonality=True,
#             weekly_seasonality=False,
#             daily_seasonality=False,
#             changepoint_prior_scale=0.8,
#             seasonality_mode='additive'
#         )
#         model.fit(df_prophet)
        
#         # Forecast
#         future = model.make_future_dataframe(periods=12, freq='MS')
#         forecast = model.predict(future)
        
#         # Create plot
#         fig = go.Figure()
        
#         fig.add_trace(go.Scatter(
#             x=df_prophet['ds'],
#             y=df_prophet['y'],
#             mode='lines+markers',
#             name='Historical GDP Growth',
#             line=dict(color='green', width=2)
#         ))
        
#         forecast_future = forecast[len(df_prophet):]
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat'],
#             mode='lines',
#             name='Forecast',
#             line=dict(color='orange', width=2, dash='dash')
#         ))
        
#         fig.update_layout(
#             title='GDP Growth Forecast',
#             xaxis_title='Date',
#             yaxis_title='GDP Growth Rate (%)',
#             hovermode='x unified',
#             template='plotly_white'
#         )
        
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
#         latest_actual = df_prophet['y'].iloc[-1]
#         avg_forecast = forecast_future['yhat'].mean()
        
#         return jsonify({
#             'success': True,
#             'graph': graphJSON,
#             'latest_actual': float(latest_actual),
#             'avg_forecast': float(avg_forecast),
#             'forecast_data': forecast_future[['ds', 'yhat']].to_dict('records')
#         })
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 400

# # Interest Rates Forecast route
# @app.route('/interest-rates-forecast')
# def interest_rates_forecast():
#     return render_template('interest_rates_forecast.html')

# @app.route('/api/interest-rates-data')
# def get_interest_rates_data():
#     """Get interest rates forecast data"""
#     try:
#         rate_type = request.args.get('rate_type', 'Repo_Rate')
        
#         df_rates = pd.read_excel("data/interest_rates_data.xlsx", parse_dates=['Date'])
        
#         # Prepare data
#         df_prophet = df_rates[['Date', rate_type]].copy()
#         df_prophet['y'] = pd.to_numeric(df_prophet[rate_type], errors='coerce')
#         df_prophet['y'] = df_prophet['y'].ffill()
#         df_prophet = df_prophet.rename(columns={'Date': 'ds'})
#         df_prophet = df_prophet.dropna()
        
#         # Train model
#         model = Prophet(
#             yearly_seasonality=True,
#             weekly_seasonality=False,
#             daily_seasonality=False,
#             changepoint_prior_scale=0.5,
#             seasonality_mode='additive'
#         )
#         model.fit(df_prophet)
        
#         # Forecast
#         future = model.make_future_dataframe(periods=12, freq='MS')
#         forecast = model.predict(future)
        
#         # Create plot
#         fig = go.Figure()
        
#         fig.add_trace(go.Scatter(
#             x=df_prophet['ds'],
#             y=df_prophet['y'],
#             mode='lines',
#             name=f'Historical {rate_type}',
#             line=dict(color='purple', width=2)
#         ))
        
#         forecast_future = forecast[len(df_prophet):]
#         fig.add_trace(go.Scatter(
#             x=forecast_future['ds'],
#             y=forecast_future['yhat'],
#             mode='lines',
#             name='Forecast',
#             line=dict(color='red', width=2, dash='dash')
#         ))
        
#         fig.update_layout(
#             title=f'{rate_type} Forecast',
#             xaxis_title='Date',
#             yaxis_title='Rate (%)',
#             hovermode='x unified',
#             template='plotly_white'
#         )
        
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
#         latest_actual = df_prophet['y'].iloc[-1]
#         avg_forecast = forecast_future['yhat'].mean()
        
#         return jsonify({
#             'success': True,
#             'graph': graphJSON,
#             'latest_actual': float(latest_actual),
#             'avg_forecast': float(avg_forecast),
#             'forecast_data': forecast_future[['ds', 'yhat']].to_dict('records')
#         })
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 400

# # Policy Recommendations route
# @app.route('/policy-recommendations')
# def policy_recommendations():
#     return render_template('policy_recommendations.html')

# @app.route('/api/policy-recommend', methods=['POST'])
# def get_policy_recommendation():
#     """Generate policy recommendations based on user profile"""
#     try:
#         from risk_assesment import calculate_risk_score
#         from search_serp import get_policy_recommendations_from_serpapi
#         from utils import build_prompt_with_search
#         from gemini_llm import query_gemini

#         data = request.get_json()

#         # Extract safely
#         age = int(data.get('age', 30))
#         gender = data.get('gender', 'Male')
#         occupation = data.get('occupation', 'Employee')
#         income = float(data.get('income', 500000))
#         smoker = data.get('smoker', 'No')
#         driving_record = data.get('driving_record', 'Clean')
#         policy_type = data.get('policy_type', 'Health Insurance')
#         disease = data.get('disease', 'None')
#         dependents = int(data.get('dependents', 0))

#         # 1️⃣ Calculate risk
#         risk_category = calculate_risk_score(age, income, driving_record, smoker, disease, dependents)

#         # 2️⃣ Build profile
#         user_profile = {
#             "Age": age,
#             "Gender": gender,
#             "Occupation": occupation,
#             "Income Level": income,
#             "Insurance Type": policy_type,
#             "Smoker": smoker,
#             "Driving Record": driving_record,
#             "Pre-existing Condition": disease,
#             "Dependents": dependents,
#             "Risk Category": risk_category,
#         }

#         # 3️⃣ SERP results
#         search_results = get_policy_recommendations_from_serpapi(user_profile)
#         if not search_results:
#             search_results = [{"title": "No results found", "link": "", "snippet": ""}]

#         # 4️⃣ Prompt + LLM
#         prompt = build_prompt_with_search(user_profile, search_results)
#         recommendation = query_gemini(prompt)

#         # 5️⃣ Return response
#         return jsonify({
#             "success": True,
#             "risk_category": risk_category,
#             "recommendation": recommendation
#         }), 200

#     except Exception as e:
#         print("Error in /api/policy-recommend:", str(e))
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "recommendation": f"""
# ## Policy Recommendations (Fallback)
# ### Risk Summary
# - Age: {data.get('age', 30)}
# - Income: ₹{data.get('income', 500000)}
# - Smoker: {data.get('smoker', 'No')}
# - Driving Record: {data.get('driving_record', 'Clean')}
# - Dependents: {data.get('dependents', 0)}
# - Risk Score: Medium (Fallback)
# ### Suggested Coverage
# - Coverage: ₹{int(float(data.get('income', 500000))) * 10:,}
# - Term: 20–30 years
# - Premium: ₹{int(float(data.get('income', 500000))) * 0.05:,}/year
# > *This is an auto-generated fallback suggestion. Please try again for personalized insights.*
# """
#         }), 200

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)


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