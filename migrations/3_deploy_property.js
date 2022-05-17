const property = artifacts.require("property");

module.exports = function (deployer) {
  deployer.deploy(property);
};
