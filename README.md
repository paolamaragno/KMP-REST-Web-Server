**KMP REST Web Server**

This web application solves the exact pattern matching problem that consists in finding the number of occurrences of a pattern in a text that is much bigger that the pattern itself.

In particular the Server implements the **Knuth Morris Pratt algorithm** to find the number of occurrences of a pattern specified by the user inside the genome of SARS-COV-2. 

Knuth Morris Pratt algorithm first builds an **index on the pattern and then uses it to scan the genomic sequence**, applying simple rules to the index to decide how to shift the pattern.

---------
KMP Server stores internally the fasta file of SARS-COV-2 genome sequence.

In order to start the Web Server write in the command line - in the source folder containing the script of the server:

```
flask run   
# to run the server in port 5000
flask run --port=port_number
# to run the server in a port chosen by the user
```

In another shell of the terminal the user can write the request:

* To obtain the list of functions that the application can perform
```
curl -i http://localhost:5000/
```

* To open the description file of the Web Server
```
curl -i http://localhost:5000/description
```

* To look at the sequence of SARS-COV-2 genome
```
curl -i http://localhost:5000/genome
```

* To find how many occurrences of a given pattern are present in SARS-COV-2 genome
```
curl -i http://localhost:5000/AAAAT
curl -i http://localhost:5000/ctaag
```

Attention: in all these requests after "localhost" the user must specify the port in which he/she decided to run the server

