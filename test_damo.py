#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import json
import unittest

import _damon
import _damon_dbgfs
import _damon_sysfs

import _damo_schemes_input

class TestDamos(unittest.TestCase):
    def test_damo_schemes_to_damos(self):
        inputs = [
                # no comment
                '''
                [
                    {
                        "name": "0",
                        "action": "stat",
                        "access_pattern": {
                            "min_sz_bytes": 0,
                            "max_sz_bytes": 0,
                            "min_nr_accesses": 0,
                            "max_nr_accesses": 0,
                            "nr_accesses_unit": "sample_intervals",
                            "min_age": 0,
                            "max_age": 0,
                            "age_unit": "aggr_intervals"
                        },
                        "quotas": {
                            "time_ms": 0,
                            "sz_bytes": 0,
                            "reset_interval_ms": 0,
                            "weight_sz_permil": 0,
                            "weight_nr_accesses_permil": 0,
                            "weight_age_permil": 0
                        },
                        "watermarks": {
                            "metric": "none",
                            "interval_us": 0,
                            "high_permil": 0,
                            "mid_permil": 0,
                            "low_permil": 0
                        }
                    }
                ]
                ''',
                # with comments
                '''
                [
                    {
                        # some comment
                        "name": "0",
                        "action": "stat",
                        "access_pattern": {
                            "min_sz_bytes": 0,
                            "max_sz_bytes": 0,
                            "min_nr_accesses": 0,
                            "max_nr_accesses": 0,
                            "nr_accesses_unit": "sample_intervals",
                            "min_age": 0,
                            "max_age": 0,
                            "age_unit": "aggr_intervals"
                        },
                        "quotas": {
                            "time_ms": 0,
                            "sz_bytes": 0,
                            "reset_interval_ms": 0,
                            "weight_sz_permil": 0,
                            "weight_nr_accesses_permil": 0,
                            "weight_age_permil": 0
                        },
                        "watermarks": {
                            "metric": "none",
                            "interval_us": 0,
                            "high_permil": 0,
                            "mid_permil": 0,
                            "low_permil": 0
                        }
                    }
                ]
                ''',
                # human redable
                '''
                [
                    {
                        # some comment
                        "name": "0",
                        "action": "stat",
                        "access_pattern": {
                            "min_sz_bytes": "min",
                            "max_sz_bytes": "min",
                            "min_nr_accesses": 0,
                            "max_nr_accesses": 0,
                            "nr_accesses_unit": "sample_intervals",
                            "min_age": 0,
                            "max_age": 0,
                            "age_unit": "aggr_intervals"
                        },
                        "quotas": {
                            "time_ms": "0s",
                            "sz_bytes": "0B",
                            "reset_interval_ms": "0us",
                            "weight_sz_permil": 0,
                            "weight_nr_accesses_permil": 0,
                            "weight_age_permil": 0
                        },
                        "watermarks": {
                            "metric": "none",
                            "interval_us": "0us",
                            "high_permil": 0,
                            "mid_permil": 0,
                            "low_permil": 0
                        }
                    }
                ]
                ''',
        ]
        for txt in inputs:
            damos_list = _damo_schemes_input.damo_schemes_to_damos(txt)
            expected = _damon.Damos('0',
                        _damon.DamosAccessPattern(0, 0, 0, 0,
                            'sample_intervals', 0, 0, 'aggr_intervals'),
                        'stat',
                        _damon.DamosQuotas(0, 0, 0, 0, 0, 0),
                        _damon.DamosWatermarks('none', 0, 0, 0, 0), None, None)
            self.assertEqual(damos_list[0], expected)

if __name__ == '__main__':
    unittest.main()
