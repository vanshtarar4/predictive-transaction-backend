import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Activity, CheckCircle, AlertTriangle } from 'lucide-react';

const Metrics = () => {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const data = await api.getMetrics();
                setMetrics(data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchMetrics();
    }, []);

    if (loading) return <div className="text-center p-8 animate-pulse">Loading Model Metrics...</div>;
    if (!metrics) return null;

    const chartData = [
        { name: 'Accuracy', value: metrics.accuracy },
        { name: 'Precision', value: metrics.precision },
        { name: 'Recall', value: metrics.recall },
        { name: 'F1 Score', value: metrics.f1_score },
        { name: 'AUC', value: metrics.auc },
    ];

    const MetricCard = ({ label, value, icon: Icon, color }) => (
        <div className="card flex items-center gap-4">
            <div className={`p-3 rounded-full bg-${color}-500/10 text-${color}-500`}>
                <Icon className="w-6 h-6" />
            </div>
            <div>
                <p className="text-sm text-gray-400">{label}</p>
                <p className="text-2xl font-bold">{(value * 100).toFixed(1)}%</p>
            </div>
        </div>
    );

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold flex items-center gap-2">
                <Activity className="text-primary" />
                Model Performance
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <MetricCard label="Accuracy" value={metrics.accuracy} icon={CheckCircle} color="blue" />
                <MetricCard label="Precision" value={metrics.precision} icon={Activity} color="green" />
                <MetricCard label="Recall" value={metrics.recall} icon={AlertTriangle} color="yellow" />
            </div>

            <div className="card h-64 w-full">
                <h3 className="text-sm text-gray-400 mb-4">Performance Overview</h3>
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} layout="vertical">
                        <XAxis type="number" domain={[0, 1]} hide />
                        <YAxis type="category" dataKey="name" width={80} tick={{ fill: '#94a3b8', fontSize: 12 }} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                        />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={index % 2 === 0 ? '#3b82f6' : '#10b981'} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default Metrics;
