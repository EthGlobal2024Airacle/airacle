// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "./bot.sol";
import "./nobots_token.sol";

contract BotClaimDistributor {
    BotChecker public botChecker;
    NOBOTS public nobotsToken;
    mapping(address => uint256) public claimResults;

    event Claimed(address indexed user, bytes32 requestId);
    event Distributed(address indexed user, uint256 result, uint256 tokensMinted);

    constructor(address _botCheckerAddress, address _nobotsTokenAddress) {
        botChecker = BotChecker(_botCheckerAddress);
        nobotsToken = NOBOTS(_nobotsTokenAddress);
    }

    function claim() external {
        bytes32 requestId = botChecker.check_bot(msg.sender, this.distribute);
        emit Claimed(msg.sender, requestId);
    }

    function distribute(uint256 result) external {
        require(msg.sender == address(botChecker), "Only bot checker can call distribute");
        address user = tx.origin;
        claimResults[user] = result;

        uint256 tokensMinted = 0;
        if (result < 70) {
            tokensMinted = 1000 * 10**18; // 1000 tokens with 18 decimals
            nobotsToken.mint(user, tokensMinted);
        }

        emit Distributed(user, result, tokensMinted);
    }
}