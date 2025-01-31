
Notes on the file structure and file in Erlangen system
to ssh login into the machines:
```shell
ssh sheth@<computer>.sternwarte.uni-erlangen.de
```

password is in the mail. computer name can be octans, asterion, solarium etc.

the main data directory is /userdata/data/sheth/
where there is a test_sixte folder in which the data and simulation outputs are there.

## 1. load the modules

```shell
module load sixte/3.0.7
module load ero-pipeline
```


# Comma separated SIMPUT 
you can download the ROSAT background from sixte website and put it after the catalog that has been made in the run_sim_allsky.sl and this would include the background with the SIMPUT for the sources that we gave. The simulation can include both without simputmerge.
