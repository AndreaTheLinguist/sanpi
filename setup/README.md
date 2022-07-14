# Environment Set Up

1. Install [anaconda](https://docs.anaconda.com/anaconda/install/index.html) if not already installed.

2. From the `setup/` directory, run: 

        $ conda env create -f sanpi_env.yml

   Or from `sanpi/` directory, run: 

        $ conda env create -f setup/sanpi_env.yml

    _For development, use `dev-sanpi_env.yml` instead_

3. To check for remaining required tools, run: 

        $ bash setup/condacheck.sh