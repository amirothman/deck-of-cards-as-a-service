# Deck of Cards As A Service

Create a general deck of cards for any card playing purpose.

## Todos

    [x] Model - code business logic
    [ ] API endpoints
        [x] Create table
            [x] Implemented
            [x] Tested
        [x] Join table (create a player)
            [x] Implemented
            [x] Tested
        [x] Give/take cards to/from players
            [x] Implemented
            [x] Tested
        [x] Give/take cards to/from table
            [x] Implemented
            [x] Tested
        [ ] Covering/uncovering cards
            [ ] Can cover own cards
            [ ] Can uncover own cards
            [ ] Can cover cards on the table
            [ ] Can uncover cards on the table
        [ ] Reading cards
            [ ] Can read own cards
            [ ] Can read uncovered cards on the table
            [ ] Can read uncovered cards from other players
        [ ] Shuffle own cards
        [ ] Shuffle cards on the table
    [ ] Web front end
    [ ] Documentation
        [ ] Creating a table
        [ ] Joining a table (creating a player)
        [ ] Take a card from the table
        [ ] Give a card to the table
        [ ] Give a card to a different player
        [ ] Cover a card on the table
        [ ] Uncover a card on the table
        [ ] Cover own card
        [ ] Uncover own card
        [ ] Read own card
        [ ] Read a card on the table
        [ ] Read a card from another player
        [ ] Shuffle cards on the table
        [ ] Shuffle own deck cards

## Endpoints

        Endpoint           Methods       Rule
        -----------------  ------------  -------------------------------------------------------------
        api.player         GET           /table/<table_name>/players/<player_name>
        api.player         POST          /table/<table_name>/players
        api.players_cards  DELETE, POST  /table/<table_name>/players/<current_name>/cards/<other_name>
        api.table          POST          /table
        api.table          GET           /table/<table_name>
        api.table_cards    DELETE, POST  /table/<table_name>/players/<current_name>/table
        static             GET           /static/<path:filename>


## Authorization

When a player is created, the server returns a 'signature'.
This signature should be included in the body of the requests as
a form of identification.


