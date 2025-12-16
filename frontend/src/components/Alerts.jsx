import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts';
import { AlertOctagon, TrendingUp } from 'lucide-react';

const Alerts = () => {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAlerts = async () => {
            try {
                const data = await api.getAlerts(20);
                setAlerts(data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchAlerts();
    }, []);

    if (loading) return <div className="text-center p-8 animate-pulse">Loading Alerts...</div>;

    // Process data for charts
    const severityData = [
        { name: 'Critical', value: alerts.filter(a => a.risk_score > 0.8).length },
        { name: 'High', value: alerts.filter(a => a.risk_score > 0.5 && a.risk_score <= 0.8).length },
        { name: 'Medium', value: alerts.filter(a => a.risk_score <= 0.5).length },
    ].filter(d => d.value > 0);

    const COLORS = ['#EF4444', '#F59E0B', '#3B82F6'];

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold flex items-center gap-2">
                <AlertOctagon className="text-danger" />
                Fraud Alerts Monitor
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Recent Alerts List */}
                <div className="card h-96 overflow-hidden flex flex-col">
                    <h3 className="text-lg font-semibold mb-4">Recent Flags</h3>
                    <div className="overflow-y-auto space-y-3 pr-2 scrollbar-thin">
                        {alerts.length === 0 ? (
                            <p className="text-gray-400 text-center py-10">No alerts found</p>
                        ) : (
                            alerts.map((alert) => (
                                <div key={alert.transaction_id} className="p-3 bg-slate-800/50 rounded-lg border border-slate-700 hover:border-danger/50 transition-colors">
                                    <div className="flex justify-between items-start mb-1">
                                        <span className="font-mono text-xs text-gray-400">{alert.transaction_id}</span>
                                        <span className="text-xs text-danger font-bold">{(alert.risk_score * 100).toFixed(0)}% Risk</span>
                                    </div>
                                    <p className="text-sm font-medium mb-1 truncate">{alert.reason.split('|')[0]}</p>
                                    <p className="text-xs text-gray-500">{new Date(alert.timestamp).toLocaleString()}</p>
                                </div>
                            ))
                        )}
                    </div>
                </div>

                {/* Charts */}
                <div className="space-y-6">
                    <div className="card h-44">
                        <h3 className="text-sm text-gray-400 mb-2">Severity Distribution</h3>
                        <div className="h-full -mt-4">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={severityData}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={40}
                                        outerRadius={60}
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {severityData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    <div className="card h-44">
                        <h3 className="text-sm text-gray-400 mb-2 flex items-center gap-2">
                            <TrendingUp className="w-4 h-4" />
                            Risk Trend (Last 20)
                        </h3>
                        <div className="h-full -mt-2">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={[...alerts].reverse()}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                    <XAxis dataKey="timestamp" hide />
                                    <YAxis domain={[0, 1]} hide />
                                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
                                    <Line type="monotone" dataKey="risk_score" stroke="#ef4444" strokeWidth={2} dot={false} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Alerts;
