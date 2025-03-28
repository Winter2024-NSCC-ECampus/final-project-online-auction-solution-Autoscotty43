# Unique Bid Blind On-line Auction System (Python Implementation)

This Python script implements a simplified Unique Bid Blind On-line Auction system. Bidders submit bids within a specified time frame. The winner is the bidder who placed the highest bid that is unique (not matched by any other bidder). If there's a tie for the highest bid, the auction restarts with the minimum bid incremented. Optionally, the system can be configured to award the win to the bidder who placed the highest tied bid first.

## Features

* **Timed Auctions:** Auctions have a defined duration for bidding.
* **Minimum Bid Enforcement:** Bids below the set minimum are discarded.
* **Unique Highest Bid Winner:** The bidder with the highest unique bid wins.
* **Tie Handling:** If the highest bid has multiple participants, the auction restarts with an increased minimum bid.
* **Optional Tie-Breaking by Timestamp:** The system can be configured (as implemented) to award the win to the bidder who placed the highest tied bid earliest.
* **Simulated Bidding:** Includes a function to simulate multiple users placing bids concurrently for testing purposes.
* **Basic Auction Restart Logic:** Implements a loop to handle auction restarts due to ties.

## Getting Started

1.  **Save the code:** Save the provided Python code as a `.py` file (e.g., `unique_auction.py`).
2.  **Run the script:** Execute the script from your terminal using `python unique_auction.py`.

## How to Use

1.  **Initialization:** The `UniqueBidAuction` class is initialized with a `min_bid` (the starting minimum bid for the auction) and `auction_duration_seconds` (the length of the bidding period in seconds).
2.  **Starting the Auction:** Call the `start_auction()` method to begin the bidding period. This will set the auction to open and start the timer.
3.  **Placing Bids:** The `place_bid(bid)` method allows bidders to submit bids. It takes a `Bid` object as input, which contains the `bidder_id` and `bid_amount`. Bids are accepted only if the auction is open, the current time is within the auction duration, and the bid amount is greater than or equal to the current minimum bid.
4.  **Determining the Winner:** Once the auction duration has elapsed, call the `determine_winner()` method.
    * If a unique highest bid exists, it returns the `bidder_id` of the winner.
    * If there's a tie at the highest bid, it returns a special tuple `(-1, new_min_bid)` to signal a restart and provide the new minimum bid.
    * If no bids were placed, it returns `None`.
5.  **Auction Restart:** The main execution block (`if __name__ == "__main__":`) demonstrates how to handle auction restarts. If `determine_winner()` indicates a tie, a new auction instance is created with the updated minimum bid.
6.  **Simulated Bidding:** The `simulate_bidding(auction)` function simulates multiple bidders placing bids with different delays to test the system.

## Code Structure

* **`Bid` Class:** A simple class to represent a bid, containing the `bidder_id`, `bid_amount`, and a `timestamp` of when the bid was placed.
* **`UniqueBidAuction` Class:**
    * `__init__(self, min_bid, auction_duration_seconds)`: Initializes the auction with a minimum bid, duration, and data structures to store bids.
    * `start_auction(self)`: Starts the auction timer and sets the auction to open.
    * `place_bid(self, bid)`: Records a bid if it meets the criteria (auction open, within time limit, above minimum bid).
    * `determine_winner(self)`: Determines the winner based on the highest unique bid, handling ties by signaling a restart.
* **`simulate_bidding(auction)` Function:** Simulates multiple bidders placing bids concurrently.
* **`if __name__ == "__main__":` Block:** Contains the main execution logic, including setting up the auction, simulating bids, and determining/announcing the winner (and handling restarts).

## Data Structures Used

* **`defaultdict(list) bids_by_amount`:** Stores bids organized by the bid amount. The keys are the bid amounts, and the values are lists of `(timestamp, bidder_id)` tuples for all bids at that amount. This is used to efficiently find the highest bids and identify ties, while also preserving the order of bids for tie-breaking.
* **`defaultdict(set) bids_by_bidder`:** Stores the unique bid amounts placed by each bidder. The keys are the bidder IDs, and the values are sets of the unique bid amounts they have submitted.

## Tie-Breaking Rule

The current implementation uses the following tie-breaking rule: if multiple bidders place the same highest bid, the bidder who placed that bid earliest (based on the timestamp) is declared the winner.

## Potential Improvements (as discussed previously)

* More explicit auction restart mechanism within the `UniqueBidAuction` class.
* More robust error handling.
* Clearer indication of auction end.
* More sophisticated concurrency management for high bid volumes.
* Logging of auction events.
* More realistic bidding simulation.
* Consider using a priority queue (heap) for potential performance optimizations in winner determination for very large datasets.

## Author

Jared Scott

## Screenshots

![image](https://github.com/user-attachments/assets/d42b57d9-1d72-4d88-8a1f-94cd7bdd8b87)

