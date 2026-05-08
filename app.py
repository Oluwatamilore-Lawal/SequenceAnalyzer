from flask import Flask, render_template, request
from sequence_utils import (
    validate_sequence, detect_type, nucleotide_count,
    translate_seq, transcribe_seq, reverse_transcribe, to_protein
)
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    sequence = ''
    selected_ops = request.form.getlist('operations')

    if request.method == 'POST':
        file = request.files.get('file')
        sequence = request.form.get('sequence', '')

        if file and file.filename:
            content = file.read()
            if len(content) > 1_000_000:
                results.append({'kind': 'error', 'value': 'File exceeds 1MB limit'})
                return render_template('index.html', results=results, sequence=sequence, selected_ops=selected_ops)
            sequence = content.decode('utf-8')

        try:
            sequence = validate_sequence(sequence)
            seq_type = detect_type(sequence)

            if 'type' in selected_ops:
                results.append({'kind': 'type', 'value': seq_type})

            if 'composition' in selected_ops:
                results.append({'kind': 'composition', 'value': nucleotide_count(sequence)})

            if 'translate' in selected_ops:
                results.append({'kind': 'sequence', 'label': 'mRNA', 'value': translate_seq(sequence)})

            if 'transcribe' in selected_ops:
                results.append({'kind': 'sequence', 'label': 'Complementary DNA', 'value': transcribe_seq(sequence)})

            if 'reverse' in selected_ops:
                results.append({'kind': 'sequence', 'label': 'DNA', 'value': reverse_transcribe(sequence)})

            if 'protein' in selected_ops:
                protein, warning = to_protein(sequence)
                results.append({'kind': 'protein', 'value': protein, 'warning': warning})

        except ValueError as e:
            results.append({'kind': 'error', 'value': str(e)})

    return render_template('index.html', results=results, sequence=sequence, selected_ops=selected_ops)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
