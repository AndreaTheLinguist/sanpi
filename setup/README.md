# Environment Set Up

1. Check whether `anaconda` is installed:

   ```shell
   conda -V
   ```

   (should indicate a version if `conda` executable is in your `PATH`)
   If not:

   1. Install [anaconda](https://docs.anaconda.com/anaconda/install/index.html) if not already installed.
   2. Or, on the `g2` server cluster, run:

      ```shell
      /share/apps/anaconda3/[VERSION]/bin/conda init
      ```

      where `VERSION` is one of the following directories:

      ```shell
      (base) arh234@brandal:/$ tree -L 1 share/apps/anaconda3/
      share/apps/anaconda3/
      ├── 2020.11
      ├── 2021.05
      ├── 2021.05-with-pytorch
      ├── 2021.11
      └── 2022.10
      ```

      - > 📌 Note: If `pytorch` will be required, `2021.05-with-pytorch` may be mandated
        > due to a bug in later versions for certain processes.

      - To _change_ your `conda` version/executable path, run the same command with your newly selected path.
        The output should resemble:

        ```shell
        (base) arh234@brandal:/$ /share/apps/anaconda3/2022.10/bin/conda init
        no change     /share/apps/anaconda3/2022.10/condabin/conda
        no change     /share/apps/anaconda3/2022.10/bin/conda
        no change     /share/apps/anaconda3/2022.10/bin/conda-env
        no change     /share/apps/anaconda3/2022.10/bin/activate
        no change     /share/apps/anaconda3/2022.10/bin/deactivate
        no change     /share/apps/anaconda3/2022.10/etc/profile.d/conda.sh
        no change     /share/apps/anaconda3/2022.10/etc/fish/conf.d/conda.fish
        no change     /share/apps/anaconda3/2022.10/shell/condabin/Conda.psm1
        no change     /share/apps/anaconda3/2022.10/shell/condabin/conda-hook.ps1
        no change     /share/apps/anaconda3/2022.10/lib/python3.9/site-packages/xontrib/conda.xsh
        no change     /share/apps/anaconda3/2022.10/etc/profile.d/conda.csh
        modified      /home/arh234/.bashrc

        ==> For changes to take effect, close and re-open your current shell. <==
        ```

2. From the `setup/` directory, run:

   ```shell
   conda env create -f sanpi_env.yml
   ```

   Or from `sanpi/` directory, run:

   ```shell
   conda env create -f setup/sanpi_env.yml
   ```

   _For development, use `dev-sanpi_env.yml` instead_

3. To check for remaining required tools, run:

   ```shell
   bash setup/condacheck.sh
   ```
