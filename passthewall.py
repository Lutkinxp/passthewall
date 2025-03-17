import itertools
import string
import time
import sys
import threading
import logging
import argparse
import mmap
import hashlib
from tqdm import tqdm
from passlib.hash import nthash  # For NTLM hash comparison

# Global variables
result = None
attempts = 0
lock = threading.Lock()
stop_event = threading.Event()  # Used for timeout handling

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def hash_password(plaintext, hash_type):
    """Generate hash from a plaintext password to compare against."""
    if hash_type == "md5":
        return hashlib.md5(plaintext.encode()).hexdigest()
    elif hash_type == "sha256":
        return hashlib.sha256(plaintext.encode()).hexdigest()
    elif hash_type == "ntlm":
        return nthash.hash(plaintext)  # NTLM hashing
    else:
        raise ValueError("Unsupported hash type. Use md5, sha256, or ntlm.")

def check_password(guess, target_hash, hash_type):
    """Check if a guessed password matches the hash."""
    return hash_password(guess, hash_type) == target_hash

def brute_force_worker(target, max_length, chars, start_index, step, hash_type=None):
    """Brute-force worker function for multi-threading."""
    global attempts, result
    for length in range(1, max_length + 1):
        for i, guess_tuple in enumerate(itertools.islice(itertools.product(chars, repeat=length), start_index, None, step)):
            if stop_event.is_set():
                return  # Stop if timeout reached
            guess = ''.join(guess_tuple)
            with lock:
                attempts += 1
                if (hash_type and check_password(guess, target, hash_type)) or (guess == target):
                    result = guess
                    stop_event.set()  # Notify all threads to stop
                    return

def threaded_brute_force(target, max_length, chars, num_threads, hash_type=None):
    """Manages multiple threads for brute-force attack."""
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=brute_force_worker, args=(target, max_length, chars, i, num_threads, hash_type))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def dictionary_attack(target, dictionary_file, hash_type=None):
    """Attempts to find the password using a dictionary attack."""
    global attempts, result
    try:
        with open(dictionary_file, 'r+b') as file:
            mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            for line in iter(mmapped_file.readline, b""):
                if stop_event.is_set():
                    return  # Stop if timeout reached
                guess = line.strip().decode('utf-8')
                with lock:
                    attempts += 1
                    if (hash_type and check_password(guess, target, hash_type)) or (guess == target):
                        result = guess
                        stop_event.set()  # Notify all threads to stop
                        return
    except FileNotFoundError:
        logging.error(f"Dictionary file {dictionary_file} not found.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Brute-force & Dictionary-based password and hash cracker")
    parser.add_argument("target", help="The target password or hash to crack")
    parser.add_argument("max_length", type=int, help="Maximum length of the password to try")
    parser.add_argument("num_threads", type=int, help="Number of threads to use")
    parser.add_argument("--charset", default=string.ascii_letters + string.digits + string.punctuation, help="Character set to use for brute-force")
    parser.add_argument("--dictionary", help="Dictionary file for dictionary attack")
    parser.add_argument("--timeout", type=int, help="Timeout in seconds for the brute-force attack")
    parser.add_argument("--hash", choices=["md5", "sha256", "ntlm"], help="Hash type if cracking a hash")

    args = parser.parse_args()

    target = args.target
    max_length = args.max_length
    num_threads = args.num_threads
    chars = args.charset
    dictionary_file = args.dictionary
    timeout = args.timeout
    hash_type = args.hash

    if hash_type:
        logging.info(f"Cracking {hash_type.upper()} hash: {target}")
    else:
        logging.info(f"Cracking plain password: {target}")

    logging.info(f"Maximum password length to try: {max_length}")
    logging.info(f"Number of threads: {num_threads}")
    logging.info(f"Character set: {chars}")

    start_time = time.time()

    # Try dictionary attack first
    if dictionary_file:
        logging.info("Starting dictionary attack...")
        dictionary_attack(target, dictionary_file, hash_type)
        if result:
            end_time = time.time()
            logging.info(f"\nPassword cracked (dictionary): {result}")
            logging.info(f"Attempts: {attempts}")
            logging.info(f"Time elapsed: {end_time - start_time:.2f} seconds")
            return

    # If dictionary attack fails, proceed with brute-force
    logging.info("Starting brute-force attack...")
    total_combinations = sum(len(chars) ** length for length in range(1, max_length + 1))

    with tqdm(total=total_combinations, desc="Progress", unit="attempt") as pbar:
        def update_progress():
            while not stop_event.is_set():
                with lock:
                    pbar.n = attempts
                    pbar.refresh()
                time.sleep(0.5)

        progress_thread = threading.Thread(target=update_progress, daemon=True)
        progress_thread.start()

        brute_force_thread = threading.Thread(target=threaded_brute_force, args=(target, max_length, chars, num_threads, hash_type))
        brute_force_thread.start()

        if timeout:
            brute_force_thread.join(timeout)
            if brute_force_thread.is_alive():
                stop_event.set()  # Stop all threads
                logging.warning("Timeout reached. Stopping the brute-force attack.")
                return
        else:
            brute_force_thread.join()

    end_time = time.time()

    if result:
        logging.info(f"\nPassword cracked (brute-force): {result}")
        logging.info(f"Attempts: {attempts}")
        logging.info(f"Time elapsed: {end_time - start_time:.2f} seconds")
    else:
        logging.info("\nPassword not cracked within the given constraints.")

if __name__ == "__main__":
    main()