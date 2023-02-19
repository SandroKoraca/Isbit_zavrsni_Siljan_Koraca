// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {
    string public name;
    string public symbol;
    uint256 public totalSupply;

    mapping(address => uint256) public balances;

    address public owner;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Mint(address indexed account, uint256 amount);
    event Burn(address indexed account, uint256 amount);

    constructor(string memory _name, string memory _symbol, uint256 _totalSupply) {
        name = _name;
        symbol = _symbol;
        totalSupply = _totalSupply;
        balances[msg.sender] = totalSupply;
        owner = msg.sender;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balances[msg.sender] >= _value, "Nedovoljno sredstava na racunu");
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
        
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= balances[_from], "Nedovoljno sredstava na racunu");
        balances[_from] -= _value;
        balances[_to] += _value;
        emit Transfer(_from, _to, _value);
        return true;
    }

    function ballanceOf(address _account) public view returns (uint256){
        return balances[_account];
    }

    function mint(address _account, int _amount) public {
        require(msg.sender == owner, "Samo vlasnik smije dodavati tokene");
        totalSupply += uint256(_amount);
        balances[_account] += uint256(_amount);
        emit Mint(_account, uint256(_amount));
    }

    function burn(address _account, uint256 _amount) public {
        require(msg.sender == owner, "Samo vlasnik smije oduzimati tokene");
        require(_amount <= balances[_account], "Nedovoljno sredstava na racunu");
        totalSupply -= _amount;
        balances[_account] -= _amount;
        emit Burn(_account, _amount);
    }
}