from collections import defaultdict
import time
import threading

class Bid:
    def __init__(self, bidder_id, bid_amount):
        self.bidder_id = bidder_id
        self.bid_amount = bid_amount
        self.timestamp = time.time()

class UniqueBidAuction:
    def __init__(self, min_bid, auction_duration_seconds):
        self.min_bid = min_bid
        self.auction_duration = auction_duration_seconds
        self.bids_by_amount = defaultdict(list)
        self.bids_by_bidder = defaultdict(set)
        self.auction_open = False
        self.auction_end_time = None
        self.lock = threading.Lock()

    def start_auction(self):
        with self.lock:
            if not self.auction_open:
                self.auction_open = True
                self.auction_end_time = time.time() + self.auction_duration
                print(f"Auction started with minimum bid ${self.min_bid}. Bidding closes in {self.auction_duration} seconds.")
                self.bids_by_amount.clear() # Clear bids from previous rounds
                self.bids_by_bidder.clear()
                return True
            else:
                print("Auction is already open.")
                return False

    def place_bid(self, bid):
        with self.lock:
            if self.auction_open and time.time() < self.auction_end_time:
                if bid.bid_amount >= self.min_bid:
                    self.bids_by_amount[bid.bid_amount].append((bid.timestamp, bid.bidder_id))
                    self.bids_by_bidder[bid.bidder_id].add(bid.bid_amount)
                    print(f"Bid of ${bid.bid_amount} placed by bidder {bid.bidder_id}.")
                    return True
                else:
                    print(f"Bid of ${bid.bid_amount} is below the minimum bid of ${self.min_bid}.")
                    return False
            else:
                print("Auction is closed. Bids are no longer accepted.")
                return False

    def determine_winner(self):
        with self.lock:
            if self.auction_open and time.time() < self.auction_end_time:
                print("Auction is still open. Cannot determine winner yet.")
                return None

            if not self.bids_by_amount:
                print("No bids were placed.")
                return None

            sorted_bids = sorted(self.bids_by_amount.items(), key=lambda item: item[0], reverse=True)

            for amount, bids in sorted_bids:
                if len(bids) == 1:
                    return bids[0][1]
                elif len(bids) > 1:
                    print(f"Tie at ${amount}. Restarting auction with minimum bid ${amount + 1}.")
                    return -1, amount + 1 # Return a signal for restart and the new min bid

            return None

def simulate_bidding(auction):
    # Simulate different users placing bids at different times
    threading.Thread(target=lambda: time.sleep(1) or auction.place_bid(Bid(1, 22))).start()
    threading.Thread(target=lambda: time.sleep(2) or auction.place_bid(Bid(2, 27))).start()
    threading.Thread(target=lambda: time.sleep(3) or auction.place_bid(Bid(1, 27))).start() # Tie
    threading.Thread(target=lambda: time.sleep(4) or auction.place_bid(Bid(3, 32))).start()
    threading.Thread(target=lambda: time.sleep(5) or auction.place_bid(Bid(2, 32))).start() # Tie
    threading.Thread(target=lambda: time.sleep(6) or auction.place_bid(Bid(4, 37))).start()
    threading.Thread(target=lambda: time.sleep(7) or auction.place_bid(Bid(1, 37))).start() # Tie, bidder 4 was first
    threading.Thread(target=lambda: time.sleep(auction.auction_duration + 1) or auction.place_bid(Bid(5, 40))).start() # Bid after auction ends

if __name__ == "__main__":
    initial_min_bid = 20
    auction_duration = 5 # Shorter duration for testing restarts

    while True:
        auction = UniqueBidAuction(min_bid=initial_min_bid, auction_duration_seconds=auction_duration)
        if auction.start_auction():
            simulate_bidding(auction)
            time.sleep(auction_duration + 1)
            result = auction.determine_winner()

            if isinstance(result, tuple) and result[0] == -1:
                initial_min_bid = result[1]
                print(f"Restarting auction with minimum bid: ${initial_min_bid}\n")
            elif result:
                print(f"\nAuction closed. The winner is bidder: {result}")
                break
            else:
                print("\nAuction closed. No unique winner found in this round.")
                break # Or potentially restart with the same min bid depending on requirements
        else:
            break