import pip
print "\nYou have already installed... : \n"
installed_packages = pip.get_installed_distributions()
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages if i.key=="matplotlib" or i.key=="numpy" or i.key=="pylab"])
print(installed_packages_list)
