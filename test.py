import bz2
with open('phase_4.mf', 'rb') as f:
    file = bz2.BZ2File('phase_4.mf.bz2', 'w')
    file.write(f.read())
    file.close()