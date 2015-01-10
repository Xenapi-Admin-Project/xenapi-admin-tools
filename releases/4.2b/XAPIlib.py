# Library for XenAPI Admin Python Tools
# 12/22/2013
# 

def formatdarray(data, order, CSV, minspace):
	string_data = [[str(row[col]) for col in order] for row in data]
	string_data.insert(0, [name for name in order])
	if CSV:
		csv = [','.join(row) for row in string_data]
		return '\n'.join(line for line in csv)
	else:
		colwidths = [max(len(row[col]) for row in string_data) for col in range(len(order))]
		formatstr = (' ' * minspace).join('%%-%ds' % width for width in colwidths)
	return '\n'.join(formatstr % tuple(line) for line in string_data)
	
	
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

