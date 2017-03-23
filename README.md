# aerocom-data-correction-tools
Tools the [aerocom project](http://aerocom.met.no/) uses to adjust submitted model data to the aerocom standard. The standard is described along with the [data submission instructions on the aerocom wiki pages](https://wiki.met.no/aerocom/data_submission).
The tools are under development, and aim to correct errors on dimensions, NaN values, axis orientations and descriptions, naming of variables.
Some variables are reconstructed from other variables, reconstruction is documented in history attribute.

How-to-Use
Routines are written in python, read model data and rewrite them according to needs.

Further development: See issues.

Acknowledgment: The work involved was supported by the Norwegian Research Council project AeroCom P3 and the project [eSTICC]( https://esticc.net/) a Nordic Centre of Excellence (NCoE) funded by NordForsk. 
