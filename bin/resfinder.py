#!/usr/bin/env python
from GeneSeekr import ARMI_Lt
__author__ = 'mike knowles'


def helper(genes, targets, out, cuttoff, aro, threads):
    from glob import glob
    from GeneSeekr.ARMICARD import decipher
    import os
    import json
    import pickle
    import time
    assert os.path.isdir(out), u'Output location is not a valid directory {0!r:s}'.format(out)
    assert os.path.isfile(genes), u'ARMI-genes.fa not valid {0!r:s}'.format(genes)
    assert os.path.isfile(aro), u'Antibiotic JSON not valid {0!r:s}'.format(aro)
    assert isinstance(threads, int)
    ispath = (lambda x: glob(x + '/*.f*[sa]') if os.path.isdir(x) else [x])
    genes = ispath(genes)
    targets = ispath(targets)
    result = ARMI_Lt.ARMISeekr(genes, targets, threads)
    result.mpblast(cuttoff)
    json.dump(result.plus, open("%s/resfinder_results_%s.json" % (out, time.strftime("%Y.%m.%d.%H.%M.%S")), 'w'),
              sort_keys=True, indent=4, separators=(',', ': '))
    decipher(result.plus, pickle.load(open(aro)), out)


if __name__ == '__main__':
    from argparse import ArgumentParser
    from GeneSeekr.MLSTSeekr import parent
    from pkg_resources import resource_filename
    parser = ArgumentParser(description='Antibiotic Resistance Marker Identifier:\n'
                                        'Use to find markers for any bacterial genome',
                            parents=[parent])
    parser.add_argument('-a', '--anti', type=str
                        , default=resource_filename(ARMI_Lt.__name__, 'data/aro.dat')
                        , help='JSON file location')
    parser.set_defaults(cutoff=85)
    args = vars(parser.parse_args())

    helper(args['marker'], args['input'], args['output'], args['cutoff'], args['anti'], args['threads'])