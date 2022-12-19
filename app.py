# import from flask module Flask function needed to create the REST server
from flask import Flask
# import webbrowser and os modules to open the description of the Web Server as html page
import webbrowser
import os

# the Server opens the fasta file containing the sequence of SARS-COV-2 genome - that is in the same directory in which
# the code of this REST web service is - skips the first header line and stores the rest of the sequence as a continuous
# string
file = open('sequence.fasta', 'r')
file.readline()
SARS_COV_2_genome = ''.join([line.rstrip('\n') for line in file.readlines()]).upper()

# definition of a function to build the index of the pattern string inserted by the user
def build_index(pattern):
    # initialize the index with 0
    index = [0]
    # initialize i to 0 and j to 1 to scan all the pattern sequence to identify the prefixes that are equal to suffixes
    i = 0
    j = 1

    while j < len(pattern):
        # if the character in position i and the character in position j are different:
        if pattern[i] != pattern[j]:
            if i == 0:
                # add 0 to the index since the character j is different from character i
                index.append(0)
                # move to the next j-th position of the pattern to check if it is equal to pattern[0]
                j += 1
            else:
                # add 0 to the index since the character j is different from character i
                index.append(0)
                # set i to the proper value of the index
                i = index[i-1]

        # if the character in position i and the character in position j are equal slide both i and j of one position
        else:
            i += 1
            index.append(i)
            j += 1

    return index

# definition of a function that returns the number of occurrences of a pattern in a sequence given the index of the pattern
def sequence_in_genome(sequence, pattern, index):
    i = 0   # to iterate over the pattern
    j = 0   # to iterate over the sequence
    tot = 0 # to store the number of occurrences of the pattern in the sequence

    while j < len(sequence):
        if pattern[i] == sequence[j]:
            # in case the whole pattern has been found in the sequence add one occurrence to the counter
            if i == len(pattern) - 1:
                tot += 1
                i = index[i]
                j += 1
            # otherwise slide both i and j of one position
            else:
                i += 1
                j += 1

        else:
            # if the character in position 0 of the pattern is different from the one in position j of the sequence
            # slide of one position only on the sequence
            if i == 0:
                j += 1
            else:
                # set i to the proper value of the index
                i = index[i-1]

    return tot

# definition of a function that checks whether the pattern inserted by the user only contains nucleotide characters
def control_characters(pattern):
    for char in pattern:
        if not char.upper() in ['A','C','T','G']:
            return False
    return True


# declare Flask application
app = Flask(__name__)

# routing to the basic URL a function that returns what the user can request
@app.route("/")
def presentation():
    result = "\n".join(["To visualize the description of the Web Server: curl -i http://127.0.0.1:port_number/description",
                      "To visualize the entire SARS-COV-2 genome: curl -i http://localhost:port_number/genome",
                      "To obtain the number of occurrences of a short input sequence in the SARS-COV-2 genome: curl -i http://localhost:port_number/<sequence>\n"])
    return result

# routing to a new URL a function that returns the description of the Web Server on a html page
@app.route("/description", methods=['GET'])
def printDescription():
    filename = 'file:///' + os.getcwd() + '/' + 'README.html'
    webbrowser.open_new_tab(filename)

# routing to a new URL a function that prints the SARS-COV-2 genome stored in the Web Server
@app.route('/genome', methods=['GET'])
def printGenome():
    result = f"SARS-COV-2 genome: {SARS_COV_2_genome}\n"
    return result

# routing to a new URL a function that returns the number of occurrences of a pattern given in input by the user
# into the SARS-COV-2 genome
@app.route('/<pattern>', methods=['GET'])
def Knuth_Morris_Pratt(pattern):
    # check the content of the pattern
    if control_characters(pattern): # the content of the pattern is right
        index = build_index(pattern.upper()) # build the index of the pattern
        number_occurrences = sequence_in_genome(SARS_COV_2_genome, pattern.upper(), index) # compute the number of occurrences
        # of the pattern in the SARS-COV-2 genome
        if number_occurrences == 0:
            result = f"There are no occurrences of the input pattern '{pattern}' in the genome of SARS-COV-2\n"
            return result
        else:
            result = f"The number of occurrences of the input pattern '{pattern}' in the genome of SARS-COV-2 is: {number_occurrences}\n"
            return result

    else: # the content of the pattern is wrong
        result = "Error: the pattern must contain only nucleotides! Please try again\n"
        return result

# Flask application is started
if __name__ == "__main__":
    app.run()
