import re
import cd_processing.textextrconst as tec

SOURCE = r'PROJECTS\Суды по поставке 20161219.txt'
NOTE_FIND_PAT = tec.note_find_pattern
ACTS_SEP_PAT = tec.acts_separator_pattern

def custom_writer(iterable_object, filename):
    from writer import writer
    writer(iterable_object, filename)

def note_deletion(path=SOURCE,
                  pattern=NOTE_FIND_PAT,
                  writing=False,
                  output_filename='cleaned_text'):
    '''Cleans courts decisions .txt file from
    database's information notes. Returns cleaned text
    or writes (by writer.py module) it into
    new output_filename.txt file.'''
    with open(path) as file:
        text = file.read()
    cl_text = re.subn(pattern, '', text, flags=re.DOTALL)
    if writing == False:
        return cl_text[0]
    else:
        custom_writer(cl_text[0], output_filename)

def acts_separator(cleaned_text,
                   pattern=ACTS_SEP_PAT,
                   writing=False,
                   output_filename='separated_acts'):
    '''Returns list of separated court descisions
    that were extracted from cleaned string of acts.
    Returns separated court acts or writes (by writer.py module)
    them into the new output_filename.txt file'''
    store = re.findall(pattern, cleaned_text, flags=re.DOTALL)
    if writing == False:
        return store
    else:
        custom_writer(store, output_filename)
