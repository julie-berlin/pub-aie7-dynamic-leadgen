#!/usr/bin/env python3
"""Generate test data for Sparkle Clean Solutions client"""

from generate_single_client import generate_client_leads

if __name__ == "__main__":
    print(generate_client_leads('sparkle_clean', 30))