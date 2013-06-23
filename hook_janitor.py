'''
Created on 02.03.2013

@author: steffen
'''

import os

def clean_temp_files():
	for root, dirnames, filenames in os.walk('./', topdown = True):
		for filename in filenames:
			if filename[-1] == '~':
				print 'remove ' + root + '/' + filename
				os.remove(root + '/' + filename)
