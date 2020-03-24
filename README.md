# Deck of Cards As A Service

Create a general deck of cards for any card playing purpose

## Todos

    [x] Model - code business logic
    [ ] API endpoints
        [x] Create table
            [x] Implemented
            [x] Tested
        [x] Join table
            [x] Implemented
            [x] Tested
        [ ] Give/take cards to/from players
            [x] Implemented
            [ ] Tested
        [ ] Give/take cards to/from table
            [x] Implemented
            [ ] Tested
    [ ] Web front end
    [ ] Documentation

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
