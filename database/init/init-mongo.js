db = db.getSiblingDB("admin");
db.createUser({
  user: "openuser",
  pwd: "openpassword",
  roles: [ { role: "readWrite", db: "opendb" } ]
});

db = db.getSiblingDB("opendb");
db.createCollection("City");
db.createCollection("Weather");
db.createCollection("DailyWeather");
db.createCollection("AirPollution");