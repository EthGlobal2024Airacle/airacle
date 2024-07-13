# AI-Powered Oracle to Combat Airdrop Farming

## Background

Airdrop farming, where users exploit token distribution campaigns by creating multiple wallet addresses, has become a
significant issue in the cryptocurrency ecosystem. This project aims to address this problem by providing an AI-powered
oracle that can detect and prevent airdrop farming, ensuring fair token distribution and maintaining the integrity of
blockchain projects.

## Project Overview

This project implements an AI-powered oracle built on Chainlink and deployed on the Arbitrum blockchain. It uses
advanced machine learning and graph analysis techniques to detect airdrop farming in real-time, leveraging Blockscout
for data collection.

### Key Components

1. **Airdrop Smart Contract**: A demo contract that integrates with the Chainlink oracle to verify claim requests.
2. **Chainlink Oracle**: Facilitates communication between the smart contract and our backend service.
3. **Backend Service**: Performs real-time analysis of wallet activities to detect airdrop farming.

## How It Works

1. When a user attempts to claim an airdrop, the smart contract calls our Chainlink oracle.
2. The Chainlink oracle triggers our backend service, which initiates the analysis process.
3. The backend service uses Blockscout to fetch data about the wallet's interactions on the Arbitrum blockchain.
4. An AI model analyzes this data to determine the likelihood of the wallet being part of an airdrop farm.
5. The Chainlink oracle returns a probability score to the smart contract.
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

## Getting Started

Our AI-powered oracle for combating airdrop farming is built with a modular and extensible architecture. Here's an
overview of the main components and how to get started with the project.

### Project Structure

The project is organized into several key classes, each responsible for a specific aspect of the airdrop farming
detection process:

1. **BlockchainAnalyzer**: Orchestrates the overall analysis process.
2. **BlockchainDataFetcher**: Handles data retrieval from Blockscout.
3. **GraphBuilder**: Constructs the interaction graph from blockchain data.
4. **CommunityDetector**: Identifies communities within the graph.
5. **Investigator**: Performs detailed analysis on the communities to detect farming behavior.

### Main Classes and Their Roles

#### BlockchainAnalyzer

This class is the entry point for the analysis process. It coordinates the data fetching, graph building, and community
detection processes. It uses a sophisticated random sampling technique to explore the neighborhood of a given address,
balancing between depth and breadth of exploration.

#### BlockchainDataFetcher

Responsible for interacting with the Blockscout API to retrieve transaction data. It implements efficient pagination and
concurrent data fetching to optimize performance.

#### GraphBuilder

Constructs a multi-directed graph (MultiDiGraph) representation of the blockchain interactions. It handles both native
token transfers and various types of smart contract interactions (ERC20, ERC721).

#### CommunityDetector

Utilizes advanced community detection algorithms to identify clusters of closely interacting addresses within the graph.
It implements the Louvain method for community detection, which is known for its efficiency and effectiveness in large
networks.

#### Investigator

This class is the core of our AI-powered analysis. It employs a multi-faceted approach to detect airdrop farming:

1. **Graph-based Analysis**: Utilizes the structure of the interaction graph to identify suspicious patterns.
2. **Temporal Analysis**: Examines the timing and frequency of interactions to detect coordinated behavior.
3. **Similarity Metrics**: Implements various similarity measures to quantify the likelihood of addresses being part of
   a farming operation.

### Advanced Analytical Methods

Our system employs a range of sophisticated techniques to ensure accurate detection of airdrop farming:

1. **Node Embedding**: We use advanced graph embedding techniques to represent addresses in a high-dimensional space,
   allowing for nuanced similarity comparisons.

2. **Jaccard Similarity**: This metric is used to quantify the overlap in transaction patterns between addresses,
   helping to identify clusters of potentially related wallets.

3. **AI and LLM-based Signals**: We leverage state-of-the-art language models to analyze transaction metadata and smart
   contract interactions, extracting semantic signals that might indicate coordinated behavior.

4. **External Signals and Blacklists**: Our system integrates with external data sources and blacklists to incorporate
   known patterns of malicious behavior.

5. **Transfer Learning**: We apply knowledge transfer techniques to leverage insights from previous malicious campaigns,
   allowing our system to quickly adapt to new exploitation strategies.

6. **Anomaly Detection**: Employs unsupervised learning techniques to identify unusual patterns that deviate from normal
   blockchain activity.

7. **Temporal Pattern Analysis**: Utilizes time series analysis to detect synchronized actions across multiple
   addresses, a common indicator of bot-driven farming.

### Workflow

1. When a claim is initiated, the airdrop smart contract calls our Chainlink oracle.
2. The Chainlink oracle triggers the BlockchainAnalyzer, which starts by fetching recent transaction data for the
   claiming address.
3. The GraphBuilder constructs a local graph representation of the address's neighborhood.
4. The CommunityDetector identifies relevant clusters within this graph.
5. The Investigator then applies our suite of analytical methods to these communities.
6. A final risk score is computed, synthesizing all the signals from our various detection methods.
7. This score is returned to the smart contract via the Chainlink oracle, allowing for an informed decision on whether
   to allow the claim.

## Code References

- **Arbitrum**: Our solution is designed to work on the Arbitrum blockchain. See `blockchain_data_fetcher.py` for API
  calls to Arbitrum's Blockscout instance.
- **Chainlink**: The integration with Chainlink is implemented in the smart contract code. The contract calls the
  Chainlink oracle to request the airdrop farming risk assessment before processing a claim.
- **Blockscout**: Data fetching from Blockscout is implemented in `blockchain_data_fetcher.py`. The `BASE_URL` in this
  file points to Arbitrum's Blockscout API.

## Future Work

- Enhance the AI model with more sophisticated machine learning techniques.
- Expand support to other blockchain networks.
- Implement additional features for detecting various types of blockchain-based fraud.

## Contributors

- Nir Magenheim
- Eli Shalom
- Xenofon Kontouris

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

### GPL-3.0 License

The GNU General Public License is a free, copyleft license for software and other kinds of works.

The licenses for most software and other practical works are designed to take away your freedom to share and change the
works. By contrast, the GNU General Public License is intended to guarantee your freedom to share and change all
versions of a program--to make sure it remains free software for all its users.

When we speak of free software, we are referring to freedom, not price. Our General Public Licenses are designed to make
sure that you have the freedom to distribute copies of free software (and charge for them if you wish), that you receive
source code or can get it if you want it, that you can change the software or use pieces of it in new free programs, and
that you know you can do these things.

For the full license text, please see
the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).