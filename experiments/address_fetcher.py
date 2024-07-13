from experiments.blockchain_analyzer import BlockchainAnalyzer


def main():
    initial_address = '0x7Bb79cE20e464062Ae265A0a9D03F3e6a9200501'
    analyzer = BlockchainAnalyzer(initial_address)
    analyzer.analyze()
    subgraph = analyzer.get_community_subgraph()
    analyzer.visualize()


if __name__ == "__main__":
    main()
