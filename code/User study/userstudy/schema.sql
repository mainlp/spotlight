DROP TABLE IF EXISTS participant;
DROP TABLE IF EXISTS submission_step;

CREATE TABLE participant (
  id TEXT PRIMARY KEY NOT NULL,
  experiment_order TEXT NOT NULL,
  experiment_variations TEXT NOT NULL,
  demographics TEXT,
  finished BOOLEAN DEFAULT 0
);

CREATE TABLE submission_step (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  participant_id TEXT NOT NULL,
  step_start_time INTEGER NOT NULL,
  step_submit_time INTEGER NOT NULL,
  experiment_id INTEGER NOT NULL,
  variation_id INTEGER NOT NULL,
  submission_text TEXT NOT NULL,
  FOREIGN KEY (participant_id) REFERENCES participant (id)
);