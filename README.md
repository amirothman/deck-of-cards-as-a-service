# Deck of Cards As A Service

Create a general deck of cards for any card playing purpose.

## Todos

    [ ] Signature to be included as a URL parameter
    [x] Model - code business logic
    [x] API endpoints
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
        [x] Covering/uncovering cards
            [x] Can cover own cards
                [x] Implemented
                [x] Tested
            [x] Can uncover own cards
                [x] Implemented
                [x] Tested
            [x] Can cover cards on the table
                [x] Implemented
                [x] Tested
            [x] Can uncover cards on the table
                [x] Implemented
                [x] Tested
        [x] Reading cards
            [x] Hide cards that are covered when reading table
                [x] Implemented
                [x] Tested
            [x] Hide cards that are covered when reading player
            [x] Can read own cards
                [x] Implemented
                [x] Tested
            [x] Can read uncovered cards on the table
                [x] Implemented
                [x] Tested
            [x] Can read uncovered cards from other players
                [x] Implemented
                [x] Tested
        [x] Shuffle own cards
        [x] Shuffle cards on the table
    [ ] Web front end
        [ ] Necessary Server-Sent Events channel to allow multiplayer
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

        Endpoint                    Methods       Rule
        --------------------------  ------------  -----------------------------------------------------------------------------
        api.player                  GET           /api/table/<table_name>/players/<player_name>
        api.player                  POST          /api/table/<table_name>/players
        api.player_card             GET           /api/table/<table_name>/player/<card_owner_name>/card/<int:index>/<signature>
        api.player_card_visibility  PATCH         /api/table/<table_name>/player/<card_owner_name>/card
        api.players_cards           DELETE, POST  /api/table/<table_name>/players/<current_name>/cards/<other_name>
        api.shuffle_player_cards    PATCH         /api/table/<table_name>/player/<card_owner_name>/cards
        api.shuffle_table_cards     PATCH         /api/table/<table_name>/cards
        api.table                   POST          /api/table
        api.table                   GET           /api/table/<table_name>
        api.table_card              GET           /api/table/<table_name>/card/<int:index>
        api.table_card_visibility   PATCH         /api/table/<table_name>/card
        api.table_cards             DELETE, POST  /api/table/<table_name>/players/<current_name>/table
        static                      GET           /static/<path:filename>

## Notes, Thoughts, etc.

### 2020-03-25

When a player is created, the server returns a 'signature'.
This signature should be included in the body of the requests as
a form of identification.

### 2020-03-26

- Maybe the `signature` should be included as a URL params, instead of in the body/url to unify the pattern

