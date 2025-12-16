import React from 'react';
import { ShieldCheck, ShieldAlert, Cpu, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

const Dashboard = ({ result }) => {
    if (!result) return null;

    const isFraud = result.prediction === 'Fraud';
    const riskPercent = Math.round(result.risk_score * 100);

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={`card border-l-4 ${isFraud ? 'border-l-danger' : 'border-l-secondary'} mt-6`}
        >
            <div className="flex justify-between items-start mb-6">
                <div>
                    <h3 className="text-gray-400 text-sm mb-1">Prediction Result</h3>
                    <div className="flex items-center gap-3">
                        {isFraud ? (
                            <ShieldAlert className="w-8 h-8 text-danger" />
                        ) : (
                            <ShieldCheck className="w-8 h-8 text-secondary" />
                        )}
                        <span className={`text-3xl font-bold ${isFraud ? 'text-danger' : 'text-secondary'}`}>
                            {result.prediction}
                        </span>
                    </div>
                </div>
                <div className="text-right">
                    <p className="text-gray-400 text-sm">Transaction ID</p>
                    <p className="font-mono text-sm">{result.transaction_id}</p>
                </div>
            </div>

            <div className="space-y-4">
                {/* Risk Score */}
                <div>
                    <div className="flex justify-between text-sm mb-2">
                        <span>Risk Score</span>
                        <span className="font-bold">{riskPercent}%</span>
                    </div>
                    <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${riskPercent}%` }}
                            transition={{ duration: 1, ease: "easeOut" }}
                            className={`h-full ${isFraud ? 'bg-danger' : 'bg-secondary'}`}
                        />
                    </div>
                </div>

                {/* Reason / Explanation */}
                <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700">
                    <h4 className="flex items-center gap-2 text-sm font-semibold mb-2">
                        <Cpu className="w-4 h-4 text-primary" />
                        Analysis Detail
                    </h4>
                    <p className="text-sm text-gray-300 leading-relaxed">
                        {result.reason || "No suspicious activity detected. Transaction appears normal."}
                    </p>
                </div>

                {isFraud && (
                    <div className="flex items-start gap-3 p-3 bg-yellow-500/10 text-yellow-500 rounded-lg text-sm">
                        <AlertTriangle className="w-5 h-5 shrink-0" />
                        <p>This transaction has been flagged for immediate review by the fraud team.</p>
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default Dashboard;
