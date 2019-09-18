#!/usr/bin/env python

import subprocess
import os

devnull = open(os.devnull, 'w')

#TODO: atom, tree, gcc, build-essential, make, cmake, net-tools, transmission
#TODO: SNAP: acrordrdc
apps = [
	'indicator-multiload',
	'filezilla',
	'ghex',
	'google-chrome-stable',
	'kompare',
	'terminology'
]

pre_task = [
	'google-chrome-stable',
	'terminology'
]

post_task = [
	'indicator-multiload'
]

def pre_tasks(app):
	print('Running pre-install tasks for ' + app)

	if app == 'google-chrome-stable':
# First add repo to source list
		ret = subprocess.call('wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -', shell=True)
		if ret != 0:
			return False
		subprocess.call('sudo sh -c \'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list\'', shell=True)		
		subprocess.call('sudo apt-get update', shell=True)
# Note: To avoid dialog about password for keyring disable auto-login in Ubuntu user settings
	
	if app == 'terminology':
# First add repo to source list
		ret = subprocess.call('sudo add-apt-repository ppa:niko2040/e19', shell=True)
# Will need to press enter to confirm adding stable repo (vs daily builds)
		if ret != 0:
			return False
		subprocess.call('sudo apt-get update', shell=True)
# Dependency libefl needs to be added manually if not already installed
# Ideally the following could have been used to check for this:
#	$ ldconfig -p | grep libefl
		subprocess.call('sudo apt -y install libefl', shell=True)
# Make sure any data from previous installs is removed (of new install will fail) 
		subprocess.call('sudo apt remove terminology-data', shell=True)

	return True

def post_tasks(app):
	print('Running post-install tasks for ' + app)

	if app == 'indicator-multiload':
# First time start after install will add appropriate file to ~/config/autostart
# so subsequent manual starts shouldn't be needed
		subprocess.call(app + '&', shell=True)
# Applying saved settings assuming the file is available
# To create the file use:
#	$ dconf dump /de/mh21/indicator-multiload/ > ~/indicator-multiload.dconf
		subprocess.call('dconf load /de/mh21/indicator-multiload/ < ./indicator-multiload.dconf', shell=True)

	return True

def is_installed(app):
	if subprocess.call('which ' + app, shell=True, stdout=devnull) == 1:
		return False
	else:
		return True

def install(app):
	ret = True
	print('Installing ' + app)

	if app in pre_task:
		ret = pre_tasks(app)
# Pre-task must pass
	if ret != True:
		print('Pre-task failed: ' + app)
		return False
	else:
		subprocess.call('sudo apt -y install ' + app, shell=True)
# Check if install succeeded
	if is_installed(app) != True:
		print('Install failed: ' + app)
		return False
	else:
		if app in post_task:
			ret = post_tasks(app)
# Warning if post-task fails
	if ret != True:
		print('[WARNING] Post-task failed: ' + app)
	return True

subprocess.call('echo "Running Install Script..."', shell=True)

for app in apps:
	if is_installed(app) == False:
		install(app)



#output1 = subprocess.check_output('which indicator-multiload', shell=True)


