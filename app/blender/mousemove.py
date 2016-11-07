################################################
#
#	MouseMove (v2.7)
#	 a Mouselook and Movement Script
#	  by Riyuzakisan (3/19/2013)
#	  Tested in Blender 2.66.1 (r55075:55077)
#
#  Contact:
#   Email:		riyuzakisan@gmail.com
#   Website:	riyuzakisan.weebly.com
#
#  Released under the Creative Commons
#  Attribution 3.0 Unported License
#
#  If you use this script/code, please include
#  this information header.
#
#  For more information, please check the Instruction
#  Manual included with this script file.
#
################################################


################################################
#  Do NOT remove any properties in the CONFIG
#  variable below.
#
#  See the Instruction Manual section on
#  Config Properties for more information.
################################################

# Print debug messages in the console
DEBUG_MESSAGES = True

CONFIG = """
# MouseMove Core Properties
mmc{
	### Enable/Disable Base Features ###
	(bool) mouselook = true
	(bool) static = false
	(bool) dynamic = false
	
	### Left handed layout ###
	(bool) lefthanded = false
	
	### Display Mouse Cursor ###
	(bool) cursor = none
	
	# Set to "none" to avoid interfering with
	# other scripts that render the cursor
}

# Mouselook Properties
ml{
	### Basic Properties ###
	(num) sensitivity = 2
	(bool) invert = false
	(bool) inherit = true
	
	# inherit: parent object inherits left/right rotation
	
	### Up/Down Rotation Cap ###
	(bool) cap = false
	(num) capupper = 80
	(num) caplower = -80
	(num) caporigin = 90
	
	# caporigin: the forward facing rotation of the object
	# 	on the X axis, in degrees.
}

# Static Movement Properties
sm{
	### Basic Properties ###
	(num) speed = 0.1
	(bool) cameramode = true
	
	# speed: uses Blender units
	# cameramode:
	#	-True: -Z is forward axis for movement
	# 	-False: +Y is forward axis for movement
}

# Dynamic Movement Properties
dm{
	### Basic Properties ###
	(num) speed = 8
	(num) runspeed = 16
	(num) jumpspeed = 10
	
	### Extra Settings ###
	(num) movemidair = 0.005
	(bool) fly = false
	
	# movemidair: How much the player can move mid-air
	#	Set value on a scale of 0.0 to 1.0
	
	### Ground Detection Distance ###
	(num) collisionrange = 2
}
"""

from bge import logic, render, events
from mathutils import Vector
import math

# MouseMove Core
class Core:
	def __init__(self, object):
		self.own = object
		self.cont = None
		
		if isCont(object):
			self.cont = object
			self.own = object.owner
		
		self.features = {}
		
		cfg = self.getConfig()
		self.config = cfg[0]
		self.configTypes = cfg[1]
		
		self.props = self.getProperties('mmc')
		self.controls = Controls(self)
	
	def module(self):
		self.main()
		
		### Mouselook System ###
		if self.props['mouselook']:
			if not self.features.get('mouselook', None):
				self.addMouselook()
			
		### Staticmove System ###
		if self.props['static']:
			if not self.features.get('static', None):
				self.addStatic()
			
		### Dynamicmove System ###
		if self.props['dynamic'] and not self.props['static']:
			if not self.features.get('dynamic', None):
				if self.own.parent:
					self.addDynamic(self.cont)
	
	def main(self):
		# Refresh properties
		self.props = self.getProperties('mmc')
		self.controls.main()
		
		cursor = self.props['cursor']
		if cursor in [True, False]:
			render.showMouse(cursor)
		
		for i in self.features:
			if self.props[i] == True:
				self.features[i].main()
			elif self.features[i].ready == True:
				self.features[i].deactivate()
	
	def create(self, key, object):
		features = {'mouselook':Mouselook, 'static':StaticMove, 'dynamic':DynamicMove}
		
		if key in self.features:
			msg('Core Feature "', key, '" already created! Returning None')
			return None
		
		newFeature = features[key](self, object)
		self.features[key] = newFeature
		
		return newFeature
		
	def addMouselook(self, object=None):
		self.setProp('mmc.mouselook', True)
		return self.create('mouselook', object)
		
	def addStatic(self, object=None):
		self.setProp('mmc.static', True)
		return self.create('static', object)
		
	def addDynamic(self, object=None):
		self.setProp('mmc.dynamic', True)
		return self.create('dynamic', object)
	
	# Decode CONFIG properties
	def getConfig(self):
		props = {'mmc':{},
				 'ml':{},
				 'sm':{},
				 'dm':{}
				}
		dTypes = {'mmc':{},
				 'ml':{},
				 'sm':{},
				 'dm':{}
				}
				 
		key = None
		
		for i in CONFIG.splitlines():
			i = i.strip()
			i = i.replace('\t', '')
			
			fullLine = i
			
			if '{' in i:
				i = i.split('{')[0].lower().strip()
				if '#' not in i:
					key = i
					props[key] = {}
					dTypes[key] = {}
			elif i.startswith('}'):
				key = None
			elif i.startswith('#'):
				continue
			else:
				if key != None and i != '':
					i = i.split('#', 1)[0].strip() # Remove trailing comments
					
					dataType = None
					if i.startswith('(') and ')' in i:
						dataType = i[1:].split(')', 1)[0].strip().lower() # Extract data type
					
					if dataType == None:
						msg('Config: Property missing Data Type; "', fullLine, '"')
						continue
					
					i = i.split(')', 1)[1]
					
					if '=' not in i:
						msg('Config: Undefined Property; "', fullLine, '"')
						continue
					
					# Property names are all stored in lower case
					propName = i.split('=', 1)[0].strip().lower()
					propValue = i.split('=', 1)[1].strip()
					
					# Remove trailing comments
					propValue = propValue.split('#', 1)[0].strip()
					
					if propValue == '':
						msg('Config: Empty Property; "', fullLine, '"')
						continue
					
					# Convert Properties to data types
					if dataType == 'bool':
						if propValue.lower() in ['true', '1']:
							propValue = True
						elif propValue.lower() in ['false', '0']:
							propValue = False
						elif propValue.lower() == 'none':
							propValue = None
						else:
							msg('Config: Property doesn\'t match Data Type; "', fullLine, '"')
							continue
						nonetype = None
						dataType = [bool().__class__, int().__class__, nonetype.__class__]
					elif dataType == 'int':
						try:
							propValue = int(propValue)
							dataType = [int().__class__]
						except:
							msg('Config: Property doesn\'t match Data Type; "', fullLine, '"')
							continue
					elif dataType in ['float', 'num']:
						try:
							propValue = float(propValue)
							dataType = [float().__class__, int().__class__]
						except:
							msg('Config: Property doesn\'t match Data Type; "', fullLine, '"')
							continue
					elif dataType == 'str':
						dataType = [str().__class__]
					else:
						msg('Config: Invalid Data Type; "', fullLine, '"')
						continue
					
					props[key][propName] = propValue
					dTypes[key][propName] = dataType
					
		return [props, dTypes]
	
	# Get Properties
	def getProperties(self, prefix):
		props = {}
		objProps = {}
		
		# Organize properties and remove prefixes
		for i in self.own.getPropertyNames():
			if i.lower().startswith(prefix + '.'):
				objProps[i.lower()[len(prefix)+1:]] = self.own[i]
		
		for i in self.config[prefix]:
			props[i] = self.config[prefix][i]
			types = self.configTypes[prefix][i]
			
			if i in objProps and objProps[i].__class__ in types:
				props[i] = objProps[i]
		
		return props
	
	# Set Property
	def setProp(self, propName, value=None):
		propName = propName.lower()
		prefix = propName.split('.', 1)[0]
		suffix = propName.split('.', 1)[1]
		
		if suffix in self.config[prefix]:
			for i in self.own.getPropertyNames():
				if i.lower() == propName:
					if value == None and self.own[i] in [True, False]:
						self.own[i] = not self.own[i]
					elif value.__class__ in self.configTypes[prefix][suffix]:
						self.own[i] = value
					return
			
			if value.__class__ in self.getTypes(propName):
				self.own[propName] = value
	
	# Get Property
	def getProp(self, propName):
		propName = propName.lower()
		prefix = propName.split('.', 1)[0]
		suffix = propName.split('.', 1)[1]
		
		if suffix in self.config[prefix]:
			if suffix in self.config[prefix]:
				return self.config[prefix][suffix]
		
		return None
			
	def getTypes(self, propName):
		prefix = propName.split('.', 1)[0]
		suffix = propName.split('.', 1)[1]
		
		if suffix in self.configTypes[prefix]:
			return self.configTypes[prefix][suffix]
		
		
class Mouselook:
	def __init__(self, core, object=None):
		self.core = core
		
		if object == None:
			object = self.core.own
				
		if isCont(object):
			object = object.owner
			
		self.own = object

		self.props = self.core.getProperties('ml')
		self.ready = False
		
		# Mouselook Attributes
		self.size = self.getWindowSize()
		self.move = self.getMovement()
		self.verticalRotation = self.own.localOrientation.to_euler().x * (180 / math.pi)
		
	def main(self):
		self.props = self.core.getProperties('ml')
		self.size = self.getWindowSize()
		self.move = self.getMovement()
		
		if self.ready:
			self.run()
		else:
			self.activate()
		
	def run(self):
		invert = -1 if self.props['invert'] else 1
		sensitivity = self.props['sensitivity'] * 0.025
		
		horizontal = self.move[0] * sensitivity * invert
		vertical = self.move[1] * sensitivity * invert
		
		### Set vertical rotation (X) and apply capping ###
		self.verticalRotation += vertical
		self.applyCap()
		
		ori = self.own.localOrientation.to_euler()
		ori.x = self.verticalRotation / (180 / math.pi)
		
		if (self.props['inherit'] == False) or (self.own.parent == None):
			ori.z += horizontal / (180 / math.pi)
			
		elif self.props['inherit'] and self.own.parent:
			parentOri = self.own.parent.localOrientation.to_euler()
			parentOri.z += horizontal / (180 / math.pi)
			self.own.parent.localOrientation = parentOri.to_matrix()
		
		self.own.localOrientation = ori.to_matrix()
		
		self.setCenter()
		
	### "Get Property" Functions ###
	def getWindowSize(self):
		return (render.getWindowWidth(), render.getWindowHeight())
		
	def getMovement(self):
		pos = logic.mouse.position
		realCenter = self.getCenter()
		move = [realCenter[0] - pos[0], realCenter[1] - pos[1]]
		
		xMove = int(self.size[0] * move[0])
		yMove = int(self.size[1] * move[1])
		
		return (xMove, yMove)
		
	def getCenter(self):
		size = self.getWindowSize()
		screenCenter = (size[0]//2, size[1]//2)
		
		return (screenCenter[0] * (1.0/size[0]), screenCenter[1] * (1.0/size[1]))
		
	def setCenter(self):
		render.setMousePosition(self.size[0]//2, self.size[1]//2)
	
	def applyCap(self):
		if self.props['cap']:
			upper = self.props['capupper']
			lower = self.props['caplower']
			origin = self.props['caporigin']
			
			if upper < lower:
				return
			
			if self.verticalRotation > origin + upper:
				self.verticalRotation = origin + upper
				
			elif self.verticalRotation < origin + lower:
				self.verticalRotation = origin + lower
	
	### Activation/Deactivation ###
	def activate(self):
		self.setCenter()
		self.ready = True
		
	def deactivate(self):
		self.ready = False

	
class StaticMove:
	def __init__(self, core, object=None):
		self.core = core
		
		if object == None:
			object = self.core.own
				
		if isCont(object):
			object = object.owner
			
		self.own = object
		
		self.props = self.core.getProperties('sm')
		
		self.ready = False
		
	def main(self):
		if self.ready:
			if self.own.parent == None:
				self.run()
		else:
			self.activate()
		
	def run(self):
		controls = self.core.controls
		
		speed = self.props['speed']
		camera = self.props['cameramode']
		
		if controls.run:
			speed *= 4
		
		forward = speed * (controls.forward - controls.back)
		side = speed * (controls.right - controls.left)
		fly = speed * ((controls.jump or controls.up) - (controls.crouch or controls.down))
		
		if camera:
			move = Vector((side, 0, -forward))
		else:
			move = Vector((side, forward, 0))
		
		self.own.applyMovement(move, True) # local
		self.own.applyMovement([0, 0, fly], False) # global
	
	### Activation/Deactivation ###
	def activate(self):
		self.ready = True
		
	def deactivate(self):
		self.ready = False
	
	
class DynamicMove:
	def __init__(self, core, object=None):
		self.core = core
		
		self.cont = None
		if object == None:
			object = self.core.own
			if self.core.cont:
				self.cont = self.core.cont
				
		if isCont(object):
			self.cont = object
			if self.cont.owner.parent == None:
				self.core.setProp('mmc.dynamic', False)
				msg('Invalid Dynamic Object')
				return
				
			object = self.cont.owner.parent
		
		self.own = object
			
		self.props = self.core.getProperties('dm')
		
		self.ready = False
		
		self.keyboardTimer = 120
		self.zPos = 0.0
		
		self.colSen = None
		self.raySen = None
		self.keySen = None
		
		objects = [self.own]
		
		if self.cont:
			if self.cont.owner not in objects:
				objects.append(self.cont.owner)
		
		# Get both Collision and Ray sensors
		for obj in objects:
			for s in obj.sensors:
				if str(s.__class__) == "<class 'KX_TouchSensor'>":
					self.colSen = s
				elif str(s.__class__) == "<class 'KX_RaySensor'>":
					if s.range <= 0.010 and s.axis == 0:
						self.raySen = s
				elif str(s.__class__) == "<class 'SCA_KeyboardSensor'>":
					if s.key == 0 and s.useAllKeys == True:
						self.keySen = s
		
			if not (self.colSen and self.raySen):
				self.colSen = None
				self.raySen = None
		
		self.run_state = self.state_onGround
		
	def main(self):
		self.props = self.core.getProperties('dm')
		
		if self.ready:
			self.run()
		else:
			self.activate()
		
	def run(self):
		### Speed Properties ###
		self.speed = self.props['speed']
		self.runspeed = self.props['runspeed']
		self.jumpspeed = self.props['jumpspeed']
		self.damping = 0.1
		
		self.fly = self.props['fly']
		self.midair = self.props['movemidair']
		
		if self.midair > 1:
			self.midair = 1
		elif self.midair < 0:
			self.midair = 0
		
		self.finalVelocity = [0, 0, 0]
		
		### Sensor Management ###
		self.col = False
		self.ray = False
		
		if self.raySen == None or self.colSen == None:
			self.fly = True
		
		if self.raySen != None:
			self.raySen.range = self.props['collisionrange']
			self.raySen.axis = 5 #-Z axis (down)
			
			if self.raySen.positive:
				self.ray = True
		
		if self.colSen != None:
			if self.colSen.positive:
				self.col = True
		
		### Keyboard Activity Timer ###
		if self.keySen != None:
			if self.keySen.positive:
				self.keyboardTimer = 120
				self.keySen.useNegPulseMode = True
			elif self.keyboardTimer > 0:
				self.keyboardTimer -= 1
			
			if self.keyboardTimer <= 0:
				self.keySen.useNegPulseMode = False
		
		### Run State ###
		self.run_state()
		
	def state_onGround(self):
		controls = self.core.controls
		
		### Adjust Speed and Damping ###
		if controls.crouch:
			self.speed *= 0.3
			self.damping = 0.85
		else:
			if controls.run and (controls.forward and not controls.back):
				self.speed = self.runspeed
				self.damping = 0.18
				
			if controls.jump and self.ray:
				self.finalVelocity[2] = self.jumpspeed
				self.run_state = self.state_inAir
			
		if not self.col:
			self.run_state = self.state_inAir
		
		### Apply ###
		self.assignVelocity()
		self.applyMovement()
		self.limitVelocity()
		self.applyDamping()
		
	def state_inAir(self):
		controls = self.core.controls
		
		if self.fly:
			if controls.jump:
				self.finalVelocity[2] = 1
			if controls.run and (controls.forward and not controls.back):
				self.speed *= 2
				self.damping = 0.1
		
		### Assign Velocity ###
		self.assignVelocity()
		
		if not self.fly:
			self.finalVelocity[0] *= self.midair
			self.finalVelocity[1] *= self.midair
		
		if self.col and self.own.worldLinearVelocity[2] <= 1:
			self.run_state = self.state_onGround
		
		### Apply Movement ###
		self.applyMovement()
		
		### Custom Velocity ###
		self.own.applyForce([0, 0, -30], False) #global force
		
		if self.fly:
			if controls.crouch == 1:
				self.zPos = self.own.worldPosition[2]
			elif controls.crouch == 2:
				self.own.worldPosition[2] = self.zPos
				self.own.worldLinearVelocity[2] = 0
			
			### Apply Damping ###
			self.applyDamping()
		
	def assignVelocity(self):
		controls = self.core.controls
		
		forwardMove = self.speed * (controls.forward - controls.back)
		sideMove = self.speed * (controls.right - controls.left)
		
		if forwardMove and sideMove:
			forwardMove *= 0.70710678
			sideMove *= 0.70710678
		
		self.finalVelocity[1] = forwardMove
		self.finalVelocity[0] = sideMove
		
	def applyMovement(self):
		### Apply Movement ###
		self.own.localLinearVelocity += Vector(self.finalVelocity)
	
	def limitVelocity(self):
		### Limit Velocity ###
		index = 0
		for i in self.own.localLinearVelocity:
			if index != 2:
				if i > self.speed:
					i = self.speed
				if i < -self.speed:
					i = -self.speed
			
			self.own.localLinearVelocity[index] = i
			index += 1
	
	def applyDamping(self):
		controls = self.core.controls
		
		if not controls.forward and not controls.back:
			self.own.localLinearVelocity[1] -= self.own.localLinearVelocity[1] * self.damping
		if not controls.left and not controls.right:
			self.own.localLinearVelocity[0] -= self.own.localLinearVelocity[0] * self.damping
	
	### Activation/Deactivation ###
	def activate(self):
		self.ready = True
		
	def deactivate(self):
		self.ready = False


class Controls:
	def __init__(self, core):
		self.core = core
		self.main()
		
	def main(self):
		key = logic.keyboard.events
		self.jump = key[events.SPACEKEY]
		
		lefthanded = self.core.props['lefthanded']
		
		if lefthanded:
			self.layout = self.layout_left
		else:
			self.layout = self.layout_right
		
		self.layout()
		
	def layout_right(self):
		key = logic.keyboard.events
		
		self.forward = key[events.WKEY]
		self.back = key[events.SKEY]
		self.left = key[events.AKEY]
		self.right = key[events.DKEY]
		
		self.up = key[events.EKEY]
		self.down = key[events.QKEY]
		
		self.crouch = key[events.LEFTCTRLKEY]
		self.run = key[events.LEFTSHIFTKEY]
		
	def layout_left(self):
		key = logic.keyboard.events
		
		self.forward = key[events.IKEY]
		self.back = key[events.KKEY]
		self.left = key[events.JKEY]
		self.right = key[events.LKEY]
		
		self.up = key[events.UKEY]
		self.down = key[events.OKEY]
		
		self.crouch = key[events.RIGHTCTRLKEY]
		self.run = key[events.RIGHTSHIFTKEY]
		
		
def isCont(object):
	if str(object.__class__) == "<class 'SCA_PythonController'>":
		return True
	return False

def msg(*args):
	message = ""
	for i in args:
		message += str(i)
		
	if DEBUG_MESSAGES:
		print('[MouseMove] ' + message)
	
#################################

# Module Execution entry point
def main():
	cont = logic.getCurrentController()
	own = cont.owner
	
	if 'mmc.core' not in own:
		own['mmc.core'] = Core(cont)
	else:
		own['mmc.core'].module()
	
# Non-Module Execution entry point (Script)
if logic.getCurrentController().mode == 0:
	main()