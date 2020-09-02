
INSERT INTO location (id, name, x, y) VALUES
('fdfb6df5-aecd-4c8f-8574-c2fc7a3bafa2', 'Washington, DC', 0, 0),
('171d238c-e20f-4ed1-bfe6-724081782cc5', 'Richmond, VA', 1, 1);

INSERT INTO location_tag(id, location_id, tag) VALUES
-- Washington, DC
('09a6a3e9-9a63-4c50-b9b6-a57af1fc0407', 'fdfb6df5-aecd-4c8f-8574-c2fc7a3bafa2', 'CAPITOL'),
-- Richmond, VA
('ad5eddf0-dc63-441b-8082-566b9449f35b', '171d238c-e20f-4ed1-bfe6-724081782cc5', 'CAPITOL');
