# gyroscope-data-export-to-gpx

Utility for converting [Gyroscope](https://gyrosco.pe) places and travels data
exports to GPX.

## Installation

You can install the utility using pipx:

```commandline
foo@bar:~$ pipx install git+https://github.com/myles/gyroscope-to-gpx.git
```

## Usage

First you will need to download your Places and Travels data from Gyroscope. You
can do this by going to the [Gyroscope Data Export](https://gyrosco.pe/export)
page and selecting the "Places" and "Travels" options. If you have a lot of data
this may take a while.

Once you have downloaded the data, you can run the script like so:

```commandline
foo@bar:~$ gyroscope-to-gpx \
  --visits /path/to/gyroscope-Myles-gvisits-export.csv \
  --travels /path/to/gyroscope-Myles-gtravels-export.csv \
  --output /path/to/output.gpx
```
