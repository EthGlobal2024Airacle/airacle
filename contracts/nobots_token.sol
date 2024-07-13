pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NOBOTS is ERC20, Ownable {
    mapping(address => bool) public minters;

    constructor(address initialMinter) ERC20("NOBOTS", "NBTS") Ownable(msg.sender) {
        minters[initialMinter] = true;
    }

    modifier onlyMinter() {
        require(minters[msg.sender], "Only a minter can call this function");
        _;
    }

    function addMinter(address newMinter) public onlyOwner {
        minters[newMinter] = true;
    }

    function removeMinter(address minter) public onlyOwner {
        minters[minter] = false;
    }

    function mint(address to, uint256 amount) public onlyMinter {
        _mint(to, amount);
    }

    function isMinter(address account) public view returns (bool) {
        return minters[account];
    }
}