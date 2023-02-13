# coding=utf-8
from pathlib import Path
import logging


def display_message(message: str,
                    logger: logging.Logger = None,
                    level: int = 20):
    '''print or send to log if given. log level of message defaults to info (20)'''
    if logger:
        if message.startswith('#'):
            message = '\n' + message
        logger.log(level=level, msg=message)
    else:
        print(message)


def dur_round(time_dur: float):
    """take float of seconds and converts to minutes if 60+, then rounds to 1 decimal if 2+ digits

    Args:
        dur (float): seconds value

    Returns:
        str: value converted and rounded with unit label of 's','m', or 'h'
    """
    unit = "s"

    if time_dur >= 60:
        time_dur = time_dur / 60
        unit = "m"

        if time_dur >= 60:
            time_dur = time_dur / 60
            unit = "h"

    if time_dur < 10:
        dur_str = f"{round(time_dur, 2):.2f}{unit}"
    else:
        dur_str = f"{round(time_dur, 1):.1f}{unit}"

    return dur_str


def file_size_round(size: int):

    if size >= 10**8:
        unit = 'G'
        power = 9
    elif size >= 10**5:
        unit = 'M'
        power = 6
    elif size >= 10**2:
        unit = 'K'
        power = 3
    else:
        unit = ''
        power = 0

    return f'{round(size / (10**power), 1):.1f} {unit}B'


def find_files(data_dir: Path(), fname_glob: str, verbose: bool = False):
    path_iter = data_dir.rglob(fname_glob)
    if verbose:
        path_iter = tuple(path_iter)
        print_iter(
            [f'../{p.relative_to(data_dir)}' for p in path_iter], bullet='-',
            header=f'### {len(path_iter)} paths matching {fname_glob} found in {data_dir}')
    return path_iter


# > moved to `get_deps.parallel_process_deps()` directly
# // def run_pool(process_to_run, inputs, log_level: int = 30):
# //     mp.set_start_method('forkserver')
# //     # logger = mp.get_logger()
# //     logger = mp.log_to_stderr()
# //     logger.setLevel(log_level)  # 20=info, 30=warning, 10=debug
# //
# //     inputs = tuple(inputs)
# //     input_count = len(inputs)
# //     # > set pool `processes` argument to
# //     # > (a) number of _available_ cpus
# //     # > OR
# //     # > (b) number of inputs to be processed,
# //     # > whichever is less
# //     cpus = min(mp.cpu_count(), input_count, 15)
# //     print(f'\n> processing {input_count} inputs with {cpus} CPUs...')
# //     _start = datetime.now()
# //
# //     with mp.Pool(processes=cpus) as pool:
# //
# //         # NOTE: if process function takes more than 1 argument:
# //         #       use (a) snippet "expand_argument_inputs" and `imap(_unordered)`
# //         #       or  (b) `starmap` -> does not require printing step after, but slower
# //         results = tuple(pool.imap_unordered(process_to_run,
# //                                             inputs)
# //                         )
# //
# //         # zfill_len = len(str(file_count))
# //         # in_sz_w = 7
# //         # out_sz_w = 8
# //         # in_name_w = len(list(corpus_dir.glob('*conllu'))[0].stem)+1
# //         # print(('  task  |  time  \tin size\tout size\t'
# //         #         f'{"in data".ljust(in_name_w)}\t'
# //         #         ' out data\n'
# //         #         f' ------ | ------ \t'
# //         #         f'{"-"*in_sz_w}\t'
# //         #         f'{"-"*out_sz_w}\t'
# //         #         f'{"-"*in_name_w}\t'
# //         #         f'{"-"*40}'
# //         #         ).expandtabs(3))
# //
# //         #! this is required to actually get the processes to run
# //         i = 0
# //         for result in results:
# //             i += 1
# //             print(f'## Input {i}')
# //             logger.info(f'({i})')
# //             # dur, in_name, in_size, out_name, out_size = result
# //             # print((f'{str(i).zfill(zfill_len).center(8)}|{dur.rjust(7)} \t'
# //             #         f'{in_size.center(in_sz_w)}\t'
# //             #         f'{out_size.center(out_sz_w)}\t'
# //             #         f'{in_name.ljust(in_name_w)}\t'
# //             #         f'{out_name}').expandtabs(3))
# //             if not isinstance(result, (int, str, float)):
# //
# //                 try:
# //                     print_iter(iter_obj=result, bullet='-')
# //                 except:
# //                     pass
# //                 else:
# //                     continue
# //
# //             print(result)
# //             logger.info(result)
# //
# //         # total_inputs_processed = i
# //         # print(total_inputs_processed, 'inputs processed')
# //
# //         # print_iter(results)
# //
# //         # ? Is there a better way to do this? ^^ Like, some "run" or "start" or "join" method?
# //     _end = datetime.now()
# //     total_time = _end - _start
# //     print('## Parallel Processing Complete\n- Timestamp:', _end.strftime("%Y-%m-%d @ %I:%M%p"),
# //           '\n- Total time elapsed:', dur_round(total_time.total_seconds()))


def print_iter(iter_obj,
               bullet: str = '▸',
               logger: logging.Logger = None,
               level: int = 20,
               header: str = ''):

    bullet_str = f'\n{bullet} '

    iter_str = bullet_str.join(f'{i}' for i in iter_obj)

    msg_str = f'\n{header}{bullet_str}{iter_str}'
    msg_str = msg_str.replace('\n\n', '\n').strip('- ')

    display_message(msg_str, logger, level)
