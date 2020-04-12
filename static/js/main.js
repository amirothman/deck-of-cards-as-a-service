const clearContent = () => {
    const content = document.querySelector("#content");
    content.innerHTML = "";
}

const getDivWithTable = (tableData) => {
    const placeholder = document.createElement("div");
    placeholder.setAttribute("class", "placeHolder");
    placeholder.setAttribute("id", "tableCards");

    const h5a = document.createElement("h5")
    h5a.innerHTML = "Table Key"
    placeholder.appendChild(h5a)

    const h5b = document.createElement("h5")
    h5b.innerHTML = tableData.name
    h5b.setAttribute("id", "tableKey")
    placeholder.appendChild(h5b)

    const h5 = document.createElement("h5")
    h5.innerHTML = "Table Cards"
    placeholder.appendChild(h5)

    tableData.cards.forEach(card => {
        const span = document.createElement("span")
        span.setAttribute("class", "card")
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
    placeholder.setAttribute("class", "placeHolder")
    const h5 = document.createElement("h5")
    h5.innerHTML = "Your cards"
    placeholder.appendChild(h5)

    playerData.cards.forEach(card => {
        const span = document.createElement("span")
        span.setAttribute("class", "card")
        span.innerHTML = `${card.suit} ${card.number}`
        placeholder.appendChild(span)
    })
    return placeholder
}

const handlePlayerData = playerData => {
    document.cookie = `signature=${playerData.signature}`
    document.cookie = `name=${playerData.name}`
    const content = document.querySelector("#content")
    const divPlayer = getDivWithPlayer(playerData);
    content.appendChild(divPlayer)

}

const handleOtherPlayer = (playerData) => {
    const placeholder = document.createElement("div");
    placeholder.setAttribute("class", "placeHolder")
    const h5 = document.createElement("h5")
    h5.setAttribute("class", "cardLabel")
    h5.innerHTML = `${playerData.name}'s cards`
    placeholder.appendChild(h5)

    playerData.cards.forEach(card => {
        const span = document.createElement("span")
        span.setAttribute("class", "card")
        span.innerHTML = `${card.suit} ${card.number}`
        placeholder.appendChild(span)
    })
    const content = document.querySelector("#content")
    content.appendChild(placeholder)
}
// TODO: Currently this handler is kinda specific
// to starting the game, but not for
// updates during the game because of `Join the table` [1]
const handleCreateTable = tableData => {

    const tableName = tableData.name;
    document.cookie = `tableName=${tableData.table_name}`
    // TODO: Somewhere here we need to subscribe to 
    // the table chhanel
    const username = document.querySelector("#nameField").value

    // TODO: Somewhere here we need to check for 
    // other players on this table


    clearContent()
    const divTable = getDivWithTable(tableData)
    const content = document.querySelector("#content");
    content.appendChild(divTable)

    const requestBody = {
        "name": username
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
        .then((data) => {
            handlePlayerData(data);
            tableData.players.forEach((elem) => {
                if (elem.name != data.name) {
                    handleOtherPlayer(elem)
                }
            })
        })
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


const playWithSSE = () => {
    const evtSource = new EventSource("/sse/table/user/");
    evtSource.addEventListener("table", (event) => {
        console.log(event)
    });
}

joinCreateTable.addEventListener("click", playWithSSE)