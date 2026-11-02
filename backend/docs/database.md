# Database

```mermaid
erDiagram
    GAME {
        uuid id PK
        string name
        string description
        int min_players
        int max_players
    }

    PLAYER {
        uuid id PK
        string name
        EmailStr email
        str hashed_password
    }

    GAME_SESSION {
        uuid id PK
        uuid game_id FK
        uuid created_by FK
        datetime played_at
        text notes
    }

    GAME_RESULT {
        uuid id PK
        uuid session_id FK
        uuid player_id FK
        int position
        int score
        json additional_game_stats
    }

    GAME ||--o{ GAME_SESSION : "played in"
    GAME_SESSION ||--o{ GAME_RESULT : "has"
    PLAYER ||--o{ GAME_RESULT : "participates"
    PLAYER ||--o{ GAME_SESSION : "creates"
```

For now SQLite is the only supported database and the tables are created with `SQLModel.metadata.create_all` (no migrations yet).

A game must have `min_players` and `max_players` greater than 0, and `min_players` must not exceed `max_players` (the API answers `422` otherwise).
