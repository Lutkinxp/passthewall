# passthewall
# Overview:

The passthwall.py script is a command-line tool designed for cracking passwords and hashes using two primary methods: brute-force attacks and dictionary attacks. The script is implemented in Python and utilizes multi-threading to enhance performance, allowing it to attempt multiple password guesses simultaneously. Below is a detailed description of its components and functionality:

# Key Features:

   Password and Hash Cracking:
        The script can crack both plain text passwords and hashed passwords (MD5, SHA256, NTLM).
        Users can specify whether they are cracking a password or a hash.

   Brute-Force Attack:
        The script generates all possible combinations of characters up to a specified maximum length.
        It supports a customizable character set, which can include letters, digits, and punctuation.
        Multi-threading is employed to distribute the workload across multiple threads, significantly speeding up the cracking process.

   Dictionary Attack:
        The script can read from a specified dictionary file containing potential passwords.
        It attempts to match each password in the dictionary against the target password or hash.

   Progress Tracking:
        The script uses the tqdm library to provide a visual progress bar that updates in real-time as attempts are made.
        It tracks the number of attempts made and displays this information to the user.

   Timeout Handling:
        Users can specify a timeout period for the brute-force attack. If the attack exceeds this duration, it will be terminated gracefully.

   Logging:
        The script logs important events and statuses, such as the start of attacks, successful cracks, and errors (e.g., file not found).
        Logging is configurable, allowing users to see detailed output during execution.

# Usage:

The script is executed from the command line with the following parameters:

    target: The password or hash to crack.
    max_length: The maximum length of the password to attempt.
    num_threads: The number of threads to use for the brute-force attack.
    --charset: (Optional) A custom character set for brute-force attempts.
    --dictionary: (Optional) A file containing potential passwords for the dictionary attack.
    --timeout: (Optional) A timeout in seconds for the brute-force attack.
    --hash: (Optional) Specifies the type of hash if cracking a hash (MD5, SHA256, NTLM).

Example Command:

    python passthwall.py <target> <max_length> <num_threads> --charset <charset> --dictionary <dictionary_file> --timeout <timeout> --hash <hash_type>

# Conclusion:

The passthwall.py script is a powerful and flexible tool for password recovery, suitable for security professionals and ethical hackers. It combines brute-force and dictionary attack methods, making it versatile for various scenarios. The use of multi-threading and progress tracking enhances its efficiency and user experience.


# Installation

 Steps to Download the "passthewall" Script


 Windows

 Using Git:
 Open Command Prompt.
 Navigate to the directory where you want to download the script using the cd command.
 Run the command:
 


    git clone https://github.com/Lutkinxp/passthewall.git

 Downloading as ZIP:
   Go to the repository page in your web browser.
   Click on the "Code" button and select "Download ZIP".
   Extract the ZIP file to your desired location.


Linux

 Using Git:
        Open Terminal.
        Navigate to the directory where you want to download the script using the cd command.
        Run the command:

        

    git clone https://github.com/Lutkinxp/passthewall.git

 Downloading as TAR.GZ:

   Go to the repository page in your web browser.
   Click on the "Code" button and select "Download TAR.GZ".
   Extract the TAR.GZ file using:

    

    tar -xvzf passthewall.tar.gz
Mac

   Using Git:
        Open Terminal.
        Navigate to the directory where you want to download the script using the cd command.
        Run the command:

       

    git clone https://github.com/Lutkinxp/passthewall.git

   Downloading as ZIP:
        Go to the repository page in your web browser.
        Click on the "Code" button and select "Download ZIP".
        Extract the ZIP file by double-clicking it in Finder.

# Post-Download Steps

   Ensure you have Python installed on your system.
   Navigate to the downloaded script directory in your terminal or command prompt.
   Run the script using:



    python passthewall.py
