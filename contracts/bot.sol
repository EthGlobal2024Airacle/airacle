// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import {FunctionsClient} from "@chainlink/contracts@1.1.1/src/v0.8/functions/v1_0_0/FunctionsClient.sol";
import {ConfirmedOwner} from "@chainlink/contracts@1.1.1/src/v0.8/shared/access/ConfirmedOwner.sol";
import {FunctionsRequest} from "@chainlink/contracts@1.1.1/src/v0.8/functions/v1_0_0/libraries/FunctionsRequest.sol";

contract BotChecker is FunctionsClient, ConfirmedOwner {
    using FunctionsRequest for FunctionsRequest.Request;

    bytes32 public s_lastRequestId;
    bytes public s_lastResponse;
    bytes public s_lastError;

    error UnexpectedRequestID(bytes32 requestId);

    event Response(
        bytes32 indexed requestId,
        uint256 result,
        bytes response,
        bytes err
    );

    address router = 0x234a5fb5Bd614a7AA2FfAB244D603abFA0Ac5C5C;

    string source =

    "const wallet = args[0]"
    "const apiResponse = await Functions.makeHttpRequest({"
    "url: 'https://stopairdropbots.xyz/claimCheck/${wallet}',"
    "method: 'GET'});"
    "return Functions.encodeUint256(apiResponse.data);";


    uint32 gasLimit = 300000;

    bytes32 donID =
        0x66756e2d617262697472756d2d7365706f6c69612d3100000000000000000000;

    uint256 public lastResult;

    mapping(bytes32 => address) private requestToAddress;
    mapping(bytes32 => function(uint256) external) private requestToCallback;

    constructor() FunctionsClient(router) ConfirmedOwner(msg.sender) {}

    function check_bot(address userAddress, function(uint256) external callback) external returns (bytes32) {
        string[] memory args = new string[](1);
        args[0] = addressToString(userAddress);

        FunctionsRequest.Request memory req;
        req.initializeRequestForInlineJavaScript(source);
        req.setArgs(args);

        bytes32 requestId = _sendRequest(
            req.encodeCBOR(),
            142, // Replace with your actual subscriptionId
            gasLimit,
            donID
        );

        requestToAddress[requestId] = userAddress;
        requestToCallback[requestId] = callback;

        return requestId;
    }

    function fulfillRequest(
        bytes32 requestId,
        bytes memory response,
        bytes memory err
    ) internal override {

        // s_lastResponse = response;
        // s_lastError = err;

        uint256 result = abi.decode(response, (uint256));
        //lastResult = result;

        //emit Response(requestId, result, s_lastResponse, s_lastError);

        // Call the stored callback function
        function(uint256) external callback = requestToCallback[requestId];
        if (callback.selector != bytes4(0)) {
            callback(result);
        }


        // Clean up the mappings
        // delete requestToAddress[requestId];
        // delete requestToCallback[requestId];
    }

    function addressToString(address _address) internal pure returns (string memory) {
        bytes32 value = bytes32(uint256(uint160(_address)));
        bytes memory alphabet = "0123456789abcdef";
        bytes memory str = new bytes(42);
        str[0] = '0';
        str[1] = 'x';
        for (uint256 i = 0; i < 20; i++) {
            str[2 + i * 2] = alphabet[uint8(value[i + 12] >> 4)];
            str[3 + i * 2] = alphabet[uint8(value[i + 12] & 0x0f)];
        }
        return string(str);
    }
}