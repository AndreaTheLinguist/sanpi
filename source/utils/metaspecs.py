# coding=utf-8
import contextlib
import errno
import itertools as it
import os
import re
from collections import namedtuple
from math import log, log1p, log2, sqrt
from pathlib import Path
from typing import NamedTuple

import matplotlib as mpl
import numpy as np
import pandas as pd

try:
    from source.utils import PKL_SUFF, SANPI_HOME, UCS_DIR
    from source.utils import find_glob_in_dir as seek_in_dir
    from source.utils import gen_random_array 
except ModuleNotFoundError:
    try:
        from utils import PKL_SUFF, SANPI_HOME, UCS_DIR
        from utils import find_glob_in_dir as seek_in_dir
        from utils import gen_random_array
    except ModuleNotFoundError:
        from dataframes import corners, print_md_table
        from general import PKL_SUFF, SANPI_HOME, UCS_DIR
        from general import find_glob_in_dir as seek_in_dir
        from general import gen_random_array
    else:
        from utils.dataframes import corners, print_md_table

else:
    from source.utils.dataframes import corners, print_md_table
# from source.utils.general import find_glob_in_dir as seek_in_dir, gen_random_array
# from source.utils.general import print_iter, snake_to_camel


class Bigram(NamedTuple):

    adv: str = ''
    adj: str = ''

    @classmethod
    def text(cls, bigram_str=str):
        return cls(*re.match(r'([a-z-]+)[^a-z-]+([a-z-]+)', bigram_str.lower().strip()).groups())

    def __repr__(self):
        return f'{self.adv}_{self.adj}'


class LexUnit(NamedTuple):

    name: str = 'adv_form_lower'
    abbr: str = 'adv'
    position: int = 1

    def __repr__(self):
        return f'l{self.position}={self.abbr}({self.name})'


class DataSpecs(NamedTuple):

    """A class representing data specifications.

    This class defines the specifications for data processing,
    including the pattern category, ucs freq floor, margin freq floor, and lexical units.

    Attributes:
        - pattern_category (str): (default='RBXadj')
            directory name of the original `.pat` files used to gather the data.
            Suggested alternatives:
                {'RBdirect', 'NEGmirror', 'POSmirror', 'ANYmirror', etc.}
        - adX_margin_floor (int; default=868):
            minimum marginal frequency required for any given `adv_form_lower` or `adj_form_lower` value to be included in initial frequency filtering. E.g. if the floor is 500 and an adverb was only observed in 300 different bigram tokens, it was dropped from the initial frequency table.
        - ucs_show_floor (int): (for associations; default=20)
            The minimum joint frequency required to be included in association table (but still accounted for in metric calculations).
        - polar (bool): (for associations; default=False)
            if the comparison considered is a representation of polarity environments
        - env_eval (bool): (for associations; default=False)
            if the comparison considered is between a single lexical unit and different datasets (technically the superset of `polar==True` cases)
        - extra (bool): (for associations; default=True)
            if the data includes additional metrics (e.g. `conservative_log_ratio`) and processing

    """
    # TODO: add attribute & processing for `complement` (for loading frequency tables)
    pattern_category: str = 'RBXadj'
    ucs_show_floor: int = 20
    adX_margin_floor: int = 868
    polar: bool = False
    env_eval: bool = False
    lex_targets: list or LexUnit = None
    extra: bool = True


class AssocTable(DataSpecs):

    """A class representing an association table.

        This class inherits from the DataSpecs class and provides properties to calculate the interaction, file glob, directory path, and pickle path for the association table.

        Attributes:
            None

        Properties:
            - interaction: The interaction property.
            - file_glob: The file glob property.
            - dir_path: The directory path property.
            - pkl_path: The pickle path property.
            - lexical (list or LexUnit): (for associations)
                solo `LexUnit` (for `polar` or `env_val` cases) or list of (2) LexUnits to run comparison/association on:

                LexUnit(name = column name from original data (e.g. "adv_form_lower"),
                        abbr = abbreviated name (e.g. "adv"),
                        position = int(1:2) indicating first or second linear position;
                            corresponds to `l1` or `l2` in association tables)
                Example:
                    [LexUnit('neg_form_lower', 'neg', 1),
                    LexUnit('bigram_lower', 'bigram', 2)]
                Defaults to:
                - if `env_eval or polar`:
                    [LexUnit('bigram_lower', 'bigram', 2)]
                - else:
                    [LexUnit('adv_lower', 'adv', 1),
                    LexUnit('adj_lower', 'adj', 2)]
    """

    __slots__ = ()

    @property
    def lexical(self):
        lex_list = []
        lex_obj = self.lex_targets

        if lex_obj is not None:

            if isinstance(lex_obj, list):
                lex_list.extend(lex_obj)
            elif isinstance(lex_obj, (LexUnit, str)):
                if isinstance(lex_obj, str):
                    lex_obj = lex_obj.lower()
                    if lex_obj in ('adj', 'adv', 'neg', 'nr', 'relay', 'mir'):
                        lex_obj = LexUnit(f'{lex_obj}_form_lower', lex_obj, 2)
                    else:
                        lex_obj = LexUnit(
                            lex_obj, snake_to_camel(lex_obj)[:6], 2)
                lex_list.append(lex_obj)

        elif self.env_eval or self.polar:
            lex_list.append(LexUnit('bigram_lower', 'bigram', 2))
            # other suggestions:
            # LexUnit('adv_form_lower', 'adv', 2)
            # LexUnit('adj_form_lower', 'adj', 2)

        else:
            lex_list.extend([LexUnit(f'{a}_form_lower', a, i)
                             for i, a in
                             enumerate(('adv', 'adj'), start=1)
                             ])

        return lex_list

    @property
    def lex_label(self):
        return '_'.join([x.abbr for x in self.lexical])

    @property
    def interaction(self):
        """The interaction property."""
        if self.polar:
            return 'polar'
        elif not self.env_eval:
            return '_'.join(x.abbr for x in self.lexical)
        elif 'mir' in self.pattern_category:
            return 'eval_mirror'
        else:
            return 'eval_env'

    @property
    def file_glob(self, pkl_only: bool = True):
        return (f'*{self.lex_label}*35f'
                f'*{self.adX_margin_floor}'
                f'*min{self.ucs_show_floor}x'
                f'*{PKL_SUFF if pkl_only else ""}')

    @property
    def dir_path(self):

        am_dir_path = UCS_DIR.joinpath(
            f'dataframes/{self.interaction}/{self.pattern_category}')
        # if len(self.lexical) == 1:
        if self.polar or self.env_eval:
            am_dir_path = am_dir_path / self.lex_label
        if self.extra:
            am_dir_path = am_dir_path / 'extra'
        return am_dir_path

    @property
    def pkl_path(self):
        pkl_path = Path(seek_in_dir(
            self.dir_path, self.file_glob, err_response='raise'))

        return pkl_path if pkl_path.exists() else None
        # else:
        #     raise FileNotFoundError(
        #         errno.ENOENT, os.strerror(errno.ENOENT),
        #         str(pkl_path))

    @property
    def other_method_path(self):
        other_dict = {'RBdirect': 'NEGmirror',
                      'NEGmirror': 'RBdirect'}
        specs_dir = self.dir_path
        other_dir = None
        for current, other in other_dict.items():
            if current in specs_dir.parts:
                other_dir = Path(str(specs_dir).replace(current, other))
        if other_dir:
            return seek_in_dir(other_dir, self.file_glob, err_response='return')

    @property
    def adX(self, df_obj: pd.DataFrame = None):
        _df = (pd.read_pickle(self.pkl_path) if df_obj is None
               else df_obj.copy())

        l2_abbr = self.lex_label  # e.g. bigram, adv, adj
        adx_set = {'adj', 'adv'}
        if l2_abbr.lower() in adx_set:
            raise UserWarning(errno.ENOENT, os.strerror(errno.ENOENT),
                              f'associations are based on environment and {l2_abbr}: '
                              f'`{l2_abbr}(_total)` columns are redundant and '
                              f"`{list(adx_set-{l2_abbr})[0]}(_total)` are irrelevant")
        adX = (_df.reset_index(drop=True)
               .drop_duplicates('l2')
               .set_index('l2')
               .filter(regex=r'^ad|f2')
               .rename(columns={'f2': f'{l2_abbr}_total'}))
        adX.index.name = l2_abbr
        print_md_table(adX.sample(15),
                       title=f'15 random {l2_abbr} values & their component margins')

        return adX

    def __repr__(self):
        info_list = [
            'Association Metric Table Specs:',
            f' pattern_category: "{self.pattern_category}"',
            f'   ucs_show_floor: {self.ucs_show_floor}',
            f' adX_margin_floor: {self.adX_margin_floor}',
            f'            polar: {self.polar}',
            f'         env_eval: {self.env_eval}',
            f'          lexical: {self.lexical}',
            f'      interaction: {self.interaction}',
            f'        lex_label: {self.lex_label}',
            f'            extra: {self.extra}',
            f'         dir_path: {self.dir_path}/',
            f'        file_glob: {self.file_glob}',
            f'         pkl_path: ../../{self.pkl_path.relative_to(UCS_DIR)}',
            f'other_method_path: ../../{self.other_method_path.relative_to(UCS_DIR)}'
        ]

        if self.lex_label == 'bigram':
            # info_list.append('              adX: [dataframe of independent adverb & adjective \n'
            #                  '                       string values and marginal frequencies    ]')
            info_list.append('              adX: [dataframe of independent adverb & adjective'
                             ' string values and marginal frequencies]')
        return '\n '.join(info_list)+'\n'

    def collect_l1_totals(self,
                          df_obj: pd.DataFrame = None,
                          other: bool = False,
                          verbose: bool = True):
        if df_obj is None:
            read_path = self.other_method_path if other else self.pkl_path
            # print('loading', read_path.relative_to(UCS_DIR))
            am_df = pd.read_pickle(read_path)
        else:
            am_df = df_obj

        N = am_df.N.unique()[0]
        am_df = am_df.reset_index()[['l1', 'f1']].drop_duplicates()
        f1_name = f'total_{self.lex_label}_tokens'
        pat_cat = read_path.parts[-4]  # //self.pattern_category

        env_totals = am_df[['l1', 'f1']].rename(
            columns={'f1': f1_name, 'l1': 'polarity'}
        ).set_index('polarity')
        env_totals.at['_&_'.join(ix[:3] for ix in env_totals.index),
                      f1_name] = N
        env_totals[f1_name] = pd.to_numeric(
            env_totals[f1_name], downcast='unsigned')
        env_totals['relative_%'] = (env_totals[f1_name]
                                    .apply(lambda t:
                                           round((t / N * 100), 2))
                                    .astype('float'))
        print_md_table(
            env_totals, n_dec=1,
            title=f'Environment Totals for Detected Pattern Category = `{pat_cat}`\n')

        # HACK to remove `.0` from raw count column; theoretically shouldn't have that added in the first place but dtypes are a mess to deal with
        print(
            re.sub(r'\.0(.+\s+\d+)', r'  \1',
                   print_md_table(
                       env_totals, n_dec=1, suppress=True,
                       title=f'Environment Totals for Detected Pattern Category = `{pat_cat}`\n')
                   )
        )

        return env_totals.assign(pol_approx_method="mirror" if pat_cat.endswith("mirror") else "set_diff")

    def show(self, with_env_totals: bool = False):
        print(self)
        if with_env_totals:
            for truth_val in (False, True):
                self.collect_l1_totals(other=truth_val)
