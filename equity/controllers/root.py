# -*- coding: utf-8 -*-
#
# Equity - An online driver location database service.
#
# Copyright (C) 2009 Jon Masters <jcm@jonmasters.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from tg import expose, flash, require, url, request, redirect, validate
from tg.decorators import paginate
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from catwalk.tg2 import Catwalk
from repoze.what import predicates
from repoze.what.predicates import not_anonymous, has_permission

from equity import release
from equity.lib.base import BaseController, Controller
from equity.model import DBSession, metadata
from equity.controllers.error import ErrorController
from equity import model
from equity.controllers.secure import SecureController

from tw.api import WidgetsList, js_callback
from tw.forms import Spacer, Label, TableForm, CalendarDatePicker
from tw.forms import SingleSelectField, MultipleSelectField, HiddenField
from tw.forms import TextField, TextArea, DataGrid
from tw.forms.validators import Int, NotEmpty, DateConverter

from equity.model.auth import User
from equity.model.main import State, Comment, Description, Arch, License
from equity.model.main import Name, Vendor, SystemFamily, System, OSFamily
from equity.model.main import OSRelease, Kernel, DeviceType, Device
from equity.model.main import DeviceAlias, DriverType, Driver, DriverMeta
from equity.model.main import DriverBuild, DriverBuildMeta
import pylons
from sqlalchemy import or_, and_, desc

from xmlrpclib import loads, dumps, Fault
from tg import tmpl_context, response
from tg.controllers import CUSTOM_CONTENT_TYPE
from pylons.controllers.xmlrpc import XMLRPCController
from pylons.controllers.util import forward

from datetime import datetime

__all__ = ['RootController', 'ArchController', 'LicenseController',
	   'VendorController', 'SystemFamilyController', 'SystemController',
	   'OSFamilyController', 'OSReleaseController', 'KernelController',
	   'DeviceTypeController', 'DeviceController', 'DeviceAliasController',
	   'DriverTypeController', 'DriverController', 'DriverBuildController']

class ArchForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='Arch Name',
		  help_text='Please enter the standardized arch name'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this architecture:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add Arch'

class ArchController(Controller):
    """
    The arch controller for the equity application.
    """

    @expose('equity.templates.arches')
    @paginate('arches', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	arches = DBSession.query(Arch).order_by('name')
	return dict(arches=arches, num_items=arches.count(),
		    admin=admin)

    @expose('equity.templates.arch_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = ArchForm("new_arch_form", action='create')
	return dict()

    @validate(ArchForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new arch and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	arch = Arch()
	arch.name = name
	arch.state.creator = user
	arch.state.owner = owner
	arch.comments.append(Comment(comment=comment))
	DBSession.add(arch)
	DBSession.flush()
	redirect("index")

    @expose('equity.templates.arch')
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	arch_name = args[0]
	arch = Arch.by_arch_name(arch_name)
	return dict(arch=arch,
		    admin=admin)

class LicenseForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='License Name',
		  help_text='Please enter the standardized license name'),
	SingleSelectField('free',
		  options=['True','False'],
		  help_text = 'Please specify if the License is GPL Compatible.'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this license:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add License'

class LicenseController(Controller):
    """
    The license controller for the equity application.
    """

    @expose('equity.templates.licenses')
    @paginate('licenses', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	licenses = DBSession.query(License).order_by('name')
	return dict(licenses=licenses, num_items=licenses.count(),
		    admin=admin)

    @expose('equity.templates.license_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = LicenseForm("new_license_form", action='create')
	return dict()

    @validate(LicenseForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new license and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	if kw['free']=='True':
		free=True
	else:
		free=False
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	license = License()
	license.name = name
	license.free = free
	license.state.creator = user
	license.state.owner = owner
	license.comments.append(Comment(comment=comment))
	DBSession.add(license)
	DBSession.flush()
	redirect("index")

    @expose('equity.templates.license')
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	license_name = args[0]
	license = License.by_license_name(license_name)
	return dict(license=license,
		    admin=admin)

class VendorForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='Vendor Name',
		  help_text='Please enter the standardized vendor name'),
	TextField('website',
		  label_text='Website',
		  help_text='Please enter the vendor website address'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this vendor:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add Vendor'

class VendorController(Controller):
    """
    The vendor controller for the equity application.
    """

    @expose('equity.templates.vendors')
    @paginate('vendors', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	vendors = DBSession.query(Vendor).order_by('name')
	return dict(vendors=vendors, num_items=vendors.count(),
		    admin=admin)

    @expose('equity.templates.vendor_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = VendorForm("new_vendor_form", action='create')
	return dict()

    @validate(VendorForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new vendor and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	website = kw['website']
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	vendor = Vendor()
	vendor.name = name
	vendor.website = website
	vendor.state.creator = user
	vendor.state.owner = owner
	vendor.comments.append(Comment(comment=comment))
	DBSession.add(vendor)
	DBSession.flush()
	redirect("index")

    @expose('equity.templates.vendor')
    @paginate('names', items_per_page=20, use_prefix=False)
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	vendor_name = args[0]
	vendor = Vendor.by_vendor_name(vendor_name)
	names = vendor.other_names
	return dict(vendor=vendor, names=names,
		    admin=admin)

class SystemFamilyForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='System Family Name',
		  help_text='Please enter the standardized system family name'),
	SingleSelectField('vendor',
		  options=lambda:[v.name for v in Vendor.get_all_vendors()],
		  help_text = 'Please choose the vendor.'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this system family:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add System Family'

class SystemFamilyController(Controller):
    """
    The systemfamily controller for the equity application.
    """

    @expose('equity.templates.systemfamilies')
    @paginate('systemfamilies', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	systemfamilies = DBSession.query(SystemFamily).order_by('name')
	return dict(systemfamilies=systemfamilies,
		    num_items=systemfamilies.count(),
		    admin=admin)

    @expose('equity.templates.osfamily_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = SystemFamilyForm("new_systemfamily_form", action='create')
	return dict()

    @validate(SystemFamilyForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new systemfamily and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	vendor = Vendor.by_vendor_name(kw['vendor'])
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	systemfamily = SystemFamily()
	systemfamily.name = name
	systemfamily.vendor = vendor
	systemfamily.state.creator = user
	systemfamily.state.owner = owner
	systemfamily.comments.append(Comment(comment=comment))
	DBSession.add(systemfamily)
	DBSession.flush()
	redirect("index")

    @expose('equity.templates.systemfamily')
    @paginate('systems', items_per_page=20, use_prefix=False)
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	systemfamily_name = args[0]
	systemfamily = SystemFamily.by_systemfamily_name(systemfamily_name)
	systems = systemfamily.systems
	return dict(systemfamily=systemfamily, systems=systems,
		    admin=admin)

class SystemForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='System Name',
		  help_text='Please enter the standardized system name'),
	SingleSelectField('vendor',
		  options=lambda:[v.name for v in Vendor.get_all_vendors()],
		  help_text = 'Please choose the vendor.'),
	SingleSelectField('family',
		  options=lambda:[f.name for f in SystemFamily.get_all_systemfamilies()],
		  help_text = 'Please choose the system family.'),
	TextField('version', validator=NotEmpty,
		  label_text='Version',
		  help_text='Please enter the system version.'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this system:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add System'

class SystemController(Controller):
    """
    The system contoller for the equity application.
    """

    @expose('equity.templates.systems')
    @paginate('systems', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	systems = DBSession.query(System).order_by('name')
	return dict(systems=systems, num_items=systems.count(),
		    admin=admin)

    @expose('equity.templates.system_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = SystemForm("new_system_form", action='create')
	return dict()

    @validate(SystemForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new device and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	vendor = Vendor.by_vendor_name(kw['vendor'])
	systemfamily = SystemFamily.by_systemfamily_name(kw['family'])
	version = kw['version']
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	system = System()
	system.name = name
	system.vendor = vendor
	system.systemfamily = systemfamily
	system.version = version
	system.state.creator = user
	system.state.owner = owner
	system.comments.append(Comment(comment=comment))
	DBSession.add(system)
	DBSession.flush()
	redirect("index")

    @expose('equity.templates.system')
    @paginate('devices', items_per_page=20, use_prefix=False)
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	system_name = args[0]
	system = System.by_system_name(system_name)
	devices = system.devices
	return dict(system=system, devices=devices,
		    admin=admin)

class OSFamilyForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='Operating System Name',
		  help_text='Please enter the standardized operating system name'),
	SingleSelectField('vendor',
		  options=lambda:[v.name for v in Vendor.get_all_vendors()],
		  help_text = 'Please choose the vendor.'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this operating system:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add Operating System'

class OSFamilyController(Controller):
    """
    The osfamily controller for the equity application.
    """

    @expose('equity.templates.osfamilies')
    @paginate('osfamilies', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	osfamilies = DBSession.query(OSFamily).order_by('name')
	return dict(osfamilies=osfamilies, num_items=osfamilies.count(),
		    admin=admin)

    @expose('equity.templates.osfamily_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = OSFamilyForm("new_osfamily_form", action='create')
	return dict()

    @validate(OSFamilyForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new osfamily and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	vendor = Vendor.by_vendor_name(kw['vendor'])
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	osfamily = OSFamily()
	osfamily.name = name
	osfamily.vendor = vendor
	osfamily.state.creator = user
	osfamily.state.owner = owner
	osfamily.comments.append(Comment(comment=comment))
	DBSession.add(osfamily)
	DBSession.flush()
	redirect("index")

    @expose('equity.templates.osfamily')
    @paginate('osreleases', items_per_page=20, use_prefix=True)
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	osfamily_name = args[0]
	osfamily = OSFamily.by_osfamily_name(osfamily_name)
	osreleases = osfamily.osreleases
	return dict(osfamily=osfamily, osreleases=osreleases,
		    admin=admin)

class OSReleaseController(Controller):
    """
    The osrelease controller for the equity application.
    """

class KernelForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='Kernel Name',
		  help_text='Please enter the standardized kernel name'),
	SingleSelectField('arch',
		  options=lambda:[a.name for a in Arch.get_all_arches()],
		  help_text = 'Please choose the architecture.'),
	SingleSelectField('osrelease',
		  options=lambda:[r.name for r in OSRelease.get_all_osreleases()],
		  help_text = 'Please choose the Operating System.'),
	SingleSelectField('vendor',
		  options=lambda:[v.name for v in Vendor.get_all_vendors()],
		  help_text = 'Please choose the vendor.'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this kernel:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add Kernel'

class KernelController(Controller):
    """
    The kernel controller for the equity application.
    """

    @expose('equity.templates.kernels')
    @paginate('kernels', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	kernels = DBSession.query(Kernel).order_by('name')
	return dict(kernels=kernels, num_items=kernels.count(),
		    admin=admin)

    @expose('equity.templates.kernel_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = KernelForm("new_kernel_form", action='create')
	return dict()

    @validate(KernelForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new kernel and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	arch = Arch.by_arch_name(kw['arch'])
	osrelease = OSRelease.by_osrelease_name(kw['osrelease'])
	vendor = Vendor.by_vendor_name(kw['vendor'])
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	kernel = Kernel()
	kernel.name = name
	kernel.arch = arch
	kernel.osrelease = osrelease
	kernel.vendor = vendor
	kernel.state.creator = user
	kernel.state.owner = owner
	kernel.comments.append(Comment(comment=comment))
	DBSession.add(kernel)
	DBSession.flush()
	redirect("index")

    @expose('equity.templates.kernel')
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	kernel_name = args[0]
	kernel = Kernel.by_kernel_name(kernel_name)
	return dict(kernel=kernel,
		    admin=admin)

class DeviceTypeForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='Device Type Name',
		  help_text='Please enter the standardized device type name'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this device type:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add Device Type'

class DeviceTypeController(Controller):
    """
    The devicetype controller for the equity application.
    """

    @expose('equity.templates.devicetypes')
    @paginate('devicetypes', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	devicetypes = DBSession.query(DeviceType).order_by('name')
	return dict(devicetypes=devicetypes, num_items=devicetypes.count(),
		    admin=admin)

    @expose('equity.templates.devicetype_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = DeviceTypeForm("new_devicetype_form", action='create')
	return dict()

    @validate(DeviceTypeForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new devicetype and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	devicetype = DeviceType()
	devicetype.name = name
	devicetype.state.creator = user
	devicetype.state.owner = owner
	devicetype.comments.append(Comment(comment=comment))
	DBSession.add(devicetype)
	DBSession.flush()
	redirect("index")

    @expose('equity.templates.devicetype')
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	devicetype_name = args[0]
	devicetype = DeviceType.by_devicetype_name(devicetype_name)
	return dict(devicetype=devicetype,
		    admin=admin)

class DeviceForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='Device Name',
		  help_text='Please enter the standardized device type name'),
	SingleSelectField('vendor',
		  options=lambda:[v.name for v in Vendor.get_all_vendors()],
		  help_text = 'Please choose the vendor.'),
	SingleSelectField('type',
		  options=lambda:[t.name for t in DeviceType.get_all_devicetypes()],
		  help_text = 'Please choose the device type.'),
	TextField('version', validator=NotEmpty,
		  label_text='Version',
		  help_text='Please enter the device version.'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this device:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add Device'

class DeviceSystemForm(TableForm):

    fields = [
	HiddenField('device_id',
		    default='unknown'),
	SingleSelectField('system',
		options=lambda:[s.name for s in System.get_all_systems()],
		label_text='')]

    submit_text = 'Add To System'

class DeviceAliasForm(TableForm):

    fields = [
	HiddenField('device_id',
		    default='unknown'),
	TextField('alias', validator=NotEmpty,
		  label_text='', size=30)]

    submit_text = 'Add Alias'

class DeviceController(Controller):
    """
    The device controller for the equity application.
    """

    @expose('equity.templates.devices')
    @paginate('devices', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	devices = DBSession.query(Device).order_by('name')
	return dict(devices=devices, num_items=devices.count(),
		    admin=admin)

    @expose('equity.templates.device_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = DeviceForm("new_device_form", action='create')
	return dict()

    @validate(DeviceForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new device and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	vendor = Vendor.by_vendor_name(kw['vendor'])
	devicetype = DeviceType.by_devicetype_name(kw['type'])
	version = kw['version']
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	device = Device()
	device.name = name
	device.vendor = vendor
	device.devicetype = devicetype
	device.version = version
	device.state.creator = user
	device.state.owner = owner
	device.comments.append(Comment(comment=comment))
	DBSession.add(device)
	DBSession.flush()
	redirect("index")

    @validate(DeviceAliasForm(), error_handler=index)
    @expose()
    def addalias(self, **kw):
	"""Create a new device alias and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	alias = kw['alias']
	device = Device.by_device_id(kw['device_id'])
	owner = device.state.owner
	comment = alias
	devicealias = DeviceAlias()
	devicealias.alias = alias
	devicealias.device = device
	devicealias.state.creator = user
	devicealias.state.owner = owner
	devicealias.comments.append(Comment(comment=comment))
	DBSession.add(device)
	DBSession.flush()
	redirect("/devices/"+device.name)

    @validate(DeviceSystemForm(), error_handler=index)
    @expose()
    def addsystem(self, **kw):
	"""Add a system to a device and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	device = Device.by_device_id(kw['device_id'])
	system = System.by_system_name(kw['system'])
	device.systems.append(system)
	DBSession.flush()
	redirect("/devices/"+device.name)

    @expose('equity.templates.device')
    @paginate('drivers', items_per_page=20, use_prefix=True)
    @paginate('aliases', items_per_page=20, use_prefix=True)
    @paginate('systems', items_per_page=20, use_prefix=True)
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	device_name = args[0]
	device = Device.by_device_name(device_name)
	drivers = device.drivers
	aliases = device.devicealiases
	systems = device.systems

	tmpl_context.systems_form = DeviceSystemForm("new_device_system_form", action='addsystem',
			    )
	tmpl_context.alias_form = DeviceAliasForm("new_device_alias_form", action='addalias',
			    )
	return dict(device=device, drivers=drivers, aliases=aliases, systems=systems,
		    admin=admin)

class DeviceAliasController(Controller):
    """
    The devicealias controller for the equity application.
    """

class DriverTypeForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='Driver Type Name',
		  help_text='Please enter the standardized driver type name'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this driver type:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add Driver Type'

class DriverTypeController(Controller):
    """
    The drivertype controller for the equity application.
    """

    @expose('equity.templates.drivertypes')
    @paginate('drivertypes', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	drivertypes = DBSession.query(DriverType).order_by('name')
	return dict(drivertypes=drivertypes, num_items=drivertypes.count(),
		    admin=admin)

    @expose('equity.templates.drivertype_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = DeviceTypeForm("new_drivertype_form", action='create')
	return dict()

    @validate(DeviceTypeForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new drivertype and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	drivertype = DriverType()
	drivertype.name = name
	drivertype.state.creator = user
	drivertype.state.owner = owner
	drivertype.comments.append(Comment(comment=comment))
	DBSession.add(drivertype)
	DBSession.flush()
	redirect("index")

    @expose('equity.templates.drivertype')
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	drivertype_name = args[0]
	drivertype = DriverType.by_drivertype_name(drivertype_name)
	return dict(drivertype=drivertype,
		    admin=admin)

class DriverForm(TableForm):

    fields = [
	TextField('name', validator=NotEmpty,
		  label_text='Driver Name',
		  help_text='Please enter the standardized driver name'),
	SingleSelectField('type',
		  options=lambda:[t.name for t in DriverType.get_all_drivertypes()],
		  help_text = 'Please choose the driver type.'),
	SingleSelectField('license',
		  options=lambda:[l.name for l in License.get_all_licenses()],
		  help_text = 'Please choose the license.'),
	SingleSelectField('vendor',
		  options=lambda:[v.name for v in Vendor.get_all_vendors()],
		  help_text = 'Please choose the vendor.'),
        TextField('version', validator=NotEmpty,
		  label_text='Driver Version',
		  help_text='Please enter the driver version.'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this driver:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add Driver'

class DriverBuildMetaForm(TableForm):

    fields = [
	HiddenField('driverbuild_id',
		    default='unknown'),
	TextField('tag', validator=NotEmpty,
		  label_text='Tag', size=10),
	TextField('value', validator=NotEmpty,
		  label_text='Value', size=10)]

    submit_text = 'Add Meta'

class DriverDeviceForm(TableForm):

    fields = [
	HiddenField('driver_id',
		    default='unknown'),
	SingleSelectField('device',
		options=lambda:[d.name for d in Device.get_all_devices()],
		label_text='')]

    submit_text = 'Add To Device'

class DriverController(Controller):
    """
    The driver controller for the equity application.
    """

    @expose('equity.templates.drivers')
    @paginate('drivers', items_per_page=20, use_prefix=False)
    def index(self):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	drivers = DBSession.query(Driver).order_by('name')
	return dict(drivers=drivers, num_items=drivers.count(),
		    admin=admin)

    @expose('equity.templates.driver_new')
    @require(has_permission('admin'))
    def new(self):
	tmpl_context.form = DriverForm("new_driver_form", action='create')
	return dict()

    @validate(DriverForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new driver and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	name = kw['name']
	drivertype = DriverType.by_drivertype_name(kw['type'])
	license = License.by_license_name(kw['license'])
	vendor = Vendor.by_vendor_name(kw['vendor'])
	version = kw['version']
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	driver = Driver()
	driver.name = name
	driver.drivertype = drivertype
	driver.license = license
	driver.vendor = vendor
	driver.version = version
	driver.state.creator = user
	driver.state.owner = owner
	driver.comments.append(Comment(comment=comment))
	DBSession.add(driver)
	DBSession.flush()
	redirect("index")

    @validate(DeviceAliasForm(), error_handler=index)
    @expose()
    def addalias(self, **kw):
	"""Create a new device alias and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	alias = kw['alias']
	device = Device.by_device_id(kw['device_id'])
	owner = device.state.owner
	comment = alias
	devicealias = DeviceAlias()
	devicealias.alias = alias
	devicealias.device = device
	devicealias.state.creator = user
	devicealias.state.owner = owner
	devicealias.comments.append(Comment(comment=comment))
	DBSession.add(device)
	DBSession.flush()
	redirect("/devices/"+device.name)

    @validate(DriverBuildMetaForm(), error_handler=index)
    @expose()
    def addmeta(self, **kw):
	"""Create a new device alias and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	driverbuild = DriverBuild.by_driverbuild_id(kw['driverbuild_id'])
	tag = kw['tag']
	value = kw['value']
	owner = driverbuild.state.owner
	comment = tag
	driverbuildmeta = DriverBuildMeta()
	driverbuildmeta.driverbuild = driverbuild
	driverbuildmeta.tag = tag
	driverbuildmeta.value = value
	driverbuildmeta.state.creator = user
	driverbuildmeta.state.owner = owner
	driverbuildmeta.comments.append(Comment(comment=comment))
	DBSession.add(driverbuildmeta)
	DBSession.flush()
	redirect("/drivers/"+driverbuild.driver.name)

    @validate(DriverDeviceForm(), error_handler=index)
    @expose()
    def adddevice(self, **kw):
	"""Add a driver to a device and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	driver = Driver.by_driver_id(kw['driver_id'])
	device = Device.by_device_name(kw['device'])
	driver.devices.append(device)
	DBSession.flush()
	redirect("/drivers/"+driver.name)

    @expose('equity.templates.driver')
    @paginate('devices', items_per_page=20, use_prefix=True)
    @paginate('descriptions', items_per_page=20, use_prefix=True)
    @paginate('builds', items_per_page=1, use_prefix=True)
    def default(self, *args):
	admin=False
	if predicates.not_anonymous():
		if predicates.has_permission('admin'):
			admin=True
	driver_name = args[0]
	driver = Driver.by_driver_name(driver_name)
	devices = driver.devices
	descriptions = driver.descriptions
	builds = driver.driverbuilds
	tmpl_context.devices_form = DriverDeviceForm("new_driver_device_form", action='adddevice',
			    )
	tmpl_context.meta_form = DriverBuildMetaForm("new_driver_build_meta_form", action='addmeta',
			    )
	return dict(driver=driver, devices=devices, descriptions=descriptions,
		    builds=builds,
		    admin=admin)

class DriverBuildForm(TableForm):

    fields = [
	HiddenField('driver_id',
		  default='unknown'),
	SingleSelectField('kernel',
		  options=lambda:[k.name for k in Kernel.get_all_kernels()],
		  help_text = 'Please choose the kernel.'),
	SingleSelectField('vendor',
		  options=lambda:[v.name for v in Vendor.get_all_vendors()],
		  help_text = 'Please choose the vendor.'),
        TextField('version', validator=NotEmpty,
		  label_text='Driver Version',
		  help_text='Please enter the driver version.'),
	SingleSelectField('owner',
		  options=lambda:[u.user_name for u in User.get_all_users()],
		  help_text = 'Please choose the owner.'),
	Spacer(),
	Label(text='Please provide a short comment about this driver build:'),
	TextArea('comment', attrs=dict(rows=4, cols=25)),
	Spacer()]

    submit_text = 'Add Driver Build'

class DriverBuildController(Controller):
    """
    The driver build controller for the equity application.
    """

    @expose('equity.templates.driverbuild_new')
    @require(has_permission('admin'))
    def new(self, driver_id):
	tmpl_context.form = DriverBuildForm("new_driverbuild_form", action='create')
	return dict(driver_id=driver_id)

    @validate(DriverBuildForm(), error_handler=new)
    @expose()
    def create(self, **kw):
	"""Create a new driverbuild and save it to the database."""
	user = request.environ.get('repoze.who.identity')['user']
	driver = Driver.by_driver_id(kw['driver_id'])
	kernel = Kernel.by_kernel_name(kw['kernel'])
	vendor = Vendor.by_vendor_name(kw['vendor'])
	version = kw['version']
	comment = kw['comment']
	owner = User.by_user_name(kw['owner'])
	if comment == "":
		comment = name
	driverbuild = DriverBuild()
	driverbuild.driver = driver
	driverbuild.kernel = kernel
	driverbuild.vendor = vendor
	driverbuild.version = version
	driverbuild.state.creator = user
	driverbuild.state.owner = owner
	driverbuild.comments.append(Comment(comment=comment))
	DBSession.add(driverbuild)
	DBSession.flush()
	redirect("/drivers/"+driver.name)

def get_driverDescs(system_vendor_name, system_product_name,
		    osfamily_name, osrelease_version,
		    kernel_name, arch_name,
		    components):

	system = None

	system_vendor = Vendor.by_vendor_name(system_vendor_name)
	if system_vendor:
		system = System.by_system_vendor_and_name(system_vendor,
							  system_product_name)

	# components are only optional if the system detail is supplied.
	if (not system) and (components==[]):
		return {}

	# FIXME: must parse modaliases specially if they are here
	# will add a special meta-tag to indicate the requirement.
	devices = []
	for component in components:
		devicealias = DeviceAlias.by_devicealias(component)
		if devicealias:
			devices.append(devicealias.device)

	osrelease = None
	osfamily = OSFamily.by_osfamily_name(osfamily_name)
	if osfamily:
		osrelease = OSRelease.by_osrelease_osfamily_and_version(
							  osfamily,
							  osrelease_version)

	# not going to return any devices unless an OSRelease is given
	if not osrelease:
		return {}

	arch = Arch.by_arch_name(arch_name)
	# not going to return any devices unless an Arch is given
	if not arch:
		return {}

	kernel = Kernel.by_kernel_osrelease_arch_and_name(osrelease,
							  arch,
							  kernel_name)
	# not going to return any devices unless a Kernel is given
	if not kernel:
		return {}

	results = {}
	for device in system.devices:
		# ignore the device if it wasn't asked about or none were
		if (not components==[]) and (not device in devices):
			continue

		for driver in device.drivers:
			if kernel in driver.kernels:
				driver_type=driver.drivertype.name
				driver_meta={}
				for meta in driver.drivermeta:
					driver_meta[meta.tag] = meta.value
				free=driver.license.free
				license=driver.license.name

				prefix=driver.drivertype.prefix
				for alias in device.devicealiases:
					devalias = prefix + alias.alias

					for build in driver.driverbuilds:
						driver_vendor=build.vendor.name
						build_meta={}
						for meta in build.driverbuildmeta:
							build_meta[meta.tag] = meta.value
						description={}
						for desc in build.descriptions:
							description[desc.locale] = desc.description
						
						result = {
							'driver_type': driver_type,
							'driver_vendor': driver_vendor,
							'description': description,
							'free': free,
							'license': license}
						result.update(driver_meta)
						result.update(build_meta)

						if results.has_key(devalias):
							results[devalias].append(result)
						else:
							results[devalias] = [result]

	return results

class EquityXMLRPCController(XMLRPCController):
    """
    The XML-RPC Controller for the equity application.
    """

    def query(self, request):

	(protocol_version, protocol_subversion, query_attributes) = request

	if (not protocol_version==release.protocol_version) \
	or (not protocol_subversion==release.protocol_subversion):
		results = {}
	else:
		#FIXME: probably raise an exception and catch instead here.
		error=False

		if query_attributes.has_key('system_vendor'):
			system_vendor = query_attributes['system_vendor']
		else:
			error=True

		if query_attributes.has_key('system_product'):
			system_product = query_attributes['system_product']
		else:
			error=True

		if query_attributes.has_key('os_name'):
			os_name = query_attributes['os_name']
		else:
			error=True

		if query_attributes.has_key('os_version'):
			os_version = query_attributes['os_version']
		else:
			error=True

		if query_attributes.has_key('kernel_ver'):
			kernel_ver = query_attributes['kernel_ver']
		else:
			error=True

		if query_attributes.has_key('architecture'):
			architecture = query_attributes['architecture']
		else:
			error=True

		if query_attributes.has_key('components'):
			components = query_attributes['components']
		else:
			error=True

		if error:
			results = {}
		else:
			results = get_driverDescs(system_vendor, system_product,
						  os_name, os_version,
						  kernel_ver, architecture,
						  components)

	return (release.protocol_version, release.protocol_subversion, results)

    query.signature = [['array', 'array']]

    def test_foo(self):

	return get_driverDescs( 'IBM', 'T60p',
				'Red Hat Enterprise Linux', '6.0',
				'2.6.xy.z', 'x86_64',
				['pci:v00008086d00002668sv*sd*bc*sc*i*'])

class RootController(BaseController):
    """
    The root controller for the equity application.
    
    All the other controllers and WSGI applications should be mounted on this
    controller. For example::
    
        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()
    
    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.
    
    """
    secc = SecureController()
    
    admin = Catwalk(model, DBSession)
    
    error = ErrorController()

    arches = ArchController()
    licenses = LicenseController()
    vendors = VendorController()
    systemfamilies = SystemFamilyController()
    systems = SystemController()
    osfamilies = OSFamilyController()
    osreleases = OSReleaseController()
    kernels = KernelController()
    devicetypes = DeviceTypeController()
    devices = DeviceController()
    devicealiases = DeviceAliasController()
    drivertypes = DriverTypeController()
    drivers = DriverController()
    driverbuilds = DriverBuildController()

    @expose()
    def RPC2(self, *args, **kw):
	return forward(EquityXMLRPCController())

    @expose('equity.templates.index')
    @paginate('systems', items_per_page=20, use_prefix=False)
    def index(self):
        """Handle the front-page."""

	if predicates.is_anonymous():
		admin=False
		logged_in=False
	else:
		logged_in=True
		user = request.environ.get('repoze.who.identity')['user']
		if predicates.has_permission('admin'):
			admin=True
		else:
			admin=False

        systems = System.get_all_systems()

        return dict(page='index',systems=systems,
		    logged_in=logged_in, admin=admin)

    @expose('equity.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('equity.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)
    
    @expose()
    def post_login(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.
        
        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect(url('/login', came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.
        
        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
