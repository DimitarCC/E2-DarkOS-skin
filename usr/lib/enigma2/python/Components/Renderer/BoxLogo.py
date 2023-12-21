from enigma import ePixmap
from Components.Renderer.Renderer import Renderer
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_GUISKIN, resolveFilename, fileExists

def getLogoPngPath(logoType):
	if logoType == "model":
		if fileExists("/usr/share/enigma2/boxlogo.svg"):
			return "/usr/share/enigma2/boxlogo.svg"
		elif fileExists("/usr/share/enigma2/distrologo.svg"):
			return "/usr/share/enigma2/distrologo.svg"
		else:
			return ""
	elif logoType == "brand" and fileExists("/usr/share/enigma2/brandlogo.svg"):
		return "/usr/share/enigma2/brandlogo.svg"
	elif logoType == "distro" and fileExists("/usr/share/enigma2/distrologo.svg"):
		return "/usr/share/enigma2/distrologo.svg"

	return ""

def getDefaultLogo(logoType, width, height):
		if logoType == "model":
			defaultPngName = resolveFilename(SCOPE_GUISKIN, "icons/logos/boxlogo.svg")
		elif logoType == "brand":
			defaultPngName = resolveFilename(SCOPE_GUISKIN, "icons/logos/brandlogo.svg")
		else:
			defaultPngName = resolveFilename(SCOPE_GUISKIN, "icons/logos/boxlogo.svg")

		is_svg = defaultPngName and defaultPngName.endswith(".svg")
		return LoadPixmap(defaultPngName, width=width, height=0 if is_svg else height)

def setLogo(px, logoType, width, height):
	pngname = getLogoPngPath(logoType)
	is_svg = pngname and pngname.endswith(".svg")
	png = pngname and LoadPixmap(pngname, width=width, height=0 if is_svg else height)
	if png != None:
		px.setPixmap(png)
	else:
		defaultLogo = getDefaultLogo(logoType, width, height)
		if defaultLogo != None:
			px.setPixmap(defaultLogo)


class BoxLogo(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.logoType = "model"
		
	GUI_WIDGET = ePixmap

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for (attrib, value) in self.skinAttributes:
			if attrib == "logoType":
				self.logoType = value
				attribs.remove((attrib, value))
				break
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def changed(self, what):
		pass
				
	def onShow(self):
		if self.instance:
			setLogo(self.instance, self.logoType, self.instance.size().width(), self.instance.size().height())
	