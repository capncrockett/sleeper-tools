import React, { useState, useEffect, useMemo } from 'react';
import KeeperTool from './KeeperTool';
import './App.css';

function App() {
    const [view, setView] = useState('adp'); // 'adp' or 'keeper'
    const [adpData, setAdpData] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortConfig, setSortConfig] = useState({ key: 'average_pick', direction: 'ascending' });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Only fetch ADP data if the view is 'adp'
        if (view === 'adp') {
            setLoading(true);
            fetch('http://localhost:5001/api/adp')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    setAdpData(data);
                    setLoading(false);
                })
                .catch(error => {
                    console.error('Error fetching ADP data:', error);
                    setError(error.message);
                    setLoading(false);
                });
        }
    }, [view]);

    const sortedData = useMemo(() => {
        if (!adpData) return [];
        let sortableData = [...adpData];
        if (sortConfig.key) {
            sortableData.sort((a, b) => {
                const aValue = a[sortConfig.key] ?? Infinity;
                const bValue = b[sortConfig.key] ?? Infinity;

                if (aValue < bValue) {
                    return sortConfig.direction === 'ascending' ? -1 : 1;
                }
                if (aValue > bValue) {
                    return sortConfig.direction === 'ascending' ? 1 : -1;
                }
                return 0;
            });
        }
        return sortableData;
    }, [adpData, sortConfig]);

    const filteredData = useMemo(() => {
        return sortedData.filter(player =>
            player.player_name.toLowerCase().includes(searchTerm.toLowerCase())
        );
    }, [sortedData, searchTerm]);

    const requestSort = (key) => {
        let direction = 'ascending';
        if (sortConfig.key === key && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    const getSortIndicator = (key) => {
        if (sortConfig.key !== key) return ' ↕';
        return sortConfig.direction === 'ascending' ? ' ▲' : ' ▼';
    };

    return (
        <div className="App">
            <div className="view-toggle">
                <button onClick={() => setView('adp')} className={view === 'adp' ? 'active' : ''}>
                    ADP View
                </button>
                <button onClick={() => setView('keeper')} className={view === 'keeper' ? 'active' : ''}>
                    Keeper Tool
                </button>
            </div>
            {view === 'adp' ? (
                <div className="container">
                    <h1>Keeper League Custom ADP</h1>
                    <input
                        type="text"
                        placeholder="Search for a player..."
                        className="search-bar"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        disabled={loading || error}
                    />
                    {loading && <p>Loading ADP data...</p>}
                    {error && <p>Error: {error}</p>}
                    {!loading && !error && (
                        <table className="adp-table" data-testid="adp-table">
                            <thead>
                                <tr>
                                    <th onClick={() => requestSort('player_name')}>Player{getSortIndicator('player_name')}</th>
                                    <th onClick={() => requestSort('average_pick')}>ADP{getSortIndicator('average_pick')}</th>
                                    <th onClick={() => requestSort('std_dev')}>Std Dev{getSortIndicator('std_dev')}</th>
                                    <th onClick={() => requestSort('times_drafted')}># Drafts{getSortIndicator('times_drafted')}</th>
                                    <th onClick={() => requestSort('earliest_pick')}>Min Pick{getSortIndicator('earliest_pick')}</th>
                                    <th onClick={() => requestSort('latest_pick')}>Max Pick{getSortIndicator('latest_pick')}</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredData.length > 0 ? (
                                    filteredData.map((player, index) => (
                                        <tr key={player.player_name || index}>
                                            <td>{player.player_name}</td>
                                            <td>{player.average_pick}</td>
                                            <td>{player.std_dev}</td>
                                            <td>{player.times_drafted}</td>
                                            <td>{player.earliest_pick}</td>
                                            <td>{player.latest_pick}</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="6">No players found.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    )}
                </div>
            ) : (
                <KeeperTool />
            )}
        </div>
    );
}

export default App;
