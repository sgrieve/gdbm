from glob import glob

zones = ['A', 'B', 'C', 'D']

for zone in zones:
    filenames = glob('../../Results/{}*_data.csv'.format(zone))

    out_string = ''

    for filename in filenames:
        with open(filename) as f:
            header = f.readline()
            if len(out_string) == 0:
                out_string += header

            lines = f.readlines()
            out_string += ''.join(lines)

    with open('../../Results/{}_data.csv'.format(zone), 'w') as w:
        w.write(out_string)
