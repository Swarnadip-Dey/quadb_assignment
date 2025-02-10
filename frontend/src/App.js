import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [activeTab, setActiveTab] = useState('addTransactions');
    const [transactions, setTransactions] = useState(['']);
    const [blockchain, setBlockchain] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Fetch blockchain data when the 'Visualize Blockchain' tab is active
    useEffect(() => {
        if (activeTab === 'visualizeBlockchain') {
            fetchBlockchain();
        }
    }, [activeTab]);

    // Fetch blockchain data from the server
    const fetchBlockchain = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get('http://127.0.0.1:5000/blockchain');
            setBlockchain(response.data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // Add a new transaction input field
    const addTransactionField = () => {
        setTransactions([...transactions, '']);
    };

    // Update transaction field value
    const handleTransactionChange = (index, event) => {
        const newTransactions = [...transactions];
        newTransactions[index] = event.target.value;
        setTransactions(newTransactions);
    };

    // Handle form submission to add transactions
    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await axios.post('http://127.0.0.1:5000/transactions', transactions); // Correct endpoint
            setTransactions(['']); // Clear the input fields
            alert("Transactions added successfully!");
            await fetchBlockchain(); // Refresh the blockchain data
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // Render the Add Transactions tab
    const renderAddTransactionsTab = () => (
        <form onSubmit={handleSubmit}>
            <h2>Add Transactions</h2>
            {transactions.map((transaction, index) => (
                <div key={index}>
                    <input
                        type="text"
                        value={transaction}
                        onChange={(event) => handleTransactionChange(index, event)}
                        placeholder={`Transaction ${index + 1}`}
                    />
                </div>
            ))}
            <button type="button" onClick={addTransactionField}>Add More</button>
            <button type="submit" disabled={loading}>
                {loading ? 'Adding...' : 'Add Transactions'}
            </button>
        </form>
    );

    // Render the Visualize Blockchain tab
    const renderVisualizeBlockchainTab = () => (
        <>
            <h2>Blockchain</h2>
            {loading ? (
                <p>Loading blockchain...</p>
            ) : (
                <div className="blockchain">
                    {blockchain.map((block) => (
                        <div key={block.index} className="block">
                            <h3>Block {block.index}</h3>
                            <p>Timestamp: {new Date(block.timestamp * 1000).toLocaleString()}</p>
                            <p>
                                Previous Hash: 
                                <span title={block.previous_hash}>
                                    {block.previous_hash.slice(0, 10)}...{block.previous_hash.slice(-10)}
                                </span>
                            </p>
                            <p>
                                Hash: 
                                <span title={block.hash}>
                                    {block.hash.slice(0, 10)}...{block.hash.slice(-10)}
                                </span>
                            </p>
                            <p>Nonce: {block.nonce}</p>
                            <h4>Transactions:</h4>
                            {Array.isArray(block.transactions) ? (
                                block.transactions.map((tx, index) => (
                                    <li key={index}>{tx}</li>
                                ))
                            ) : (
                                <p>No transactions found.</p>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </>
    );

    return (
        <div className="App">
            <h1>Blockchain Visualizer</h1>

            <div className="tabs">
                <button
                    className={activeTab === 'addTransactions' ? 'active' : ''}
                    onClick={() => setActiveTab('addTransactions')}
                >
                    Add Transactions
                </button>
                <button
                    className={activeTab === 'visualizeBlockchain' ? 'active' : ''}
                    onClick={() => setActiveTab('visualizeBlockchain')}
                >
                    Visualize Blockchain
                </button>
            </div>

            {error && <p className="error">Error: {error}</p>}

            {activeTab === 'addTransactions' && renderAddTransactionsTab()}
            {activeTab === 'visualizeBlockchain' && renderVisualizeBlockchainTab()}
        </div>
    );
}

export default App;
