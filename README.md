# sitent-connector

This tool annotates results stemming from [TimeAlign](https://github.com/UUDigitalHumanitieslab/timealign) with annotations from *the Situation entity type labeling system* [sitent](https://github.com/annefried/sitent) by Annemarie Friedrich.

## Running the script

You can run the script `process.py` after installing sitent and modyfying the paths in `sitent.py` as follows:

    python process.py example/en10.csv example/en10-out.csv

The output file `en10-out.csv` will then contain annotations for situation entity type, genericity, habituality, and aspectual class.
 