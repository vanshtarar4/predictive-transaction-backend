import React, { useState } from 'react';
import TransactionForm from './components/TransactionForm';
import Dashboard from './components/Dashboard';
import Metrics from './components/Metrics';
import Alerts from './components/Alerts';
import { LayoutDashboard, Zap, Activity, AlertCircle } from 'lucide-react';
import clsx from 'clsx';

function App() {
  const [activeTab, setActiveTab] = useState('predict');
  const [predictionResult, setPredictionResult] = useState(null);

  const tabs = [
    { id: 'predict', label: 'Predict Risk', icon: Zap },
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard }, // For result viewing mostly
    { id: 'alerts', label: 'Live Alerts', icon: AlertCircle },
    { id: 'metrics', label: 'Model Performance', icon: Activity },
  ];

  const handlePrediction = (result) => {
    setPredictionResult(result);
    // Determine where to go? Maybe stay on predict or show dashboard below?
    // User requested "Prediction Result Dashboard... After submission, display results in Animated card view"
    // I will show it below the form or switch to a 'result' view? 
    // Usually best to show inline.
    // I'll keep it on the 'predict' tab but scroll to result, OR switch tabs if prefered.
    // Let's Keep it simple: show Dashboard component BELOW form when on 'predict' tab.
  };

  return (
    <div className="min-h-screen bg-background text-gray-100 pb-20">
      {/* Navbar */}
      <nav className="border-b border-gray-800 bg-surface/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary to-blue-400 rounded-lg flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
              F
            </div>
            <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
              FraudShield
            </span>
          </div>

          <div className="flex gap-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={clsx(
                    "px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all",
                    activeTab === tab.id
                      ? "bg-primary/10 text-primary"
                      : "text-gray-400 hover:text-white hover:bg-white/5"
                  )}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8">

        {activeTab === 'predict' && (
          <div className="space-y-8">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold mb-2">Transaction Analysis</h1>
              <p className="text-gray-400">Enter transaction details below for real-time fraud assessment.</p>
            </div>

            <TransactionForm onPrediction={handlePrediction} />

            {predictionResult && (
              <div id="result-section" className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                <Dashboard result={predictionResult} />
              </div>
            )}
          </div>
        )}

        {/* Dashboard Tab - could satisfy user request for separate "Dashboard" page */}
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold">Analytics Dashboard</h2>
            {/* Combine elements here if requested, for now reusing Alerts + Metrics briefly or just explanation */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="card bg-gradient-to-br from-slate-800 to-slate-900 border-none">
                <h3 className="text-lg font-bold mb-2">System Status</h3>
                <div className="flex items-center gap-2 text-green-400">
                  <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                  Operational
                </div>
                <p className="text-sm text-gray-400 mt-2">Real-time inference engine active.</p>
              </div>
              <div className="card bg-gradient-to-br from-primary/20 to-blue-900/20 border-none">
                <h3 className="text-lg font-bold mb-2">Total Scanned</h3>
                <p className="text-4xl font-bold">2,451</p>
                <p className="text-sm text-gray-400 mt-1">Transactions processed today</p>
              </div>
            </div>

            <Alerts />
          </div>
        )}

        {activeTab === 'alerts' && <Alerts />}

        {activeTab === 'metrics' && <Metrics />}

      </main>
    </div>
  );
}

export default App;
