import numpy as np
from bitarray import bitarray


def xspare(x, attention_threshold=0.5, elimination_threshold=1., elimination_count_threshold=None, return_columns=False):
	x = np.array(x)
	corr = np.corrcoef(x.T)
	
	rows = []
	cols = corr.shape[0]

	for i in range(cols):
		row = [0, i, bitarray(cols)]

		for j in range(cols):
			if abs(corr[i, j]) >= attention_threshold:
				row[2][j] = True

		row[0] = row[2].count(1)
		rows.append(row)

	rows = tuple(sorted(rows, reverse=True))

	excluded = bitarray(cols)
	excluded.setall(1)

	for row in rows:
		if elimination_count_threshold != None and (row[2] & excluded).count(1) >= elimination_count_threshold:
			excluded[row[1]] = False
		elif (row[2] & excluded).count(1) / cols >= elimination_threshold:
			excluded[row[1]] = False

	if return_columns:
		return np.array(excluded.tolist(), dtype=bool)
	else:
		return x[:, np.array(excluded.tolist(), dtype=bool)]
