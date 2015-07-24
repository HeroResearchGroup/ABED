
"""
General functions for generating tables for Abed results

"""

import datetime
import os

from tabulate import tabulate

from abed import settings
from abed.results.html import generate_html
from abed.results.models import AbedTable, AbedTableTypes
from abed.results.ranks import make_rank_table
from abed.utils import info, mkdir

def make_tables_scalar(abed_cache, scalar):
    # First create the normal table
    table = build_tables_scalar(abed_cache, scalar)
    table.higher_better = (True if settings.SCALARS[scalar]['best'] == max else 
            False)
    table.type = AbedTableTypes.VALUES
    table.desc = 'Scalar: %s' % scalar
    table.name = scalar
    table.target = scalar
    write_table(table, output_formats=settings.OUTPUT_FORMATS)
    # Now create the rank table from the generated table
    ranktable = make_rank_table(table)
    write_table(ranktable, output_formats=settings.OUTPUT_FORMATS)

def build_tables_scalar(abed_cache, scalarname):
    table = AbedTable()
    table.headers = sorted(abed_cache.methods)
    for i, dset in enumerate(sorted(abed_cache.datasets)):
        row = []
        for j, method in enumerate(sorted(abed_cache.methods)):
            values = abed_cache.get_scalar_values_dm(dset, method, scalarname)
            best_value = settings.SCALARS[scalarname]['best'](values)
            row.append(round(best_value, settings.RESULT_PRECISION))
        table.add_row(dset, row)
    return table

def get_table_fname(table, fmt):
    outdir = '%s%s%s' % (settings.OUTPUT_DIR, os.sep, fmt)
    mkdir(outdir)
    if table.is_metric:
        fname = '%s%sABED_%s_%s_%s.%s' % (outdir, os.sep, table.target,
                table.name, table.type, fmt)
    else:
        fname = '%s%sABED_%s_%s.%s' % (outdir, os.sep, table.target,
                table.type, fmt)
    return fname

def write_table(table, output_formats=None):
    if output_formats is None:
        output_formats = ['txt']
    for fmt in output_formats:
        if fmt == 'txt':
            write_table_txt(table)
        elif fmt == 'csv':
            write_table_csv(table)
        elif fmt == 'xls':
            write_table_xls(table)
        elif fmt == 'html':
            write_table_html(table)
        else:
            raise ValueError

def write_table_txt(table):
    fname = get_table_fname(table, 'txt')
    now = datetime.datetime.now()
    with open(fname, 'w') as fid:
        fid.write("%% Result file generated by ABED at %s\n" % 
                now.strftime('%c'))
        fid.write("%% Table for label: %s\n" % table.target)
        fid.write("% Showing: %s\n" % table.type)
        if table.is_metric:
            fid.write('%% Metric: %s\n\n' % table.name)
        txttable = [r for i, r in table]
        tabtxt = tabulate(txttable, headers=table.header)
        fid.write(tabtxt)
        fid.write('')
        sumtable = [r for i, r in table.summary_table()]
        tabtxt = tabulate(sumtable, headers=table.header)
        fid.write(tabtxt)
    info("Created output file: %s" % fname)

def write_table_xls(table):
    pass

def write_table_csv(table):
    pass

def write_table_html(table):
    fname = get_table_fname(table, 'html')
    html = generate_html(table)
    with open(fname, 'w') as fid:
        fid.write(html)
    info("Created output file: %s" % fname)
