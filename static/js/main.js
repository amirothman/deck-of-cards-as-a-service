const clearContent = () => {
    const content = document.querySelector("#content");
    content.innerHTML = "";
}

const getDivWithTable = (tableData) => {
    const placeholder = document.createElement("div");
    const h5 = document.createElement("h5")
    h5.innerHTML = "Table"
    placeholder.appendChild(h5)
    const h5a = document.createElement("h5")
    h5a.innerHTML = "Table Key"
    placeholder.appendChild(h5a)
    const h5b = document.createElement("h5")
    h5b.innerHTML = tableData.name
    placeholder.appendChild(h5b)
    tableData.cards.forEach(card => {
        const span = document.createElement("span")
        if (card.covered) {
            span.innerHTML = "#"
        } else {
            span.innerHTML = `${card.suit} ${card.number}`
        }
        placeholder.appendChild(span)
    });
    return placeholder
}

const getDivWithPlayer = (playerData) => {
    const placeholder = document.createElement("div");
    const h5 = document.createElement("h5")
    h5.innerHTML = "Yours"

    placeholder.appendChild(h5)

    playerData.cards.forEach(card => {
        const span = document.createElement("span")
        span.innerHTML = `${card.suit} ${card.number}`
        placeholder.appendChild(span)
    });
    return placeholder
}

const handlePlayerData = playerData => {
    // console.log(playerData)
    document.cookie = `signature=${playerData.signature}`
    document.cookie = `name=${playerData.name}`
    // TODO: Somewhere here we need to subscribe to 
    // the current player's channel
    const content = document.querySelector("#content")
    const divPlayer = getDivWithPlayer(playerData);
    content.appendChild(divPlayer)

}

const handleOtherPlayer = (data) => {
    console.log(data)
}
// TODO: Currently this handler is kinda specific
// to starting the game, but not for
// updates during the game because of `Join the table` [1]
const handleCreateTable = tableData => {

    const tableName = tableData.name;
    document.cookie = `tableName=${tableData.table_name}`
    // TODO: Somewhere here we need to subscribe to 
    // the table chhanel
    const nameFieldValue = document.querySelector("#nameField").value

    // TODO: Somewhere here we need to check for 
    // other players on this table
    tableData.players.forEach(handleOtherPlayer)

    clearContent()
    const divTable = getDivWithTable(tableData)
    const content = document.querySelector("#content");
    content.appendChild(divTable)

    const requestBody = {
        "name": nameFieldValue
    }

    // Join the table [1]
    const endpoint = `/api/table/${tableName}/players`
    fetch(endpoint, {
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
        },
        "body": JSON.stringify(requestBody)
    }).then((response) => response.json()
        .then(handlePlayerData)
        .catch((error) => {
            console.error("Error:", error);
        }))



}

const executeJoinCreateTable = () => {

    const tableKey = document.querySelector("#tableKeyfield").value

    if (!tableKey) {
        fetch("/api/table", {
            "method": "POST"
        }).then(response => response.json()
        ).then(handleCreateTable).catch((error) => {
            console.error("Error:", error);
        })
    } else {
        fetch(`/api/table/${tableKey}`).then(
            response => response.json()
        ).then(
            handleCreateTable
        ).catch(() => {

            fetch("/api/table", {
                "method": "POST"
            }).then(response => response.json()
            ).then(handleCreateTable).catch((error) => {
                console.error("Error:", error);
            })

        })
    }

}

const joinCreateTable = document.querySelector("#joinCreateTable");

joinCreateTable.addEventListener("click", executeJoinCreateTable);

