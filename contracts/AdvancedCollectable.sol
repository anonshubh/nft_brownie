// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectable is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    enum Type {
        CHARACTER,
        SCENE
    }
    mapping(uint256 => Type) public tokenIdToType;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectable(bytes32 indexed requestId, address requester);
    event typeAssigned(uint256 indexed tokenId, Type tp);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("popArt", "POP")
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectable() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectable(requestId,msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Type tp = Type(randomNumber % 2);
        uint256 newTokenId = tokenCounter;
        tokenIdToType[newTokenId] = tp;
        emit typeAssigned(newTokenId,tp);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 _tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), _tokenId),
            "ERC721: Caller is not Owner nor approved!"
        );
        _setTokenURI(_tokenId, _tokenURI);
    }
}
