#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse
import json

import damo_stat

import _damo_fmt_str
import _damon

def update_pr_kdamonds_summary(json_format):
    kdamonds = _damon.current_kdamonds()
    summary = [k.summary_str() for k in kdamonds]
    if json_format:
        print(json.dumps(summary, indent=4))
        return
    print('\n'.join(summary))

def update_pr_kdamonds(json_format):
    if _damon.any_kdamond_running():
        for name in _damon.current_kdamond_names():
            err = _damon.update_schemes_stats(name)
            if err != None:
                print('update schemes stat fail:', err)
                exit(1)
            if _damon.feature_supported('schemes_tried_regions'):
                err = _damon.update_schemes_tried_regions(name)
                if err != None:
                    print('update schemes tried regions fail: %s', err)
                    exit(1)
    kdamonds = _damon.current_kdamonds()
    if json_format:
        print(json.dumps([k.to_kvpairs() for k in kdamonds], indent=4))
    else:
        print('kdamonds')
        print(_damo_fmt_str.indent_lines(
            '\n\n'.join(['%s' % k for k in kdamonds]), 4))

def set_argparser(parser):
    damo_stat.set_common_argparser(parser)
    parser.add_argument('--detail', action='store_true',
            help='print detailed stat of kdamonds')
    parser.add_argument('--json', action='store_true',
            help='print kdamond in json format')

def __main(args):
    if not args.detail:
        update_pr_kdamonds_summary(args.json)
    else:
        update_pr_kdamonds(args.json)

def main(args=None):
    if not args:
        parser = argparse.ArgumentParser()
        set_argparser(parser)
        args = parser.parse_args()

    # Require root permission
    _damon.ensure_root_permission()
    _damon.ensure_initialized(args)

    damo_stat.run_count_delay(__main, args)

if __name__ == '__main__':
    main()