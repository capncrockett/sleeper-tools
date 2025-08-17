import React, { useState, useEffect } from 'react';
import DraftBoard from './DraftBoard';

const KeeperTool = () => {
    const [keeperData, setKeeperData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedKeepers, setSelectedKeepers] = useState([]);
    const [view, setView] = useState('selection'); // 'selection' or 'board'

    useEffect(() => {
        const fetchKeeperData = async () => {
            try {
                const response = await fetch('http://localhost:5001/api/keeper-data');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setKeeperData(data);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchKeeperData();
    }, []);

    const handleKeeperSelect = (playerId) => {
        setSelectedKeepers(prev => {
            if (prev.includes(playerId)) {
                return prev.filter(id => id !== playerId);
            }
            return [...prev, playerId];
        });
    };

    const handleRemoveKeeper = (playerId) => {
        setSelectedKeepers(prev => prev.filter(id => id !== playerId));
    };

    const handleDragEnd = (result) => {
        if (!result.destination) return;

        const items = Array.from(selectedKeepers);
        const [reorderedItem] = items.splice(result.source.index, 1);
        items.splice(result.destination.index, 0, reorderedItem);

        setSelectedKeepers(items);
    };

    const generateDraftBoard = () => {
        setView('board');
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!keeperData) return <div>No data available.</div>;

    if (view === 'board') {
        return (
            <DraftBoard 
                keepers={selectedKeepers}
                allPlayers={keeperData}
                onBack={() => setView('selection')}
                onRemove={handleRemoveKeeper}
                onDragEnd={handleDragEnd}
            />
        );
    }

    return (
        <div className="keeper-tool">
            <h1>{keeperData.league_name} - Keeper List</h1>
            <button onClick={generateDraftBoard} className="generate-btn">
                Generate Draft Board ({selectedKeepers.length} selected)
            </button>
            <div className="teams-container">
                {keeperData.teams.map((team, index) => (
                    <div key={index} className="team-card">
                        <h2>{team.owner_name}</h2>
                        <ul>
                            {team.players.map((player) => (
                                <li key={player.id}>
                                    <input 
                                        type="checkbox" 
                                        id={`player-${player.id}`}
                                        checked={selectedKeepers.includes(player.id)}
                                        onChange={() => handleKeeperSelect(player.id)}
                                    />
                                    <label htmlFor={`player-${player.id}`}>
                                        {player.name} ({player.position}) - Drafted: {player.draft_round}.{player.draft_pick}
                                    </label>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default KeeperTool;
