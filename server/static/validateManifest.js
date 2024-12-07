var validate = require("web-app-manifest-validator");
var manifest = require("./manifest.json");

validate(manifest).forEach(function (error) {
  console.log(error);
});
