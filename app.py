from flask import Flask, render_template, request, send_from_directory
import os, time
from huffman import HuffmanCompressor


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


allowed_extensions = {'txt', 'csv', 'log', 'md', 'json', 'xml'}
def allowed_file(filename):
    # Checks if there is a dot, and if the part after the last dot is in ALLOWED_EXTENSIONS
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
  
# Landing Page
@app.route('/')
def home():
    return render_template('landing.html')


# Handle File Upload + Show Loading Screen
@app.route('/submit', methods=['POST'])
def submit():
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return render_template('landing.html', error="Please select a file before uploading.")

    
    if not allowed_file(uploaded_file.filename):
       return render_template('landing.html', error="File type not allowed. Allowed: .txt, .csv, .log, .md, .json, .xml")
    # Save uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(input_path)

    # Create output filename
    output_filename = uploaded_file.filename + '.bin'
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    start = time.time()
    # Read file
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Compress using your class
    hc = HuffmanCompressor()
    compressed_data = hc.compress(text)

    decompressed = hc.decompress(compressed_data, hc.codes)
    print("Decompression successful:", decompressed )
    # Save binary output
    with open(output_path, "wb") as f:
        f.write(compressed_data)

    end = time.time()

    # Stats
    duration = round(end - start, 3)
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)

    if original_size == 0:
        ratio = 0  
    else:
        ratio = round((1 - compressed_size / original_size) * 100, 2)


    # Store results temporarily in global variables 
    global stats
    stats = {
        "original_size": original_size,
        "compressed_size": compressed_size,
        "duration": duration,
        "ratio": ratio,
        "output_filename": output_filename
    }
    return render_template('loading.html', duration = duration)


# Show Result Page
@app.route('/result')
def result():
    if 'stats' not in globals():
        return render_template('landing.html')  # safety 

    return render_template(
        'result.html',
        original_size=stats["original_size"],
        compressed_size=stats["compressed_size"],
        duration=stats["duration"],
        ratio=stats["ratio"]
    )

@app.route('/download')
def download():
    return send_from_directory(OUTPUT_FOLDER, stats['output_filename'], as_attachment = True)


if __name__ == '__main__':
    app.run(debug=True)
