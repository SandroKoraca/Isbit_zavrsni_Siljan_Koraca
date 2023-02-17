// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    address public owner;

    event Transfer(address indexed from, address indexed to, uint256 value);
    /*
    event Approval(address indexed owner, address indexed spender, uint256 value);
    */
    event Mint(address indexed account, uint256 amount);
    event Burn(address indexed account, uint256 amount);

    constructor(string memory _name, string memory _symbol, uint8 _decimals, uint256 _totalSupply) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _totalSupply;
        balanceOf[msg.sender] = totalSupply;
        owner = msg.sender;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        /*
        emit Transfer(msg.sender, _to, _value);
        */
        return true;
        
    }

    /*
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    */

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= balanceOf[_from], "Insufficient balance");
        require(_value <= allowance[_from][msg.sender], "Insufficient allowance");
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        /*
        emit Transfer(_from, _to, _value);
        */
        return true;
    }

    function ballanceOf(address _owner) public view returns (uint256){
        return balanceOf[_owner];
    }

    function mint(address _account, uint256 _amount) public {
        require(msg.sender == owner, "Only the owner can mint tokens");
        totalSupply += _amount;
        balanceOf[_account] += _amount;
        /*
        emit Mint(_account, _amount);
        */
    }

    function burn(uint256 _amount) public {
        require(msg.sender == owner, "Only the owner can burn tokens");
        require(_amount <= balanceOf[msg.sender], "Insufficient balance");
        totalSupply -= _amount;
        balanceOf[msg.sender] -= _amount;
        /*
        emit Burn(msg.sender, _amount);
        */
    }
}