import React from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const DraftBoard = ({ keepers, allPlayers, onBack, onRemove, onDragEnd }) => {

    const getPlayerDetails = (playerId) => {
        if (!allPlayers || !allPlayers.teams) return null;
        for (const team of allPlayers.teams) {
            const player = team.players.find(p => p.id === playerId);
            if (player) return player;
        }
        return null;
    };

    return (
        <div className="draft-board">
            <button onClick={onBack} className="back-btn">← Back to Keeper Selection</button>
            <h1>Final Draft Board</h1>
            <DragDropContext onDragEnd={onDragEnd}>
                <Droppable droppableId="keepers">
                    {(provided) => (
                        <div {...provided.droppableProps} ref={provided.innerRef} className="keepers-list">
                            <h2>Selected Keepers ({keepers.length})</h2>
                            <ul>
                                {keepers.map((keeperId, index) => {
                                    const player = getPlayerDetails(keeperId);
                                    return player ? (
                                        <Draggable key={keeperId} draggableId={String(keeperId)} index={index}>
                                            {(provided, snapshot) => (
                                                <li 
                                                    ref={provided.innerRef}
                                                    {...provided.draggableProps} 
                                                    {...provided.dragHandleProps}
                                                    data-is-dragging={snapshot.isDragging}
                                                >
                                                    <span>{index + 1}. {player.name} ({player.position})</span>
                                                    <button onClick={() => onRemove(keeperId)} className="remove-btn">Remove</button>
                                                </li>
                                            )}
                                        </Draggable>
                                    ) : null;
                                })}
                                {provided.placeholder}
                            </ul>
                        </div>
                    )}
                </Droppable>
            </DragDropContext>
        </div>
    );
};

export default DraftBoard;
