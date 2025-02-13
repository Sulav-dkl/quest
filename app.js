document.addEventListener("DOMContentLoaded", () => {
    let playerLevel = 1;
    let playerEXP = 0;
    const quests = [];

    // Elements from HTML
    const levelElement = document.getElementById("level");
    const expElement = document.getElementById("exp");
    const questList = document.getElementById("quest-list");
    const questForm = document.getElementById("quest-form");
    const questNameInput = document.getElementById("quest-name");
    const expRewardInput = document.getElementById("exp-reward");
    const resetProgressButton = document.getElementById("reset-progress");

    // Fetch player data
    async function fetchPlayerData() {
        const response = await fetch('/get_player_data');
        const data = await response.json();
        playerLevel = data.level;
        playerEXP = data.exp;
        updatePlayerStats();
    }

    // Fetch quests
    async function fetchQuests() {
        const response = await fetch('/get_quests');
        const data = await response.json();
        quests.length = 0; // Clear current quests
        data.forEach(quest => quests.push(quest));
        displayQuests();
    }

    // Update player stats
    function updatePlayerStats() {
        levelElement.textContent = playerLevel;
        expElement.textContent = playerEXP;
    }

    // Display quests on the UI
    function displayQuests() {
        questList.innerHTML = '';
        quests.forEach((quest, index) => {
            const questItem = document.createElement('li');
            questItem.innerHTML = `
                <strong>${quest.name}</strong> | EXP: ${quest.exp_reward}
                <button onclick="completeQuest(${quest.id})">Complete</button>
                <button onclick="deleteQuest(${quest.id})">Delete</button>
            `;
            questList.appendChild(questItem);
        });
    }

    // Complete a quest
    window.completeQuest = async function (questId) {
        await fetch(`/complete_quest/${questId}`, { method: 'POST' });
        fetchQuests(); // Refresh quest list after completing a quest
        fetchPlayerData(); // Refresh player data after completing a quest
    };

    // Delete a quest
    window.deleteQuest = async function (questId) {
        await fetch(`/delete_quest/${questId}`, { method: 'POST' });
        fetchQuests(); // Refresh quest list after deleting a quest
    };

    // Add a new quest
    questForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const questName = questNameInput.value;
        const expReward = parseInt(expRewardInput.value);
        await fetch('/add_quest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: questName, exp_reward: expReward })
        });
        questNameInput.value = '';
        expRewardInput.value = '';
        fetchQuests();
    });

    // Reset player progress
    resetProgressButton.addEventListener("click", async function () {
        await fetch('/reset_player', { method: 'POST' });
        fetchPlayerData();
        fetchQuests();
    });

    // Initial fetch to load player data and quests
    fetchPlayerData();
    fetchQuests();
});
