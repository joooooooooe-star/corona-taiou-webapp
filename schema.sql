CREATE TABLE IF NOT EXISTS user (
    name_id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name_id INTEGER NOT NULL,
    temperature REAL NOT NULL, 
    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    fatigue BOOLEAN NOT NULL, 
    tpain BOOLEAN NOT NULL, 
    other BOOLEAN NOT NULL);

CREATE TABLE IF NOT EXISTS removelog (
    remove_id INTEGER PRIMARY KEY AUTOINCREMENT,
    old_id INTEGER NOT NULL,
    old_name_id INTEGER NOT NULL,
    old_temp REAL NOT NULL,
    old_date DATETIME NOT NULL,
    old_fatigue BOOLEAN NOT NULL,
    old_tpain BOOLEAN NOT NULL,
    old_other BOOLEAN NOT NULL,
    del_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comment TEXT DEFAULT "NONE");

CREATE TABLE IF NOT EXISTS changelog (
    change_id INTEGER PRIMARY KEY AUTOINCREMENT,
    old_name_id INTEGER NOT NULL,
    new_name_id INTEGER NOT NULL,
    old_temp REAL NOT NULL,
    old_date DATETIME NOT NULL,
    old_fatigue BOOLEAN NOT NULL,
    old_tpain BOOLEAN NOT NULL,
    old_other BOOLEAN NOT NULL,
    new_temp REAL NOT NULL,
    new_date DATETIME NOT NULL,
    new_fatigue BOOLEAN NOT NULL,
    new_tpain BOOLEAN NOT NULL,
    new_other BOOLEAN NOT NULL,
    change_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comment TEXT DEFAULT "NONE");
    
CREATE TRIGGER IF NOT EXISTS log_change
    AFTER UPDATE ON data
BEGIN
    INSERT INTO changelog (
    old_name_id,
    new_name_id,
    old_temp,
    new_temp,
    old_date,
    new_date,
    old_fatigue,
    new_fatigue,
    old_tpain,
    new_tpain,
    old_other,
    new_other,
    change_time
    )
    VALUES (
        old.name_id,
        new.name_id,
        old.temperature,
        new.temperature,
        old.date,
        new.date,
        old.fatigue,
        new.fatigue,
        old.tpain,
        new.tpain,
        old.other,
        new.other,
        CURRENT_TIMESTAMP
        );
END;

CREATE TRIGGER IF NOT EXISTS log_remove
    AFTER DELETE ON data
BEGIN
    INSERT INTO removelog (
        old_id,
        old_name_id,
        old_temp,
        old_date,
        old_fatigue,
        old_tpain,
        old_other,
        del_time
    )
    VALUES (
        old.id,
        old.name_id,
        old.temperature,
        old.date,
        old.fatigue,
        old.tpain,
        old.other,
        CURRENT_TIMESTAMP
            );

END;

