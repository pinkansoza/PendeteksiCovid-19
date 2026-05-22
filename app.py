import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import covid19_ai_diagnoser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    mode = request.form.get('mode', 'covid19')
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            result_data = covid19_ai_diagnoser.doOnlineInference_covid19Pneumonia(filepath)
                
            # Clean up the file
            try:
                os.remove(filepath)
            except:
                pass
                
            if isinstance(result_data, str) and "Error" in result_data:
                return jsonify({'error': result_data}), 500
                
            status = result_data['status']
            
            # Determine status type for UI coloring
            status_type = "safe" # Default
            if "Covid19 detected" in status or "Pneumonia detected" in status:
                status_type = "danger"
            elif "Normal" in status:
                status_type = "safe"
                
            return jsonify({
                'status': status,
                'status_type': status_type,
                'confidence': result_data['percentage'],
                'raw_score': result_data['raw_score']
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Membuka server web di http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
