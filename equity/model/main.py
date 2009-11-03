# -*- coding: utf-8 -*-

import os
from datetime import datetime
import sys

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode

from equity.model import DeclarativeBase, metadata, DBSession
from equity.model.auth import User, Group, Permission

__all__ = ['State', 'Comment', 'Description', 'Arch', 'License', 'Name',
	   'Vendor', 'SystemFamily', 'System', 'OSFamily', 'OSRelease',
	   'Kernel', 'DeviceType', 'Device', 'DeviceAlias', 'DriverType',
	   'Driver', 'DriverMeta', 'DriverBuild', 'DriverBuildMeta']

#{ Association tables

arch_comment_table = Table('arches_comments', metadata,
	Column('arch_id', Integer, ForeignKey('arches.arch_id',
		onupdate="CASCADE", ondelete="CASCADE")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="CASCADE", ondelete="CASCADE"))
)
license_comment_table = Table('licenses_comments', metadata,
	Column('license_id', Integer, ForeignKey('licenses.license_id',
		onupdate="CASCADE", ondelete="CASCADE")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="CASCADE", ondelete="CASCADE"))
)
license_description_table = Table('licenses_descriptions', metadata,
	Column('license_id', Integer, ForeignKey('licenses.license_id',
		onupdate="CASCADE", ondelete="CASCADE")),
	Column('description_id', Integer, ForeignKey('descriptions.description_id',
		onupdate="CASCADE", ondelete="CASCADE"))
)
name_comment_table = Table('names_comments', metadata,
	Column('name_id', Integer, ForeignKey('names.name_id',
		onupdate="CASCADE", ondelete="CASCADE")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="CASCADE", ondelete="CASCADE"))
)
vendor_name_table = Table('vendors_names', metadata,
	Column('vendor_id', Integer, ForeignKey('vendors.vendor_id',
		onupdate="CASCADE", ondelete="CASCADE")),
	Column('name_id', Integer, ForeignKey('names.name_id',
		onupdate="CASCADE", ondelete="CASCADE"))
)
vendor_comment_table = Table('vendors_comments', metadata,
	Column('vendor_id', Integer, ForeignKey('vendors.vendor_id',
		onupdate="CASCADE", ondelete="CASCADE")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="CASCADE", ondelete="CASCADE"))
)
systemfamily_name_table = Table('systemfamilies_names', metadata,
	Column('systemfamily_id', Integer, ForeignKey('systemfamilies.systemfamily_id',
		onupdate="CASCADE", ondelete="CASCADE")),
	Column('name_id', Integer, ForeignKey('names.name_id',
		onupdate="CASCADE", ondelete="CASCADE"))
)
systemfamily_comment_table = Table('systemfamilies_comments', metadata,
	Column('family_id', Integer, ForeignKey('systemfamilies.systemfamily_id',
		onupdate="CASCADE", ondelete="CASCADE")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="CASCADE", ondelete="CASCADE"))
)
system_name_table = Table('systems_names', metadata,
	Column('system_id', Integer, ForeignKey('systems.system_id',
		onupdate="CASCADE", ondelete="CASCADE")),
	Column('name_id', Integer, ForeignKey('names.name_id',
		onupdate="CASCADE", ondelete="CASCADE"))
)
system_comment_table = Table('systems_comments', metadata,
	Column('system_id', Integer, ForeignKey('systems.system_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
osfamily_name_table = Table('osfamilies_names', metadata,
	Column('osfamily_id', Integer, ForeignKey('osfamilies.osfamily_id',
		onupdate="cascade", ondelete="cascade")),
	Column('name_id', Integer, ForeignKey('names.name_id',
		onupdate="cascade", ondelete="cascade"))
)
osfamily_comment_table = Table('osfamilies_comments', metadata,
	Column('osfamily_id', Integer, ForeignKey('osfamilies.osfamily_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
osrelease_name_table = Table('osreleases_names', metadata,
	Column('osrelease_id', Integer, ForeignKey('osreleases.osrelease_id',
		onupdate="cascade", ondelete="cascade")),
	Column('name_id', Integer, ForeignKey('names.name_id',
		onupdate="cascade", ondelete="cascade"))
)
osrelease_comment_table = Table('osreleases_comments', metadata,
	Column('osrelease_id', Integer, ForeignKey('osreleases.osrelease_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
kernel_driver_table = Table('kernels_drivers', metadata,
	Column('kernel_id', Integer, ForeignKey('kernels.kernel_id',
		onupdate="cascade", ondelete="cascade")),
	Column('driver_id', Integer, ForeignKey('drivers.driver_id',
		onupdate="cascade", ondelete="cascade"))
)
kernel_comment_table = Table('kernels_comments', metadata,
	Column('kernel_id', Integer, ForeignKey('kernels.kernel_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
devicetype_comment_table = Table('devicetypes_comments', metadata,
	Column('devicetype_id', Integer, ForeignKey('devicetypes.devicetype_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
device_name_table = Table('devices_names', metadata,
	Column('device_id', Integer, ForeignKey('devices.device_id',
		onupdate="cascade", ondelete="cascade")),
	Column('name_id', Integer, ForeignKey('names.name_id',
		onupdate="cascade", ondelete="cascade"))
)
device_driver_table = Table('devices_drivers', metadata,
	Column('device_id', Integer, ForeignKey('devices.device_id',
		onupdate="cascade", ondelete="cascade")),
	Column('driver_id', Integer, ForeignKey('drivers.driver_id',
		onupdate="cascade", ondelete="cascade"))
)
device_system_table = Table('devices_systems', metadata,
	Column('device_id', Integer, ForeignKey('devices.device_id',
		onupdate="cascade", ondelete="cascade")),
	Column('system_id', Integer, ForeignKey('systems.system_id',
		onupdate="cascade", ondelete="cascade"))
)
device_comment_table = Table('devices_comments', metadata,
	Column('device_id', Integer, ForeignKey('devices.device_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
devicealias_comment_table = Table('devicealiases_comments', metadata,
	Column('devicealias_id', Integer, ForeignKey('devicealiases.device_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
drivertype_comment_table = Table('drivertypes_comments', metadata,
	Column('drivertype_id', Integer, ForeignKey('drivertypes.drivertype_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
driver_description_table = Table('drivers_descriptions', metadata,
	Column('driver_id', Integer, ForeignKey('drivers.driver_id',
		onupdate="cascade", ondelete="cascade")),
	Column('description_id', Integer, ForeignKey('descriptions.description_id',
		onupdate="cascade", ondelete="cascade"))
)
driver_comment_table = Table('drivers_comments', metadata,
	Column('driver_id', Integer, ForeignKey('drivers.driver_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
drivermeta_comment_table = Table('drivermeta_comments', metadata,
	Column('drivermeta_id', Integer, ForeignKey('drivermeta.drivermeta_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
driverbuild_description_table = Table('driverbuilds_descriptions', metadata,
	Column('driverbuild_id', Integer, ForeignKey('driverbuilds.driver_id',
		onupdate="cascade", ondelete="cascade")),
	Column('description_id', Integer, ForeignKey('descriptions.description_id',
		onupdate="cascade", ondelete="cascade"))
)
driverbuild_comment_table = Table('driverbuilds_comments', metadata,
	Column('driverbuild_id', Integer, ForeignKey('driverbuilds.driverbuild_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)
driverbuildmeta_comment_table = Table('driverbuildmeta_comments', metadata,
	Column('driverbuildmeta_id', Integer, ForeignKey('driverbuildmeta.driverbuildmeta_id',
		onupdate="cascade", ondelete="cascade")),
	Column('comment_id', Integer, ForeignKey('comments.comment_id',
		onupdate="cascade", ondelete="cascade"))
)

#{ The main model

class State(DeclarativeBase):
	"""
	The state is used to store meta-data about objects, such as whether
	they are currently locked for changes, are being edited, and so on.
	"""

	__tablename__ = 'states'

	#{ Columns

	state_id = Column(Integer, autoincrement=True, primary_key=True)

	date_added = Column(DateTime, default=datetime.now)

	date_modified = Column(DateTime, default=datetime.now)

	active = Column(Boolean(), default=False) # is this object active?

	deleted = Column(Boolean(), default=False) # is this object deleted?

	locked = Column(Boolean(), default=True) # is this object locked?

	creator_id = Column(Integer, ForeignKey('users.user_id'))

	owner_id = Column(Integer, ForeignKey('users.user_id'))

	#{ Relations

	creator = relation('User', primaryjoin="State.creator_id==User.user_id",
				   backref='created_states')

	owner = relation('User', primaryjoin="State.owner_id==User.user_id",
				 backref='owned_states')

	#{ Special methods

	def __init__(self):
		self.creator = User.by_user_name("admin")
		self.owner = User.by_user_name("admin")

class Comment(DeclarativeBase):
	"""
	A comment from a particular user on an object (kernel, driver, etc.)
	"""

	__tablename__ = 'comments'

	#{ Columns

	comment_id = Column(Integer, autoincrement=True, primary_key=True)

	comment = Column(Unicode(255))

	system = Column(Boolean(), default=False) # is it an automatic comment?

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="Comment.state_id==State.state_id",
				  backref='comments')

	# { Special methods

	def __repr__(self):
		return '<Comment: comment=%s>' % self.comment

	def __init__(self, comment=None):
		self.state = State()
		comment=comment

class Description(DeclarativeBase):
	"""
	A description in a locale-specific format.
	"""

	__tablename__ = 'descriptions'

	#{ Columns

	description_id = Column(Integer, autoincrement=True, primary_key=True)

	locale = Column(Unicode(255))

	description = Column(Unicode(255))

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="Description.state_id==State.state_id",
				  backref='descriptions')

	# { Special methods

	def __repr__(self):
		return '<Comment: comment=%s>' % self.comment

	def __init__(self, locale=None, desciption=None):
		self.state = State()
		locale=locale
		description=description

class Arch(DeclarativeBase):
	"""
	An architecture supported by the platform ("i686", "x86_64", etc.)
	"""

	__tablename__ = 'arches'

	#{ Columns

	arch_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), unique=True, nullable=False)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	comments = relation('Comment', secondary=arch_comment_table,
				       backref='arches')

	state = relation('State', primaryjoin="Arch.state_id==State.state_id",
				  backref='arches')

	#{ Special methods

	def __repr__(self):
		return '<Architecture: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_arch_name(cls, name):
		"""Return the arch object whose name is "name"."""
		
		result = DBSession.query(cls).filter(cls.name==name).first()
		if result:
			return result
		else:
			name = Name.by_name(name)
			if not name:
				return None
			arch = name.arches()[0]
			return arch

	@classmethod
	def get_all_arches(cls):
		"""Return a list of all architectures known to the system."""

		arches = DBSession.query(Arch)

		return arches

class License(DeclarativeBase):
	"""
	A software license as used by the driver for a particular device.
	"""

	__tablename__ = 'licenses'

	#{ Columns

	license_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), unique=True, nullable=False)

	free = Column(Boolean(), default=False) # is this a Free license?

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	comments = relation('Comment', secondary=license_comment_table,
				       backref='licenses')

	descriptions = relation('Description', secondary=license_description_table,
					       backref='licenses')

	state = relation('State', primaryjoin="License.state_id==State.state_id",
				  backref='licenses')

	#{ Special methods

	def __repr__(self):
		return '<License: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_license_name(cls, name):
		"""Return the license object whose name is "name"."""
		return DBSession.query(cls).filter(cls.name==name).first()

	@classmethod
	def get_all_licenses(cls):
		"""Return a list of all licenses known to the system."""

		licenses = DBSession.query(License)

		return licenses

class Name(DeclarativeBase):
	"""
	Alternative names used in addition to the standard "name" for an entity.
	"""

	__tablename__ = 'names'

	#{ Columns

	name_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), unique=True, nullable=False)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="Name.state_id==State.state_id",
				  backref='names')

	comments = relation('Comment', secondary=name_comment_table,
				       backref='names')

	#{ Special methods

	def __repr__(self):
		return '<Name: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_name(cls, name):
		"""Return the name object whose name is "name"."""
		return DBSession.query(cls).filter(cls.name==name).first()

	@classmethod
	def get_all_names(cls):
		"""Return a list of all names known to the system."""

		names = DBSession.query(Name)

		return names

class Vendor(DeclarativeBase):
	"""
	Information about a hardware/software vendor (legal name, etc.).
	"""

	__tablename__ = 'vendors'

	vendor_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), nullable=False)

	website = Column(Unicode(255), nullable=False)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="Vendor.state_id==State.state_id",
				  backref='vendors')

	other_names = relation('Name', secondary=vendor_name_table,
				       backref='vendors')

	comments = relation('Comment', secondary=vendor_comment_table,
				       backref='vendors')

	#{ Special methods

	def __repr__(self):
		return '<Vendor: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_vendor_name(cls, name):
		"""Return the vendor object whose name is "name"."""
		
		result = DBSession.query(cls).filter(cls.name==name).first()
		if result:
			return result
		else:
			name = Name.by_name(name)
			if not name:
				return None
			vendor = name.vendors()[0]
			return vendor

	@classmethod
	def get_all_vendors(cls):
		"""Return a list of all vendors known to the system."""

		vendors = DBSession.query(Vendor)

		return vendors

class SystemFamily(DeclarativeBase):
	"""
	A collection of related hardware systems forming an entire family.
	"""

	__tablename__ = 'systemfamilies'

	#{ Columns

	systemfamily_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), nullable=False)

	vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'))

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="SystemFamily.state_id==State.state_id",
				  backref='systemfamilies')

	vendor = relation('Vendor', primaryjoin="SystemFamily.vendor_id==Vendor.vendor_id",
				    backref='systemfamilies')

	other_names = relation('Name', secondary=systemfamily_name_table,
				       backref='systemfamilies')

	comments = relation('Comment', secondary=systemfamily_comment_table,
				       backref='systemfamilies')

	#{ Special methods

	def __repr__(self):
		return '<SystemFamily: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_systemfamily_name(cls, name):
		"""Return the system family object whose name is "name"."""
		return DBSession.query(cls).filter(cls.name==name).first()

	@classmethod
	def get_all_systemfamilies(cls):
		"""Return a list of all systemfamilies known to the system."""

		systemfamilies = DBSession.query(SystemFamily)

		return systemfamilies


class System(DeclarativeBase):
	"""
	A system is a collection of hardware devices from a specific vendor.
	"""

	__tablename__ = 'systems'

	#{ Columns

	system_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), unique=True, nullable=False)

	vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'))

	version = Column(Unicode(255))

	release_date = Column(DateTime, default=datetime.now)

	systemfamily_id = Column(Integer, ForeignKey('systemfamilies.systemfamily_id'))

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="System.state_id==State.state_id",
				  backref='systems')

	vendor = relation('Vendor', primaryjoin="System.vendor_id==Vendor.vendor_id",
				    backref='systems')

	systemfamily = relation('SystemFamily', primaryjoin="System.systemfamily_id==SystemFamily.systemfamily_id",
						backref='systems')

	other_names = relation('Name', secondary=system_name_table,
				       backref='systems')

	comments = relation('Comment', secondary=system_comment_table,
				       backref='systems')

	#{ Special methods

	def __repr__(self):
		return '<System: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_system_name(cls, name):
		"""Return the system object whose name is "name"."""
		
		result = DBSession.query(cls).filter(cls.name==name).first()
		if result:
			return result
		else:
			name = Name.by_name(name)
			if not name:
				return None
			system = name.systems()[0]
			return system

	@classmethod
	def by_system_vendor_and_name(cls, vendor, name):
		"""Return the system object from vendor whose name is "name"."""

		result = DBSession.query(cls).filter(and_(cls.vendor==vendor,cls.name==name)).first()
		if result:
			return result
		else:
			name = Name.by_name(name)
			if not name:
				return None
			for system in name.systems:
				if system.vendor==vendor:
					return system
			return None

	@classmethod
	def get_all_systems(cls):
		"""Return a list of all systems known to the system."""

		systems = DBSession.query(System)

		return systems

class OSFamily(DeclarativeBase):
	"""
	A collection of related Operating Systems (e.g. "Foo Bar Linux").
	"""

	__tablename__ = 'osfamilies'

	osfamily_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), unique=True, nullable=True)

	vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'))

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="OSFamily.state_id==State.state_id",
				  backref='osfamilies')

	vendor = relation('Vendor', primaryjoin="OSFamily.vendor_id==Vendor.vendor_id",
				    backref='osfamilies')

	other_names = relation('Name', secondary=osfamily_name_table,
				       backref='osfamilies')

	comments = relation('Comment', secondary=osfamily_comment_table,
				       backref='osfamilies')

	#{ Special methods

	def __repr__(self):
		return '<OSFamily: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_osfamily_name(cls, name):
		"""Return the osfamily object whose name is "name"."""
		
		result = DBSession.query(cls).filter(cls.name==name).first()
		if result:
			return result
		else:
			name = Name.by_name(name)
			if not name:
				return None
			osfamily = name.osfamilies()[0]
			return osfamily


	@classmethod
	def get_all_osfamilies(cls):
		"""Return a list of all osfamilies known to the system."""

		osfamilies = DBSession.query(OSFamily)

		return osfamilies

class OSRelease(DeclarativeBase):
	"""
	A specific release of an OSFamily (e.g. "Foo Bar Linux 1.0").
	"""

	__tablename__ = 'osreleases'

	osrelease_id = Column(Integer, autoincrement=True, primary_key=True)

	osfamily_id = Column(Integer, ForeignKey('osfamilies.osfamily_id'))

	name = Column(Unicode(255), unique=True, nullable=True)

	version = Column(Unicode(255), unique=False, nullable=True)

	vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'))

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="OSRelease.state_id==State.state_id",
				  backref='osreleases')

	osfamily = relation('OSFamily', primaryjoin="OSRelease.osfamily_id==OSFamily.osfamily_id",
					backref='osreleases')

	other_versions = relation('Name', secondary=osrelease_name_table,
				          backref='osreleases')

	vendor = relation('Vendor', primaryjoin="OSRelease.vendor_id==Vendor.vendor_id",
				    backref='osreleases')

	comments = relation('Comment', secondary=osrelease_comment_table,
				       backref='osreleases')

	#{ Special methods

	def __repr__(self):
		return '<OSRelease: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_osrelease_name(cls, name):
		"""Return the osrelease object whose name is "name"."""

		return DBSession.query(cls).filter(cls.name==name).first()

	@classmethod
	def by_osrelease_osfamily_and_version(cls, osfamily, version):
		"""Return the osrelease object from osfamily whose name is "name"."""

		result = DBSession.query(cls).filter(and_(cls.osfamily==osfamily,cls.version==version)).first()
		if result:
			return result
		else:
			version = Name.by_name(version)
			if not version:
				return None
			for osrelease in version.osreleases:
				if osrelease.osfamily==osfamily:
					return osrelease
			return None

	@classmethod
	def get_all_osreleases(cls):
		"""Return a list of all osreleases known to the system."""

		osreleases = DBSession.query(OSRelease)

		return osreleases

class Kernel(DeclarativeBase):
	"""
	A kernel build for a particular architecture. This includes the
	variant implicitly because each OS handles variants differently
	(so there are simply multiple kernel entries to cover variants).
	"""

	__tablename__ = 'kernels'

	#{ Columns

	kernel_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), unique=True, nullable=False)

	arch_id = Column(Integer, ForeignKey('arches.arch_id'))

	osrelease_id = Column(Integer, ForeignKey('osreleases.osrelease_id'))

	vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'))

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="Kernel.state_id==State.state_id",
				  backref='kernels')

	arch = relation('Arch', primaryjoin="Kernel.arch_id==Arch.arch_id",
				backref='kernels')

	osrelease = relation('OSRelease', primaryjoin="Kernel.osrelease_id==OSRelease.osrelease_id",
					  backref='kernels')

	drivers = relation('Driver', secondary=kernel_driver_table,
				     backref='kernels')

	vendor = relation('Vendor', primaryjoin="Kernel.vendor_id==Vendor.vendor_id",
				    backref='kernels')

	comments = relation('Comment', secondary=kernel_comment_table,
				       backref='kernels')

	#{ Special methods

	def __repr__(self):
		return '<Kernel: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_kernel_name(cls, name):
		"""Return the kernel object whose name is "name"."""
		return DBSession.query(cls).filter(cls.name==name).first()

	@classmethod
	def by_kernel_osrelease_arch_and_name(cls, osrelease, arch, name):
		"""Return the kernel object from osrelease for arch whose name is "name"."""

		result = DBSession.query(cls).filter(and_(cls.osrelease==osrelease,and_(cls.arch==arch,cls.name==name))).first()
		if result:
			return result
		else:
			name = Name.by_name(name)
			if not name:
				return None
			for kernel in name.kernels:
				if kernel.osrelease==osrelease and kernel.arch==arch:
					return kernel
			return None

	@classmethod
	def get_all_kernels(cls):
		"""Return a list of all kernels known to the system."""

		kernels = DBSession.query(Kernel)

		return kernels

class DeviceType(DeclarativeBase):
	"""
	A type of hardware device classification (e.g. "Audio", "Video")
	"""

	__tablename__ = 'devicetypes'

	#{ Columns

	devicetype_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), unique=True, nullable=False)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="DeviceType.state_id==State.state_id",
				  backref='devicetypes')

	comments = relation('Comment', secondary=devicetype_comment_table,
				       backref='devicetypes')

	#{ Special methods

	def __repr__(self):
		return '<DeviceType: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_devicetype_name(cls, name):
		"""Return the devicetype object whose name is "name"."""
		return DBSession.query(cls).filter(cls.name==name).first()

	@classmethod
	def get_all_devicetypes(cls):
		"""Return a list of all devicetypes known to the system."""

		devicetypes = DBSession.query(DeviceType)

		return devicetypes

class Device(DeclarativeBase):
	"""
	A device is a piece of hardware for which we may have a driver.
	"""

	__tablename__ = 'devices'

	#{ Columns

	device_id = Column(Integer, autoincrement=True, primary_key=True)

	devicetype_id = Column(Integer, ForeignKey('devicetypes.devicetype_id'))

	vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'))

	name = Column(Unicode(255), unique=True, nullable=False)

	version = Column(Unicode(255), unique=True, nullable=False)

	release_date = Column(DateTime, default=datetime.now)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="Device.state_id==State.state_id",
				  backref='devices')

	other_names = relation('Name', secondary=device_name_table,
				       backref='devices')

	devicetype = relation('DeviceType', primaryjoin="Device.devicetype_id==DeviceType.devicetype_id",
					    backref='devices')

	vendor = relation('Vendor', primaryjoin="Device.vendor_id==Vendor.vendor_id",
				    backref='devices')

	drivers = relation('Driver', secondary=device_driver_table,
				     backref='devices')

	systems = relation('System', secondary=device_system_table,
				     backref='devices')

	comments = relation('Comment', secondary=device_comment_table,
				       backref='devices')

	#{ Special methods

	def __repr__(self):
		return '<Device: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_device_id(cls, id):
		"""Return the device object whose id is "id"."""
		return DBSession.query(cls).filter(cls.device_id==id).first()

	@classmethod
	def by_device_name(cls, name):
		"""Return the device object whose name is "name"."""
		return DBSession.query(cls).filter(cls.name==name).first()

	@classmethod
	def get_all_devices(cls):
		"""Return a list of all devices known to the system."""

		devices = DBSession.query(Device)

		return devices

class DeviceAlias(DeclarativeBase):
	"""
	A devicealias is a standardized hardware alias used by an OS.
	"""

	__tablename__ = 'devicealiases'

	#{ Columns

	devicealias_id = Column(Integer, autoincrement=True, primary_key=True)

	device_id = Column(Integer, ForeignKey('devices.device_id'))

	alias = Column(Unicode(255), unique=False)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="DeviceAlias.state_id==State.state_id",
				  backref='devicealises')

	device = relation('Device', primaryjoin="DeviceAlias.device_id==Device.device_id",
				    backref='devicealiases')

	comments = relation('Comment', secondary=devicealias_comment_table,
				       backref='devicealises')

	#{ Special methods

	def __repr__(self):
		return '<DeviceAlias: alias=%s>' % self.alias

	def __init__(self):
		self.state= State()

	#{ Getters and setters

	@classmethod
	def by_devicealias(cls, alias):
		"""Return the devicealias object whose alias is "alias"."""
		return DBSession.query(cls).filter(cls.alias==alias).first()

	@classmethod
	def get_all_devicealiases(cls):
		"""Return a list of all devicealiases known to the system."""

		devicealiases = DBSession.query(DeviceAlias)

		return devicealiases

class DriverType(DeclarativeBase):
	"""
	A type of driver (for example, a "kernel driver").
	"""

	__tablename__ = 'drivertypes'

	#{ Columns

	drivertype_id = Column(Integer, autoincrement=True, primary_key=True)

	name = Column(Unicode(255), unique=True, nullable=False)

	prefix = Column(Unicode(255), unique=True, nullable=True)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="DriverType.state_id==State.state_id",
				  backref='drivertypes')

	comments = relation('Comment', secondary=drivertype_comment_table,
				       backref='drivertypes')

	#{ Special methods

	def __repr__(self):
		return '<DriverType: type=%s>' % self.type

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_drivertype_name(cls, name):
		"""Return the drivertype object whose type is "type"."""
		return DBSession.query(cls).filter(cls.name==name).first()

	@classmethod
	def get_all_drivertypes(cls):
		"""Return a list of drivertypes known to the system."""

		drivertypes = DBSession.query(DriverType)

		return drivertypes

class Driver(DeclarativeBase):
	"""
	A driver providing support for a particular device.
	"""

	__tablename__ = 'drivers'

	#{ Columns

	driver_id = Column(Integer, autoincrement=True, primary_key=True)

	drivertype_id = Column(Integer, ForeignKey('drivertypes.drivertype_id'))

	license_id = Column(Integer, ForeignKey('licenses.license_id'))

	vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'))

	name = Column(Unicode(255), nullable=False)

	version = Column(Unicode(255))

	release_date = Column(DateTime, default=datetime.now)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	drivertype = relation('DriverType', primaryjoin="Driver.drivertype_id==DriverType.drivertype_id",
					    backref='drivers')

	license = relation('License', primaryjoin="Driver.license_id==License.license_id",
				      backref='drivers')

	vendor = relation('Vendor', primaryjoin="Driver.vendor_id==Vendor.vendor_id",
				    backref='drivers')

	descriptions = relation('Description', secondary=driver_description_table,
					       backref='drivers')

	comments = relation('Comment', secondary=driver_comment_table,
				       backref='drivers')

	state = relation('State', primaryjoin="Driver.state_id==State.state_id")

	#{ Special methods

	def __repr__(self):
		return '<Driver: name=%s>' % self.name

	def __init__(self):
		self.state = State()

	#{ Getters and setters

	@classmethod
	def by_driver_id(cls, id):
		"""Return the driver object whose is is "id"."""
		return DBSession.query(cls).filter(cls.driver_id==id).first()

	@classmethod
	def by_driver_name(cls, name):
		"""Return the driver object whose name is "name"."""
		return DBSession.query(cls).filter(cls.name==name).first()

	@classmethod
	def get_all_drivers(cls):
		"""Return a list of all drivers known to the system."""

		drivers = DBSession.query(Driver)

		return drivers

class DriverMeta(DeclarativeBase):
	"""
	Meta-data about a driver (key/value pairs, for example "kernel_module".
	"""

	__tablename__ = 'drivermeta'

	#{ Columns

	drivermeta_id = Column(Integer, autoincrement=True, primary_key=True)

	driver_id = Column(Integer, ForeignKey('drivers.driver_id'))

	tag = Column(Unicode(255), nullable=False)

	value = Column(Unicode(255), nullable=False)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="DriverMeta.state_id==State.state_id",
				  backref='drivermeta')

	driver = relation('Driver', primaryjoin="DriverMeta.driver_id==Driver.driver_id",
				    backref='drivermeta')

	comments = relation('Comment', secondary=drivermeta_comment_table,
				       backref='drivermeta')

	#{ Special methods

	def __repr__(self):
		return '<DriverMeta: name=%s>' % self.name

	def __init__(self):
		self.state = State()

class DriverBuild(DeclarativeBase):
	"""
	A build of a driver for a specific kernel (on a given arch/variant).
	"""

	__tablename__ = 'driverbuilds'

	#{ Columns

	driverbuild_id = Column(Integer, autoincrement=True, primary_key=True)

	driver_id = Column(Integer, ForeignKey('drivers.driver_id'))

	kernel_id = Column(Integer, ForeignKey('kernels.kernel_id'))

	vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'))

	version = Column(Unicode(255))

	release_date = Column(DateTime, default=datetime.now)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="DriverBuild.state_id==State.state_id",
				  backref='driverbuilds')

	driver = relation('Driver', primaryjoin="DriverBuild.driver_id==Driver.driver_id",
				    backref='driverbuilds')

	kernel = relation('Kernel', primaryjoin="DriverBuild.kernel_id==Kernel.kernel_id",
				    backref='driverbuilds')

	vendor = relation('Vendor', primaryjoin="DriverBuild.vendor_id==Vendor.vendor_id",
				    backref='driverbuilds')

	descriptions = relation('Description', secondary=driverbuild_description_table,
					       backref='driverbuilds')

	comments = relation('Comment', secondary=driverbuild_comment_table,
				        backref='driverbuilds')

	#{ Getters and setters

	@classmethod
	def by_driverbuild_id(cls, id):
		"""Return the driverbuild object whose id is "id"."""
		return DBSession.query(cls).filter(cls.driverbuild_id==id).first()

	#{ Special methods

	def __repr__(self):
		return '<DriverBuild: version=%s>' % self.version

	def __init__(self):
		self.state = State()

class DriverBuildMeta(DeclarativeBase):
	"""
	Meta-data about a driver build (key/value pairs, for example "kernel_module".
	"""

	__tablename__ = 'driverbuildmeta'

	#{ Columns

	driverbuildmeta_id = Column(Integer, autoincrement=True, primary_key=True)

	driverbuild_id = Column(Integer, ForeignKey('driverbuilds.driverbuild_id'))

	tag = Column(Unicode(255), nullable=False)

	value = Column(Unicode(255), nullable=False)

	state_id = Column(Integer, ForeignKey('states.state_id'))

	#{ Relations

	state = relation('State', primaryjoin="DriverBuildMeta.state_id==State.state_id",
				  backref='driverbuildmeta')

	driverbuild = relation('DriverBuild', primaryjoin="DriverBuildMeta.driverbuild_id==DriverBuild.driverbuild_id",
				    backref='driverbuildmeta')

	comments = relation('Comment', secondary=driverbuildmeta_comment_table,
				       backref='driverbuildmeta')

	#{ Special methods

	def __repr__(self):
		return '<DriverBuildMeta: name=%s>' % self.name

	def __init__(self):
		self.state = State()

