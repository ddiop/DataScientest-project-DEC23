db = db.getSiblingDB("admin");
db.createUser({
  user: "openuser",
  pwd: "openpassword",
  roles: [ { role: "readWrite", db: "opendb" } ]
});

db = db.getSiblingDB("opendb");
db.createCollection("city");
db.createCollection("weather");
db.createCollection("dailyWeather");
db.createCollection("airPollution");