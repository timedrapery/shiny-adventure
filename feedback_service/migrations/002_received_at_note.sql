-- A row imported from the form sheet whose timestamp could not be read is
-- stored with the import time instead. This column says so, so the stored
-- time is never mistaken for when the reader actually responded.
ALTER TABLE submissions ADD COLUMN received_at_note TEXT NOT NULL DEFAULT '';
