from pathlib import Path
import sys
import numpy as np
from astropy.table import Table


def get_tractor_data(rootdir, outdir=None):
    # coadddir = rootdir / 'coadd'
    rootdir = Path(rootdir)
    tracdir = rootdir / 'tractor'
    coords  = []
    brname = []
    for path in tracdir.glob("*"):
        for brpath in path.glob("tractor-*"):
            brname.append(brpath.name)
            dtab = Table.read(brpath)
            coords.append((dtab['ra'].data, dtab['dec'].data))
    datcoords = np.hstack(coords).T
    bricks = [br.split('-')[1].split('.')[0] for br in brname]
    if outdir:
        outdir = Path(outdir)
        outdir.mkdir(exist_ok=True)
        np.save(outdir / 'bricks.npy', bricks)
        np.save(outdir / 'coords.npy', datcoords)    
    return bricks, datcoords


if __name__ == '__main__':
    rootdir = sys.argv[1]
    outdir = None if len(sys.argv) > 2 else sys.argv[2]
    print('Getting tractor data...',
          '\nRoot directory:', rootdir,
          '\nOutput directory', outdir
          )
    get_tractor_data(rootdir, outdir)
    print('Done')
