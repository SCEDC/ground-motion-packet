## Examples

Examples **with fake data** can be found in this repository 
[here](https://github.com/SCEDC/ground-motion-packet/tree/main/gmpacket/data/examples).
These examples are selected to illustrate a number of different possible
instrument configurations and to highlight the value of sensible grouping
of traces into streams. 

[Example 1](https://raw.githubusercontent.com/SCEDC/ground-motion-packet/main/gmpacket/data/examples/example1.json)
:  This is a very simple example for station CI.CCC. It contains a single stream
   for the HN instrument with. It contains two traces: the HNE component, and ROTD50.

   This illustrates one important aspect of this data structure: ROTD50 is derived from
   two horizontal components for this instrument and the ROTD50 metrics cannot be
   derived from the metrics of the individual components. Thus, it is valuable to
   report it at the "trace" level (note that there is a trace from which ROTD50 is
   derived, which is a rotated combination of the horizontal traces).

   For the HNE trace, the metrics dictionary includes response spectra (a 2D array
   metric) and peak ground acceleration (a scalar metric).

   For the ROTD50 trace, the metrics dictionary includes significant duration (a 2D
   array metric) and bracketed duration (a 1D array metric). 

[Multichannel](https://raw.githubusercontent.com/SCEDC/ground-motion-packet/main/gmpacket/data/examples/multichannel_example.json)
:  This example is also for a single station (BK.OVRO) and contains
   a single stream for the HN instrument. It contains three traces: HNN, HNE, and HNZ.
   Each traces includes PGA and response spectra metrics. 

[Borehole Example](https://raw.githubusercontent.com/SCEDC/ground-motion-packet/main/gmpacket/data/examples/borehole_example.json)
:  This is for the downhole geotechnical array at Treasure Island. There are three
   traces at each depth, and each depth is grouped as a stream.

[Multisamplerate](https://raw.githubusercontent.com/SCEDC/ground-motion-packet/main/gmpacket/data/examples/sps-100-200-example.json)
:  This is example is for a single free field station (CI.CCC). This station has a 3
   component strong motion sensor that is being recorded at 100 sps and 200 sps. Each
   sample rate is grouped as a stream and as 3 traces for each sensor component as well
   as ROTD50 trace in the 100 sps stream.
