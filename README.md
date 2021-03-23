This is a simple file compressor that compresses text files.
In order to compress you must run the following console command:
python3 filework.py -e/-d filename

-e: Encode the file, this compresses the file and outputs a .dec file with the same name as the original. Do not delete or rename either file as both are required for uncompression.
-d: Decode the file, reverses the compression of the file based on its .dec version.

Note: The compression is better the larger the input file, with very small text files (i.e a couple words or one sentence) the compression may even bloat the output as compared to the input.
