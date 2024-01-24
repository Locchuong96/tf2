from google.colab import _message
from google.colab import files
import json

def run(name='notebook.ipynb'):

    # Flag if the notebook is corrupt
    META_CORRUPT = False

    # Cell output to tell the learners if the metadata is intact
    WARNING = f'**IMPORTANT: Missing grader metadata detected! It has now been added and saved to `{name}`. \nThe notebook is being downloaded. Please submit {name} to the grader.'
    SAFE = "Grader metadata detected! You can download this notebook by clicking `File > Download > Download as .ipynb` and submit it to the grader!"

    # String to search for in the cell 'tags' metadata
    TAG = "graded"


    # Strings in the cell indicating that the cell is required by the grader
    REQUIRED_IDENTIFIERS = ["Graded Cell", "# START CODE HERE", "grader-required-cell"]
    # -

    # Load the notebook JSON.
    ntbk = _message.blocking_request('get_ipynb', timeout_sec=120)['ipynb']


    for cell in ntbk['cells']:
        
        # The loop will only check code cells
        if cell['cell_type'] == 'code':
            
            required_identifier_found =  any(required_check in '.\t'.join(cell['source']) for required_check in REQUIRED_IDENTIFIERS)
            
            # Only check the metadata if the cell is required by the grader
            if required_identifier_found:
                
                cell['metadata']['tags'] = cell.get('metadata', {}).get('tags', [])

                if TAG not in cell['metadata']['tags']:

                    # Flag notebook as corrupt and back up to a different file
                    META_CORRUPT = True
                    
                    cell['metadata']['tags'].append(TAG)


    # Save the notebook in a local file if the current version is corrupt
    if META_CORRUPT:
        
        with open(name, 'w') as f:
            json.dump(ntbk, f)
        
        # download the file automatically
        files.download(name)

        print(WARNING)

    else:
        print(SAFE)
