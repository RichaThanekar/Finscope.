// import React from 'react';
// import Navbar from '../components/Navbar';
// import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

// const modules = [
//   {
//     title: 'Economic Trend Analyzer',
//     icon: '📊',
//     description: 'Shows users historical + forecasted economic indicators like inflation, GDP, interest rates that directly affect their savings, investments, and insurance premiums.',
//     tech: 'Time-series forecasting models → ARIMA, Facebook Prophet.',
//     benefit: 'Helps users see how inflation erodes money value and how GDP/interest rates affect their policies/investments.',
//   },
//   {
//     title: 'Insurance Policy Analyzer & Gap Finder',
//     icon: '🛡️',
//     description: 'Reads user’s uploaded insurance policy PDF, extracts key details (premium, coverage, riders), and checks if coverage matches their life stage & income.',
//     tech: 'NLP (LLM / LangChain + pdfplumber) → extract policy details.',
//     benefit: 'Removes dependency on agents who often mis-sell, gives unbiased, data-driven analysis.',
//   },
//   {
//     title: 'Premium Affordability Calculator',
//     icon: '🧮',
//     description: 'Helps middle-class users check whether their insurance premiums fit into their budget. Prevents over-buying policies that strain monthly income.',
//     tech: 'Rule-based affordability rule: Premium ≤ 10–15% of monthly income.',
//     benefit: 'Makes financial planning practical & family-friendly.',
//   },
//   {
//     title: 'Investment Portfolio Advisor',
//     icon: '💹',
//     description: 'Recommends personalized portfolios (SIP, mutual funds, FD, gold) based on user’s goals, risk profile, and inflation forecast.',
//     tech: 'Risk profiling → clustering / decision tree.',
//     benefit: 'Ensures users don’t just invest blindly but know future real growth of money.',
//   },
// ];

// const AboutPage = () => {
//   return (
//     <div className="bg-slate-50 min-h-screen">
//       <Navbar />
//       <div className="container mx-auto p-8">
//         <header className="text-center mb-12">
//           <h1 className="text-4xl font-bold text-gray-800">
//             🌐 Forecasting & Personalized Financial Wellness Platform
//           </h1>
//           <p className="text-lg text-gray-600 mt-4 max-w-3xl mx-auto">
//             A fintech web platform that helps individuals and families make smarter financial decisions by combining economic forecasting, insurance gap detection, investment advising, and affordability analysis.
//           </p>
//         </header>

//         <section>
//           <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">📌 Modules Breakdown</h2>
//           <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
//             {modules.map((mod, index) => (
//               <Card key={index} className="shadow-lg hover:shadow-xl transition-shadow duration-300">
//                 <CardHeader>
//                   <CardTitle className="flex items-center text-2xl">
//                     <span className="text-3xl mr-3">{mod.icon}</span>
//                     {mod.title}
//                   </CardTitle>
//                 </CardHeader>
//                 <CardContent>
//                   <p className="text-gray-700 mb-4">{mod.description}</p>
//                   <p className="text-sm text-gray-600 mb-2"><strong className="font-semibold">ML/Tech Used:</strong> {mod.tech}</p>
//                   <p className="text-sm text-green-700 bg-green-100 p-2 rounded">👉 {mod.benefit}</p>
//                 </CardContent>
//               </Card>
//             ))}
//           </div>
//         </section>

//         <section className="mt-16">
//           <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">🔄 Project Flow</h2>
//           <div className="bg-white p-6 rounded-lg shadow-md">
//             <ul className="list-decimal list-inside space-y-3 text-gray-700">
//               <li>User Login/Register (via website).</li>
//               <li>Upload Policy PDF + Enter Personal & Financial Details (income, expenses, dependents, goals).</li>
//               <li>Backend Processing: NLP extracts policy, forecasts trends, checks affordability, and advises on portfolios.</li>
//               <li>Dashboard Output: Graphs, policy insights, affordability status, and investment suggestions are displayed.</li>
//               <li>Downloadable Report with charts + insights.</li>
//             </ul>
//           </div>
//         </section>

//         <div className="grid md:grid-cols-2 gap-8 mt-16">
//             <section>
//               <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">🎯 Target Users</h2>
//               <div className="bg-white p-6 rounded-lg shadow-md h-full">
//                 <ul className="list-disc list-inside space-y-2 text-gray-700">
//                   <li>Middle-class individuals/families concerned about premiums & affordability.</li>
//                   <li>Young professionals wanting investment + insurance advice.</li>
//                   <li>Financially aware users who want independent, data-driven advice.</li>
//                 </ul>
//               </div>
//             </section>

//             <section>
//               <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">🚀 Why It’s a Major Project</h2>
//               <div className="bg-white p-6 rounded-lg shadow-md h-full">
//                 <ul className="list-disc list-inside space-y-2 text-gray-700">
//                   <li>An end-to-end fintech ecosystem, not just a single module.</li>
//                   <li>Uses diverse techniques like ML models, NLP, and forecasting.</li>
//                   <li>Solves a genuine problem: financial literacy and independent decision-making.</li>
//                   <li>User-centric, with clear visuals (graphs, dashboards).</li>
//                 </ul>
//               </div>
//             </section>
//         </div>

//       </div>
//     </div>
//   );
// };

// export default AboutPage;

import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

const styles = `
.hero-section { 
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
  padding: 80px 30px; 
  text-align: center; 
  color: white; 
  position: relative;
  overflow: hidden;
}
.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%);
}
.hero-section h1 { 
  font-size: 3.5rem; 
  margin-bottom: 20px; 
  font-weight: 900; 
  position: relative;
  z-index: 1;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}
.hero-section p { 
  font-size: 1.4rem; 
  margin-bottom: 30px; 
  opacity: 0.95; 
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}
.about-container { 
  max-width: 1400px; 
  margin: 0 auto; 
  padding: 60px 30px; 
}
.section-title { 
  color: #2e7d32; 
  font-size: 2.8rem; 
  margin-bottom: 20px; 
  text-align: center; 
  font-weight: 900;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}
.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 2px;
}
.section-subtitle {
  text-align: center;
  color: #666;
  font-size: 1.3rem;
  margin-bottom: 50px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}
.modules-grid { 
  display: grid; 
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); 
  gap: 35px; 
  margin-bottom: 60px; 
}
.module-card { 
  background: white; 
  border-radius: 20px; 
  padding: 35px; 
  box-shadow: 0 10px 40px rgba(0,0,0,0.08); 
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
  border-top: 6px solid;
  position: relative;
  overflow: hidden;
}
.module-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  transform: translate(30%, -30%);
}
.module-card:hover { 
  transform: translateY(-10px) scale(1.02); 
  box-shadow: 0 20px 60px rgba(0,0,0,0.15); 
}
.module-card.advisor { border-top-color: #00d2d3; }
.module-card.inflation { border-top-color: #ff6b6b; }
.module-card.gdp { border-top-color: #4ecdc4; }
.module-card.interest { border-top-color: #f7b731; }
.module-card.policy { border-top-color: #5f27cd; }
.module-card.investment { border-top-color: #ee5a6f; }
.module-icon { 
  font-size: 4.5rem; 
  margin-bottom: 20px; 
  display: block;
  filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}
.module-card h2 { 
  color: #1a1a1a; 
  font-size: 2rem; 
  margin-bottom: 15px;
  font-weight: 800;
}
.module-card p { 
  color: #555; 
  font-size: 1.05rem; 
  line-height: 1.7; 
  margin-bottom: 20px; 
}
.module-features { 
  list-style: none; 
  padding: 0; 
  margin: 25px 0; 
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
}
.module-features li { 
  padding: 10px 0; 
  color: #444; 
  font-size: 0.98rem;
  display: flex;
  align-items: flex-start;
  line-height: 1.6;
}
.module-features li:before { 
  content: "✓"; 
  color: #4caf50; 
  font-weight: bold; 
  margin-right: 12px;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.tech-badge { 
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
  color: white; 
  padding: 10px 20px; 
  border-radius: 25px; 
  font-size: 0.88rem; 
  display: inline-block; 
  margin-top: 15px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}
.benefit-box { 
  background: linear-gradient(135deg, #f0f8f0 0%, #e8f5e9 100%); 
  border-left: 5px solid #4caf50; 
  padding: 18px; 
  margin-top: 20px; 
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(76, 175, 80, 0.1);
}
.benefit-box p { 
  margin: 0; 
  color: #2e7d32; 
  font-weight: 600;
  font-size: 1.02rem;
}
.workflow-section { 
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
  padding: 70px 30px; 
  margin: 70px 0;
  position: relative;
}
.workflow-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
  background-size: 200% 100%;
  animation: gradientMove 3s ease infinite;
}
@keyframes gradientMove {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
.workflow-steps { 
  max-width: 1000px; 
  margin: 50px auto 0; 
}
.workflow-step { 
  display: flex; 
  gap: 25px; 
  margin-bottom: 35px; 
  align-items: flex-start; 
}
.step-number { 
  background: linear-gradient(135deg, #1f77b4 0%, #2e7d32 100%); 
  color: white; 
  width: 70px; 
  height: 70px; 
  border-radius: 50%; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  font-size: 1.8rem; 
  font-weight: 900; 
  flex-shrink: 0;
  box-shadow: 0 8px 20px rgba(31, 119, 180, 0.3);
  position: relative;
}
.step-number::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid rgba(31, 119, 180, 0.3);
  animation: pulse 2s ease-out infinite;
}
@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(1.3); opacity: 0; }
}
.step-content { 
  flex: 1; 
  background: white; 
  padding: 25px 30px; 
  border-radius: 15px; 
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
  border-left: 4px solid #1f77b4;
  transition: all 0.3s ease;
}
.step-content:hover {
  transform: translateX(5px);
  box-shadow: 0 12px 35px rgba(0,0,0,0.12);
}
.step-content h3 { 
  color: #1a1a1a; 
  margin-bottom: 12px; 
  font-size: 1.5rem;
  font-weight: 700;
}
.step-content p { 
  color: #666; 
  margin: 0;
  line-height: 1.6;
  font-size: 1.05rem;
}
.stats-section { 
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
  padding: 60px 30px; 
  text-align: center;
  position: relative;
  overflow: hidden;
}
.stats-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: moveGrid 20s linear infinite;
}
@keyframes moveGrid {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}
.stats-section h2 {
  color: white;
  font-size: 2.5rem;
  margin-bottom: 15px;
  font-weight: 900;
  position: relative;
  z-index: 1;
}
.stats-grid { 
  display: grid; 
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
  gap: 30px; 
  max-width: 1200px; 
  margin: 40px auto 0;
  position: relative;
  z-index: 1;
}
.stat-item { 
  background: white; 
  padding: 35px 25px; 
  border-radius: 20px; 
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.stat-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}
.stat-item:hover {
  transform: translateY(-10px) scale(1.05);
  box-shadow: 0 15px 50px rgba(0,0,0,0.2);
}
.stat-number { 
  font-size: 3rem; 
  font-weight: 900; 
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px; 
}
.stat-label { 
  color: #555; 
  font-size: 1.15rem;
  font-weight: 600;
}
.target-section { 
  display: grid; 
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); 
  gap: 40px; 
  margin: 70px 0; 
}
.target-card { 
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
  color: white; 
  padding: 50px 40px; 
  border-radius: 25px; 
  box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}
.target-card::before {
  content: '';
  position: absolute;
  top: -100px;
  right: -100px;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  border-radius: 50%;
}
.target-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
}
.target-card h2 { 
  font-size: 2.3rem; 
  margin-bottom: 30px;
  font-weight: 900;
  position: relative;
  z-index: 1;
}
.target-card ul { 
  list-style: none; 
  padding: 0;
  position: relative;
  z-index: 1;
}
.target-card li { 
  padding: 15px 0; 
  font-size: 1.15rem; 
  border-bottom: 1px solid rgba(255,255,255,0.2);
  display: flex;
  align-items: flex-start;
  line-height: 1.6;
}
.target-card li:before { 
  content: "✓"; 
  font-weight: bold; 
  margin-right: 15px;
  font-size: 1.3rem;
  flex-shrink: 0;
}
.target-card li:last-child {
  border-bottom: none;
}
.why-card { 
  background: linear-gradient(135deg, #1f77b4 0%, #2e7d32 100%); 
}
.footer { 
  background: #2c3e50; 
  color: white; 
  text-align: center; 
  padding: 50px 30px; 
  margin-top: 0;
  position: relative;
}
.footer h3 {
  font-size: 2rem;
  margin-bottom: 20px;
  font-weight: 800;
}
.footer p {
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.8;
}
.cta-section { 
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
  color: white; 
  padding: 80px 40px; 
  text-align: center; 
  border-radius: 30px; 
  margin: 70px 0;
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;
}
.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(255,255,255,0.1) 0%, transparent 50%);
}
.cta-section h2 { 
  font-size: 3rem; 
  margin-bottom: 25px;
  font-weight: 900;
  position: relative;
  z-index: 1;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}
.cta-section p { 
  font-size: 1.35rem; 
  margin-bottom: 40px; 
  opacity: 0.95;
  position: relative;
  z-index: 1;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}
.cta-button { 
  display: inline-block; 
  background: white; 
  color: #667eea; 
  padding: 18px 50px; 
  border-radius: 30px; 
  font-weight: 800; 
  text-decoration: none; 
  transition: all 0.3s ease; 
  font-size: 1.2rem;
  box-shadow: 0 8px 25px rgba(0,0,0,0.2);
  position: relative;
  z-index: 1;
}
.cta-button:hover { 
  transform: translateY(-3px) scale(1.05); 
  box-shadow: 0 12px 35px rgba(0,0,0,0.3);
  background: #f8f9fa;
}
@media (max-width: 768px) {
  .hero-section h1 { font-size: 2.5rem; }
  .modules-grid { grid-template-columns: 1fr; }
  .target-section { grid-template-columns: 1fr; }
  .workflow-step { flex-direction: column; align-items: center; text-align: center; }
}
`;

const modules = [
  {
    title: 'Financial Advisor',
    icon: '💡',
    modifier: 'advisor',
    description: 'Comprehensive financial planning and analysis tool. Upload your insurance policy PDFs for automatic extraction and analysis of coverage, premiums, and riders.',
    features: ['PDF policy upload & parsing', 'Coverage adequacy check', 'Premium affordability analysis', 'Financial health scoring', 'Detailed action plans'],
    // tech: 'NLP (LLM/LangChain + pdfplumber) for document extraction and multi-factor analysis',
    benefit: 'Get unbiased analysis without depending on agents who often mis-sell policies'
  },
  {
    title: 'Inflation Forecast',
    icon: '📈',
    modifier: 'inflation',
    description: 'Track and predict inflation trends with advanced AI models. Get 12-month predictions with historical trend analysis and confidence intervals.',
    features: ['12-month inflation predictions', 'Historical trend analysis', 'Interactive visualizations', 'Confidence intervals'],
    // tech: 'Time-series forecasting using ARIMA, LSTM, and Facebook Prophet',
    benefit: 'Understand how inflation will impact your purchasing power and investment returns'
  },
  {
    title: 'GDP Growth Forecast',
    icon: '📊',
    modifier: 'gdp',
    description: 'Analyze economic growth patterns and future projections with quarterly GDP predictions and growth rate analysis.',
    features: ['Quarterly GDP predictions', 'Growth rate analysis', 'Economic trend insights', 'Data-driven forecasts'],
    // tech: 'Economic modeling with ARIMA and ensemble methods',
    benefit: 'Make informed decisions based on economic growth trends and forecasts'
  },
  {
    title: 'Interest Rates Forecast',
    icon: '💰',
    modifier: 'interest',
    description: 'Predict lending and deposit rate movements including repo rates, bond yields, and loan rates for better financial planning.',
    features: ['Multiple rate predictions', 'Repo, bond & loan rates', 'Rate change analysis', 'Financial planning support'],
    // tech: 'Multi-rate forecasting with macroeconomic indicators integration',
    benefit: 'Plan your borrowing and savings strategies based on predicted rate movements'
  },
  {
    title: 'Policy Recommendations',
    icon: '🔍',
    modifier: 'policy',
    description: 'Get personalized insurance policy suggestions with risk assessment analysis and coverage optimization powered by AI.',
    features: ['Risk assessment analysis', 'Personalized recommendations', 'Coverage optimization', 'AI-powered insights'],
    // tech: 'NLP and risk profiling algorithms with collaborative filtering',
    benefit: 'Find the right insurance coverage tailored to your life stage and financial situation'
  },
  {
    title: 'Investment Recommendations',
    icon: '💹',
    modifier: 'investment',
    description: 'Get personalized SIP, fund, and investment insights powered by AI with goal-based planning and inflation-aware recommendations.',
    features: ['Goal-based SIP planning', 'Top-performing fund analysis', 'Personalized insights', 'Inflation aware recommendations'],
    // tech: 'Portfolio optimization using Modern Portfolio Theory and clustering',
    benefit: 'Build a diversified portfolio aligned with your goals and risk tolerance'
  },
];

const AboutPage = () => {
  return (
    <div className="bg-slate-50 min-h-screen">
      <style>{styles}</style>
      <Navbar />
      
      <div className="hero-section">
        <h1>🏦 About Our Financial Wellness Platform</h1>
        <p>Your Complete Financial Analysis & Planning Ecosystem</p>
        <p style={{ fontSize: '1.1rem', opacity: 0.9 }}>
          Empowering individuals and families with AI-driven insights, personalized recommendations, and data-backed forecasts
        </p>
      </div>

      <div className="stats-section">
        <h2>Platform Highlights</h2>
        <div className="stats-grid">
          <div className="stat-item">
            <div className="stat-number">6</div>
            <div className="stat-label">Powerful Modules</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">12</div>
            <div className="stat-label">Month Forecasts</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">AI</div>
            <div className="stat-label">Powered Insights</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">24/7</div>
            <div className="stat-label">Access</div>
          </div>
        </div>
      </div>

      <div className="about-container">
        <h2 className="section-title">📌 Our Modules</h2>
        <p className="section-subtitle">
          Six intelligent tools working together for your complete financial wellness
        </p>
        
        <div className="modules-grid">
          {modules.map((mod, index) => (
            <div key={index} className={`module-card ${mod.modifier}`}>
              <span className="module-icon">{mod.icon}</span>
              <h2>{mod.title}</h2>
              <p>{mod.description}</p>
              <ul className="module-features">
                {mod.features.map((feature, idx) => (
                  <li key={idx}>{feature}</li>
                ))}
              </ul>
              <div className="tech-badge">
                🔧 {mod.tech}
              </div>
              <div className="benefit-box">
                <p>✨ {mod.benefit}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="workflow-section">
        <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 30px' }}>
          <h2 className="section-title">🔄 How It Works</h2>
          <p className="section-subtitle">
            Simple, seamless, and secure process in 6 steps
          </p>
          <div className="workflow-steps">
            <div className="workflow-step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>🔐 Create Your Account</h3>
                <p>Sign up with secure authentication and create your personalized profile</p>
              </div>
            </div>
            <div className="workflow-step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>📄 Upload Documents</h3>
                <p>Upload insurance policy PDFs and financial documents for analysis</p>
              </div>
            </div>
            <div className="workflow-step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>💼 Enter Financial Details</h3>
                <p>Input your personal and financial information (income, expenses, dependents, goals)</p>
              </div>
            </div>
            <div className="workflow-step">
              <div className="step-number">4</div>
              <div className="step-content">
                <h3>🤖 AI Analysis</h3>
                <p>Our AI extracts data, forecasts trends, checks affordability, and generates insights</p>
              </div>
            </div>
            <div className="workflow-step">
              <div className="step-number">5</div>
              <div className="step-content">
                <h3>📊 View Dashboard</h3>
                <p>Access interactive dashboard with graphs, policy insights, and personalized recommendations</p>
              </div>
            </div>
            <div className="workflow-step">
              <div className="step-number">6</div>
              <div className="step-content">
                <h3>✅ Download Reports</h3>
                <p>Get comprehensive reports with charts, insights, and actionable advice</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="about-container">
        <div className="target-section">
          <div className="target-card">
            <h2>🎯 Who We Serve</h2>
            <ul>
              <li>Middle-class individuals/families concerned about premiums & affordability</li>
              <li>Young professionals wanting investment + insurance advice</li>
              <li>Financially aware users who want independent, data-driven advice</li>
              <li>Anyone seeking unbiased financial recommendations</li>
            </ul>
          </div>

          <div className="target-card why-card">
            <h2>🚀 Why Choose Us</h2>
            <ul>
              <li>End-to-end fintech ecosystem, not just a single module</li>
              <li>Advanced ML models, NLP, and forecasting techniques</li>
              <li>Solves genuine problems in financial literacy</li>
              <li>User-centric with clear visuals (graphs, dashboards)</li>
              <li>Transparent, unbiased recommendations</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="about-container">
        <div className="cta-section">
          <h2>Ready to Transform Your Financial Future?</h2>
          <p>Join thousands of users making smarter financial decisions with AI-powered insights</p>
          <Link to="/dashboard" className="cta-button">
            Go to Dashboard →
          </Link>
        </div>
      </div>

      <div className="footer">
        <h3>🌟 Make Smarter Financial Decisions Today</h3>
        <p style={{ marginTop: 15, opacity: 0.8 }}>
          All forecasts and recommendations are based on advanced AI models and historical data analysis.
          <br />
          For personalized financial advice, please consult with a certified financial planner.
        </p>
        <p style={{ marginTop: 20, fontSize: '0.9rem' }}>
          © 2025 Financial Wellness Dashboard. All rights reserved.
        </p>
      </div>
    </div>
  );
};

export default AboutPage;