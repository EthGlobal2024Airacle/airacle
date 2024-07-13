import os

from flask import Flask, send_from_directory, request, redirect

from farm_detection.address_fetcher import Investigator
from farm_detection.blockchain_analyzer import BlockchainAnalyzer
from farm_detection.blockchain_data_fetcher import BlockchainDataFetcher

app = Flask(__name__)


@app.before_request
def before_request():
    if not request.is_secure and app.env != "development":
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)


@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.route('/claimCheck/', defaults={'address': '0x9E8Ab5Ed0E6275f0d0b837971e74Dd97a3e8E04d'})
@app.route('/claimCheck/<address>')
def get_claim_bot_check(address: str):
    fetcher = BlockchainDataFetcher()
    analyzer = BlockchainAnalyzer(address, fetcher)
    analyzer.analyze(max_queries=2)
    subgraph = analyzer.get_community_subgraph()
    investigator = Investigator(subgraph, fetcher)
    investigator.enrich_community()
    return str(int(round(investigator.evaluate_farmness(address) * 100, 0)))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
