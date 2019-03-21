#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""auto-run script for ont-vaas tool on cloud platform
"""
import os
import sys
import json
import requests
import urllib.parse
from collections import OrderedDict


def testONT(path):

	with open(path, "r") as f:
		text = f.read()

	filename = os.path.basename(path)
	# headerdata = {"Content-type": "application/json"}
	data = {"contractName": filename, "contracts": [{"fileName": filename, "fileCode": text}]}

	try:
		ret = requests.post("http://ec2-54-183-244-8.us-west-1.compute.amazonaws.com/ont", str(json.dumps(data)))
		#ret = requests.post("http://localhost:9080/ont", str(json.dumps(data)))
		return ret.content.decode("utf-8")
	except Exception:
		return 'HTTP Error'


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('input target file, please')
		print('command format: \n run_ont_vaas_on_platform.py filename')
		exit(0)
	res = testONT(sys.argv[1])
	try:
		obj = json.loads(res, object_pairs_hook=OrderedDict)
		try:
			for key in obj:
				print("\n")
				print("cfg_path:","http://ec2-54-183-244-8.us-west-1.compute.amazonaws.com/ont/cfg/"+key.split("/")[2]) 
				break
			print("\n")
		except Exception:
			pass
		print(json.dumps(obj, default=lambda obj: obj.__dict__, sort_keys=False, indent=4, ensure_ascii=False))
	except Exception:
		print(res)
