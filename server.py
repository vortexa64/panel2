from flask import Flask, request, send_from_directory, redirect, render_template_string
import os

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    files = os.listdir(UPLOAD_FOLDER)
    html = """
    <html><head><title>VPS KW Arya 😈</title></head><body style='background:#111;color:#eee;font-family:sans-serif;'>
    <h2>🗂️ File Manager - VPS KW Arya</h2>
    <form method='POST' enctype='multipart/form-data' action='/upload'>
        <input type='file' name='file'>
        <button type='submit'>Upload File</button>
    </form><br>
    <ul>
    {% for file in files %}
        <li>
            {{file}} |
            <a href='/file/{{file}}'>Download</a> |
            <a href='/edit/{{file}}'>Edit</a> |
            <a href='/delete/{{file}}'>Delete</a> |
            <a href='/run/{{file}}'>Run</a>
        </li>
    {% endfor %}
    </ul>
    <br><h4>💥 Python Runner 💥</h4>
    <form method='POST' action='/run_code'>
        <textarea name='code' style='width:100%;height:200px;background:#222;color:#eee;'></textarea><br>
        <button type='submit'>Run Python Code</button>
    </form>
    {% if output %}
    <pre style='background:#222;padding:10px;'>{{output}}</pre>
    {% endif %}
    </body></html>
    """
    return render_template_string(html, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect('/')

@app.route('/file/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if request.method == 'POST':
        with open(filepath, 'w') as f:
            f.write(request.form['content'])
        return redirect('/')
    else:
        with open(filepath, 'r') as f:
            content = f.read()
        return f"""
        <form method='POST'>
            <textarea name='content' style='width:100%;height:500px;'>{content}</textarea><br>
            <button type='submit'>Save</button>
        </form>
        """

@app.route('/delete/<filename>')
def delete_file(filename):
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    return redirect('/')

@app.route('/run/<filename>')
def run_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if filename.endswith('.py'):
        output = os.popen(f'python3 {filepath}').read()
        return f"<pre>{output}</pre><br><a href='/'>Back</a>"
    return "Only .py files can be executed."

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.form['code']
    with open('temp_exec.py', 'w') as f:
        f.write(code)
    output = os.popen('python3 temp_exec.py').read()
    return home().replace("{{output}}", output)

app.run(host='0.0.0.0', port=7860)