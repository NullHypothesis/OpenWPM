const data = require("sdk/self").data;
var loggingDB = require("./loggingdb.js");

exports.run = function(crawlID) {
  // Create sql tables
  var createCookieBannerTable = data.load("create_cookie_banners_table.sql");
  loggingDB.executeSQL(createCookieBannerTable, false);
};
