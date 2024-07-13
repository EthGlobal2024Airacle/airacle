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

Our system employs a range of techniques to detect airdrop farming, with a focus on extensibility and community involvement. The core methods currently implemented include:

1. **Efficient Graph Exploration**: We utilize advanced random sampling techniques to explore the transaction graph. This approach focuses on dense "areas" of activity, making the exploration highly efficient and targeted. By prioritizing regions with high interaction frequency, we can quickly identify potential hotspots of coordinated behavior.

2. **Community Detection**: Building on our graph exploration, we employ similarity-based connections to detect communities within the network. Our approach initially uses the Louvain algorithm to identify core communities, which are then refined using additional similarity metrics. This multi-step process allows us to isolate clusters of addresses that exhibit coordinated behavior.

3. **Jaccard Similarity**: This metric is used to quantify the overlap in transaction patterns between addresses, helping to identify clusters of potentially related wallets. It serves as a key component in our similarity-based community detection.

Our system is designed with extensibility in mind, allowing for the integration of various sophisticated techniques to enhance airdrop farming detection. While some of these methods are in development or planned for future iterations, the system's architecture facilitates their seamless integration:

4. **Temporal Pattern Analysis**: The system's data collection and analysis pipelines are structured to support time series analysis. This could be utilized to detect synchronized actions across multiple addresses, a potential indicator of bot-driven farming.

5. **LLM-based Signals**: The system is prepared to leverage state-of-the-art language models for analyzing transaction metadata and smart contract interactions. This could potentially extract semantic signals indicative of coordinated behavior.

6. **External Signals and Blacklists**: The architecture supports integration with external data sources and blacklists. This feature could incorporate known patterns of malicious behavior, enhancing the system's detection capabilities.

7. **Transfer Learning**: The system is designed to accommodate knowledge transfer techniques. This could allow leveraging insights from previous malicious campaigns, potentially enabling quick adaptation to new exploitation strategies.

8. **Anomaly Detection**: The framework is ready for the implementation of unsupervised learning techniques. These could be used to identify unusual patterns that deviate from normal blockchain activity.

9. **Node Embedding**: Advanced graph embedding techniques can be employed to represent addresses in a high-dimensional space, potentially allowing for more nuanced similarity comparisons.

10. **GNN-based Classification**: Our architecture is primed for the integration of Graph Neural Networks (GNNs). This approach could offer several potential advantages:

   - **Community Detection Enhancement**: GNNs could refine and improve our initial community detection results.
   - **Adaptive Learning**: As the system detects and confirms airdrop farming attempts, these identified communities could potentially be used as training data for the GNN, creating a feedback loop to continually improve detection.
   - **Structural Analysis**: GNNs could capture complex relationships and structures within blockchain transaction graphs, potentially detecting subtle patterns in farming community formation.
   - **Feature Aggregation**: By aggregating features from neighboring nodes, GNNs could capture not just individual wallet behavior, but also characteristics of the wallet's transaction neighborhood.
   - **Scalability**: GNNs could efficiently process large-scale graph data, making them suitable for analyzing extensive blockchain networks.
   - **Robustness**: As the GNN learns from confirmed farming instances, it could become increasingly robust in detecting new, previously unseen farming strategies.

The open and public nature of blockchain data presents unique opportunities for the crypto community to collaborate on improving detection methods. As these techniques are developed and refined, they could be easily integrated into our extensible system. Moreover, the transparency of on-chain data allows for potential portability of these methods across different blockchain networks, fostering a collaborative approach to combating airdrop farming across the entire crypto ecosystem.

By providing this flexible and extensible framework, we aim to create a foundation upon which the community can build and improve, leveraging collective expertise to stay ahead of evolving airdrop farming techniques.

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