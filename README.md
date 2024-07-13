# AI-Powered Oracle to Combat Airdrop Farming

## Background

Airdrop farming, where users exploit token distribution campaigns by creating multiple wallet addresses, has become a significant issue in the cryptocurrency ecosystem. This project aims to address this problem by providing an AI-powered oracle that can detect and prevent airdrop farming, ensuring fair token distribution and maintaining the integrity of blockchain projects.

## Project Overview

This project implements an AI-powered oracle built on Chainlink and deployed on the Arbitrum blockchain. It uses advanced machine learning and graph analysis techniques to detect airdrop farming in real-time, leveraging Blockscout for data collection.

### Key Components

1. **Airdrop Smart Contract**: A demo contract that integrates with the oracle to verify claim requests.
2. **Chainlink Oracle**: Facilitates communication between the smart contract and our backend service.
3. **Backend Service**: Performs real-time analysis of wallet activities to detect airdrop farming.

## How It Works

1. When a user attempts to claim an airdrop, the smart contract queries our Chainlink oracle.
2. The oracle calls our backend service, which initiates the analysis process.
3. The backend service uses Blockscout to fetch data about the wallet's interactions on the Arbitrum blockchain.
4. An AI model analyzes this data to determine the likelihood of the wallet being part of an airdrop farm.
5. The oracle returns a probability score to the smart contract.
6. The smart contract decides whether to allow or block the claim based on a predefined threshold.

## AI-Powered Analysis

Our solution employs a sophisticated AI model that:

1. Explores the activity around the wallet in real-time.
2. Queries the wallets and contracts it has interacted with.
3. Incrementally explores interactions of other addresses in the neighborhood.
4. Builds a neighborhood graph using random sampling.
5. Detects communities inside the constructed graph, isolating highly relevant addresses.
6. Applies a similarity model to check how likely the community behaves together.
7. Determines if the community is forming an airdrop farm based on behavioral patterns.

## Technology Stack

- **Blockchain**: Arbitrum
- **Oracle Service**: Chainlink
- **Data Source**: Blockscout
- **Graph Analysis**: NetworkX
- **Backend**: Python Flask

## Code References

- **Arbitrum**: Our solution is designed to work on the Arbitrum blockchain. See `blockchain_data_fetcher.py` for API calls to Arbitrum's Blockscout instance.
- **Chainlink**: While not explicitly shown in the provided code, the project integrates with Chainlink for oracle services. This would typically be implemented in the smart contract code.
- **Blockscout**: Data fetching from Blockscout is implemented in `blockchain_data_fetcher.py`. The `BASE_URL` in this file points to Arbitrum's Blockscout API.

## Getting Started

(Here you would include instructions on how to set up and run the project, including any necessary environment setup, dependencies, and configuration steps.)

## Future Work

- Enhance the AI model with more sophisticated machine learning techniques.
- Expand support to other blockchain networks.
- Implement additional features for detecting various types of blockchain-based fraud.

## Contributors

(List of project contributors)

## License

(Specify the project's license)