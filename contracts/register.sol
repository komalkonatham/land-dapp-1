// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {
  uint[] _ids;
  string[] _names;
  uint[] _passwords;
  address admin;

  constructor()  {
    admin=msg.sender;
  }

  


}
