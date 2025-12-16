import React, { useState } from 'react';
import { api } from '../api/client';
import { Send, Loader2, RefreshCw } from 'lucide-react';

const TransactionForm = ({ onPrediction }) => {
    const [formData, setFormData] = useState({
        transaction_id: `TXN-${Math.floor(Math.random() * 10000)}`,
        customer_id: 'CUST-001',
        account_age_days: 365,
        transaction_amount: 50.0,
        channel: 'online',
        kyc_verified_flag: 1,
        hour: new Date().getHours(),
        weekday: new Date().getDay(),
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? (checked ? 1 : 0) : value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const result = await api.predict({
                ...formData,
                transaction_id: `TXN-${Math.floor(Math.random() * 100000)}`, // Generate new ID
            });
            onPrediction(result);
        } catch (err) {
            setError("Prediction failed. Please try again.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card max-w-lg mx-auto">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Send className="w-5 h-5 text-primary" />
                Analyze Transaction
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                {/* Customer ID & Amount */}
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm text-gray-400 mb-1">Customer ID</label>
                        <input
                            type="text"
                            name="customer_id"
                            value={formData.customer_id}
                            onChange={handleChange}
                            className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-sm focus:border-primary outline-none"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm text-gray-400 mb-1">Amount ($)</label>
                        <input
                            type="number"
                            name="transaction_amount"
                            value={formData.transaction_amount}
                            onChange={handleChange}
                            className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-sm focus:border-primary outline-none"
                            required
                        />
                    </div>
                </div>

                {/* Account Age & Channel */}
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm text-gray-400 mb-1">Account Age (Days)</label>
                        <input
                            type="number"
                            name="account_age_days"
                            value={formData.account_age_days}
                            onChange={handleChange}
                            className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-sm focus:border-primary outline-none"
                        />
                    </div>
                    <div>
                        <label className="block text-sm text-gray-400 mb-1">Channel</label>
                        <select
                            name="channel"
                            value={formData.channel}
                            onChange={handleChange}
                            className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-sm focus:border-primary outline-none"
                        >
                            <option value="atm">ATM</option>
                            <option value="online">Online</option>
                            <option value="pos">POS</option>
                            <option value="mobile">Mobile</option>
                            <option value="web">Web</option>
                        </select>
                    </div>
                </div>

                {/* KYC Toggle */}
                <div className="flex items-center gap-2">
                    <input
                        type="checkbox"
                        name="kyc_verified_flag"
                        checked={formData.kyc_verified_flag === 1}
                        onChange={handleChange}
                        className="w-4 h-4 accent-primary"
                    />
                    <label className="text-sm">KYC Verified</label>
                </div>

                {error && <p className="text-danger text-sm">{error}</p>}

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full btn btn-primary flex items-center justify-center gap-2 mt-4"
                >
                    {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Analyze Risk"}
                </button>
            </form>
        </div>
    );
};

export default TransactionForm;
