# Compressify

Compressify is a lightweight Flask-based web application designed to demonstrate the power and mechanics of Huffman Coding. It allows users to upload text-based files and visualize the compression process through real-time statistics and downloadable results.

**Features:**

_Broad Format Support:_ Process .txt, .csv, .log, .md, .json, and .xml files.

**Real-time Analytics:**
View original vs. compressed file sizes, compression ratio, and execution time.
Error Handling: Robust processing for edge cases, including empty files.
Seamless Downloads: Export your compressed data as a .bin file instantly.
Clean UI: A simple, intuitive interface built with Flask and HTML5.

**How It Works:**

The application utilizes the Huffman Coding Algorithm, a lossless data compression technique. The workflow follows these steps:
Frequency Analysis: The app scans the uploaded file to count the occurrences of each character.
Tree Construction: A binary tree is built based on frequency, where the most frequent characters are placed closer to the root.
Bit Mapping: Unique binary codes are assigned to each character; frequent characters get shorter codes, while rare ones get longer ones.
Binary Encoding: The text is converted into a bitstream and saved as a compact .bin file.

Note on Compression Ratios: Huffman coding thrives on patterns. Files with high redundancy (like logs or repetitive text) will see significant savings. Conversely, very small files or purely random data may increase in size due to the overhead of storing the Huffman code map within the file header.

**Installation & Setup:**

Clone the repository:
git clone https://github.com/yourusername/Compressify.git
cd Compressify

Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install Flask

Run the application:
python app.py
