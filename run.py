#!/usr/bin/env python

import subprocess
import os

devnull = open(os.devnull, 'w')

#TODO: atom, vlc
#TODO: SNAP: acrordrdc
apps = [
	'indicator-multiload',
	'filezilla',
	'ghex',
#	'google-chrome-stable',
	'kompare',
	'terminology',
	'tree',
	'gcc',
	'build-essential',
	'make',
	'cmake',
	'net-tools',
	'transmission-gtk',
	'atom'
]

pre_task = [
#	'google-chrome-stable',
	'terminology',
	'atom'
]

post_task = [
	'indicator-multiload'
]

def pre_tasks(app):
	print('[***UBI***] Running pre-install tasks for ' + app)

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
		ret = subprocess.call('sudo add-apt-repository ppa:niko2040/e19 -y', shell=True)
# Will need to press enter to confirm adding stable repo (vs daily builds)
		if ret != 0:
			return False
		subprocess.call('sudo apt-get update', shell=True)
# Dependency libefl needs to be added manually if not already installed
# Ideally the following could have been used to check for this:
#	$ ldconfig -p | grep libefl
		subprocess.call('sudo apt -y install libefl', shell=True)
# Make sure any data from previous installs is removed (or new install will fail) 
		subprocess.call('sudo apt remove terminology-data', shell=True)

	if app == 'atom':
		ret = subprocess.call('wget -qO - https://packagecloud.io/AtomEditor/atom/gpgkey | sudo apt-key add -', shell=True)
		if ret != 0:
			return False
		subprocess.call('sudo sh -c \'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list\'', shell=True)
		subprocess.call('sudo apt-get update', shell=True)

	return True

def post_tasks(app):
	print('[***UBI***] Running post-install tasks for ' + app)

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
	output = subprocess.check_output('apt list --installed ' + app, shell=True)
	if output.find('installed') == -1:
		return False
	else:
		return True

def install(app):
	ret = True
	print('[***UBI***] Installing ' + app)

	if app in pre_task:
		ret = pre_tasks(app)
# Pre-task must pass
	if ret != True:
		print('[***UBI:ERROR***] Pre-task failed: ' + app)
		return False
	else:
		subprocess.call('sudo apt -y install ' + app, shell=True)
# Check if install succeeded
	if is_installed(app) != True:
		print('[***UBI:ERROR***] Install failed: ' + app)
		return False
	else:
		print('[***UBI***] Install succeeded: ' + app)
		if app in post_task:
			ret = post_tasks(app)
# Warning if post-task fails
	if ret != True:
		print('[***UBI:WARNING***] Post-task failed: ' + app)
	return True


print('[***UBI***] Running Install Script...')

for app in apps:
	if is_installed(app) == False:
		install(app)
	else:
		print('[***UBI***] ' + app + ' already installed, nothing to do.')



