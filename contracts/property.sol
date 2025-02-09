// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract property {
  
  address admin;
  uint[] _propertyId;
  uint[][] _ownerId;
  string[] _propertyData;
  string[] _size;
   
  
  mapping(uint => bool) registeredProperties;

  constructor() {
      admin=msg.sender;
  }

  modifier onlyAdmin {
    require(admin==msg.sender);
    _;
  }

  function registerProperty(uint propertyId,uint ownerId,string memory propertyData,string memory propertysize) public {

    require(!registeredProperties[propertyId]);

    registeredProperties[propertyId]=true;
    _propertyId.push(propertyId);
    _ownerId.push([ownerId]);
    _propertyData.push(propertyData);
    _size.push(propertysize);
    
  }

  function viewProperties() public view returns(uint[] memory,uint[][] memory,string[] memory,string[] memory) {
    return (_propertyId,_ownerId,_propertyData,_size);
  }

  function buyProperty(uint propertyID, uint newOwner) public{
      uint i;
      for(i=0;i<_propertyId.length;i++) {
        if(_propertyId[i]==propertyID) {
            
          _ownerId[i].push(newOwner);
        }
      }

  }

  
}
