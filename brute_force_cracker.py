import itertools
import string
import time
import sys
import threading
import logging
import argparse

# Global variables to store the result and attempts
result = None
attempts = 0
lock = threading.Lock() 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def brute_force_password(target_password, max_length, chars):
    global attempts, result
    for length in range(1, max_length + 1):
        for guess in itertools.product(chars, repeat=length):
            guess = ''.join(guess)
            with lock:
                attempts += 1

            if guess == target_password:
                with lock:
                    result = guess
                return

def threaded_brute_force(target_password, max_length, chars, num_threads):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=brute_force_password, args=(target_password, max_length, chars))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def dictionary_attack(target_password, dictionary_file):
    global attempts, result
    try:
        with open(dictionary_file, 'r') as file:
            for line in file:
                guess = line.strip()
                with lock:
                    attempts += 1
                if guess == target_password:
                    with lock:
                        result = guess
                    return
    except FileNotFoundError:
        logging.error(f"Dictionary file {dictionary_file} not found.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Brute-force password cracker")
    parser.add_argument("target_password", help="The target password to crack")
    parser.add_argument("max_length", type=int, help="Maximum length of the password to try")
    parser.add_argument("num_threads", type=int, help="Number of threads to use")
    parser.add_argument("--charset", default=string.ascii_letters + string.digits + string.punctuation, help="Character set to use for brute-force")
    parser.add_argument("--dictionary", help="Dictionary file for dictionary attack")
    parser.add_argument("--timeout", type=int, help="Timeout in seconds for the brute-force attack")

    args = parser.parse_args()

    target_password = args.target_password
    max_length = args.max_length
    num_threads = args.num_threads
    chars = args.charset
    dictionary_file = args.dictionary
    timeout = args.timeout

    logging.info(f"Starting advanced brute-force attack on password: {target_password}")
    logging.info(f"Maximum password length to try: {max_length}")
    logging.info(f"Number of threads: {num_threads}")
    logging.info(f"Character set: {chars}")

    start_time = time.time()

    # First, try the dictionary attack if a dictionary file is provided
    if dictionary_file:
        logging.info("Starting dictionary attack...")
        dictionary_attack(target_password, dictionary_file)
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
            pbar.update(1)

        # Create a thread for brute-force attack
        def threaded_brute_force_with_progress():
            global attempts
            threaded_brute_force(target_password, max_length, chars, num_threads)
            pbar.n = attempts  # Update progress bar with the number of attempts
            pbar.refresh()

        # Start the brute-force attack
        thread = threading.Thread(target=threaded_brute_force_with_progress)
        thread.start()

        if timeout:
            thread.join(timeout)
            if thread.is_alive():
                logging.warning("Timeout reached. Stopping the brute-force attack.")
                return
        else:
            thread.join()

    end_time = time.time()

    if result:
        logging.info(f"\nPassword cracked (brute-force): {result}")
        logging.info(f"Attempts: {attempts}")
        logging.info(f"Time elapsed: {end_time - start_time:.2f} seconds")
    else:
        logging.info("\nPassword not cracked within the given constraints.")

if __name__ == "__main__":
    main()
