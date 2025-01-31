# questions
1. what to do in the attitude entry column for pointed observations
	1. dont do that. use GTI or attitude files. that also better represents the survey obervations.
2. you copied some files from your computer (or linked here in the script) which contain the eROSITA attitudes.
3. We should make our own versions of `run_sim_allsky.sl` for pointed versions?
4. when should we run the isis command? before every simulation? or before 
# 1. Prepare the SIMPUT
create a SIMPUT that contains the source catalog and their spectra in the SIMPUT standard structure.

# 2. Login to the erlangen network

```bash
ssh sheth@octans.sternwarte.uni-erlangen.de
```
password is in the mail
# 3. Load the modules
the module that we need is the latest sixte installation:

```shell
module load sixte/3.0.7
```

# 4. Copy and Modify the files to configure the simulation

```shell
nano run_sim_allsky.sl
nano subs_erosim.sl
```
these are files written in slang, a programming language. 
# 5. Run isis to configure the directories and job submission

```shell
isis ./run_sim_allsky.sl
```

this sets up the directory structure with folders like `evt` ,  `log`, `sh` which will be populated during the simulation.

# 6. Then run the simulation
```shell
sbatch run_sim_allsky-sl
```

# 7.  Check on the processes
```shell
squeue -u sheth
```

# 8. Load modules for analysis

```shell
module load ero-pipeline
module load esass/211214-p4
```

# 9. Merge into skytiles

```shell
ero-simulation --telgti--simdir evt --skytile-dir skytile_test --account erosita --partition erosita
```

this creates a DATool like skytile product in which we can access the objects as we need.

