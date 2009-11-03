# -*- coding: utf-8 -*-
"""Setup the equity application"""

import logging

import transaction
from tg import config

from equity.config.environment import load_environment

__all__ = ['setup_app']

log = logging.getLogger(__name__)


def setup_app(command, conf, vars):
    """Place any commands to setup equity here"""
    load_environment(conf.global_conf, conf.local_conf)
    # Load the models
    from equity import model
    print "Creating tables"
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)

    print "Creating default account tables"
    admin_user = model.User()
    admin_user.user_name = u'admin'
    admin_user.display_name = u'admin'
    admin_user.email_address = u'admin'
    admin_user.password = u'admin'
    model.DBSession.add(admin_user)

    admin_group = model.Group()
    admin_group.group_name = u'admin'
    admin_group.display_name = u'admin'
    admin_group.users.append(admin_user)
    model.DBSession.add(admin_group)

    admin_permission = model.Permission()
    admin_permission.permission_name = u'admin'
    admin_permission.description = u'The ability to perform admin actions'
    admin_permission.groups.append(admin_group)
    model.DBSession.add(admin_permission)

    rpc_user = model.User()
    rpc_user.user_name = u'rpc'
    rpc_user.display_name = u'XML-RPC Test User'
    rpc_user.email_address = u'rpc'
    rpc_user.password = u'rpc'
    model.DBSession.add(rpc_user)

    normal_user = model.User()
    normal_user.user_name = u'user'
    normal_user.display_name = u'user'
    normal_user.email_address = u'user'
    normal_user.password = u''
    model.DBSession.add(normal_user)

    print "Creating example user (jcm)"
    example_user = model.User()
    example_user.user_name = u'jcm'
    example_user.display_name = u'Jon Masters'
    example_user.email_address = u'jcm@redhat.com'
    example_user.password = u''
    model.DBSession.add(example_user)

    print "Creating example arch"
    example_arch1 = model.Arch()
    example_arch1.name = u'x86_64'
    model.DBSession.add(example_arch1)

    print "Creating example license"
    example_license1 = model.License()
    example_license1.name = u'GPL'
    example_license1.free = True
    model.DBSession.add(example_license1)

    print "Creating example Vendor1"
    example_vendor1 = model.Vendor()
    example_vendor1.name = u'Red Hat'
    example_vendor1.website = u'http://www.redhat.com/'
    model.DBSession.add(example_vendor1)

    print "Creating example Vendor2"
    example_vendor2 = model.Vendor()
    example_vendor2.name = u'IBM'
    example_vendor2.website = u'http://www.ibm.com/'
    model.DBSession.add(example_vendor2)

    print "Creating example Vendor3"
    example_vendor3 = model.Vendor()
    example_vendor3.name = u'Intel'
    example_vendor3.website = u'http://www.intel.com/'
    model.DBSession.add(example_vendor3)

    print "Creating example SystemFamily"
    example_systemfamily = model.SystemFamily()
    example_systemfamily.name = u'Thinkpad T60p'
    example_systemfamily.vendor = example_vendor2
    model.DBSession.add(example_systemfamily)

    print "Creating example System"
    example_system = model.System()
    example_system.name = u'Thinkpad T60p'
    example_system_name1 = model.Name()
    example_system_name1.name = u'T60p'
    example_system.other_names.append(example_system_name1)
    example_system.vendor = example_vendor2
    example_system.version = '2007'
    example_system.systemfamily = example_systemfamily
    model.DBSession.add(example_system)

    print "Creating example OSFamily"
    example_osfamily = model.OSFamily()
    example_osfamily.name = u'Red Hat Enterprise Linux'
    example_osfamily.vendor = example_vendor1
    model.DBSession.add(example_osfamily)

    print "Creating example OSRelease"
    example_osrelease = model.OSRelease()
    example_osrelease.osfamily = example_osfamily
    example_osrelease.name = u'Red Hat Enterprise Linux 6.0'
    example_osrelease.version = u'6.0'
    example_osrelease.vendor = example_vendor1
    model.DBSession.add(example_osrelease)

    print "Creating example Kernel"
    example_kernel = model.Kernel()
    example_kernel.name = u'2.6.xy.z'
    example_kernel.arch = example_arch1
    example_kernel.osrelease = example_osrelease
    example_kernel.vendor = example_vendor1
    model.DBSession.add(example_kernel)

    print "Creating example DeviceType"
    example_devicetype = model.DeviceType()
    example_devicetype.name = u'Audio'
    model.DBSession.add(example_devicetype)

    print "Creating example Device"
    example_device = model.Device()
    example_device.name = u'Intel Corporation 82801G (ICH7 Family) High Definition Audio Controller (rev 02)'
    example_device.version = u'2'
    example_device.vendor = example_vendor3
    example_device.devicetype = example_devicetype
    example_device.systems.append(example_system)
    model.DBSession.add(example_device)

    print "Creating example DeviceAliases"
    example_devicealias1 = model.DeviceAlias()
    example_devicealias1.device = example_device
    example_devicealias1.alias = u'pci:v00008086d0000269Asv*sd*bc*sc*i*'
    model.DBSession.add(example_devicealias1)

    example_devicealias2 = model.DeviceAlias()
    example_devicealias2.device = example_device
    example_devicealias2.alias = u'pci:v00008086d000027D8sv*sd*bc*sc*i*'
    model.DBSession.add(example_devicealias2)

    example_devicealias3 = model.DeviceAlias()
    example_devicealias3.device = example_device
    example_devicealias3.alias = u'pci:v00008086d00002668sv*sd*bc*sc*i*'
    model.DBSession.add(example_devicealias3)

    print "Creating example DriverType"
    example_drivertype = model.DriverType()
    example_drivertype.name = u'kernel_module'
    example_drivertype.prefix = u'modalias:'
    model.DBSession.add(example_drivertype)

    print "Creating example Driver"
    example_driver = model.Driver()
    example_driver.drivertype = example_drivertype
    example_driver.license = example_license1
    example_driver.vendor = example_vendor3
    example_driver.name = u'snd_hda_intel'
    example_driver.devices.append(example_device)
    example_driver.kernels.append(example_kernel)
    model.DBSession.add(example_driver)

    print "Creating example DriverMeta"
    example_drivermeta = model.DriverMeta()
    example_drivermeta.tag = u'kernel_module'
    example_drivermeta.value = u'snd_intel_hda'
    example_drivermeta.driver = example_driver
    model.DBSession.add(example_drivermeta)

    print "Creating example DriverBuild"
    example_driverbuild = model.DriverBuild()
    example_driverbuild.driver = example_driver
    example_driverbuild.kernel = example_kernel
    example_driverbuild.vendor = example_vendor1
    example_driverbuild.repository = u'file:///localhost/'
    example_driverbuild.package = u'foo'
    model.DBSession.add(example_driverbuild)

    print "Creating example DriverBuildMeta"
    example_driverbuildmeta1 = model.DriverBuildMeta()
    example_driverbuildmeta1.tag = u'repository'
    example_driverbuildmeta1.value = u'http://drivers.intel.com/'
    example_driverbuildmeta1.driverbuild = example_driverbuild
    model.DBSession.add(example_driverbuildmeta1)

    example_driverbuildmeta2 = model.DriverBuildMeta()
    example_driverbuildmeta2.tag = u'package'
    example_driverbuildmeta2.value = u'kmod-snd_intel-hda'
    example_driverbuildmeta2.driverbuild = example_driverbuild
    model.DBSession.add(example_driverbuildmeta2)

    model.DBSession.flush()

    transaction.commit()
    print "Successfully setup"
