from enigma import ePixmap
from Components.Renderer.Renderer import Renderer
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_GUISKIN, resolveFilename

try:
	from Components.SystemInfo import BoxInfo
	model = BoxInfo.getItem("model")
except:
	from Tools.HardwareInfo import HardwareInfo
	model = HardwareInfo().get_device_model()


def getLogoPngName(logoType):
		logoname = ""
		if logoType == "model":
			return model or ""
		elif logoType == "brand":
			if model and model in ("vusolo", "vuduo", "vuuno", "vuzero", "vusolo2", "vusolose", "vuduo2",  "vuultimo", "vuzero4k", "vusolo4k", "vuuno4k", "vuuno4kse", "vuduo4k", "vuduo4kse", "vuultimo4k"):
				logoname = "vulogo"
			elif model and model in ("dagsmv200"):
				logoname = "qviartlogo"
			elif model and model in ("sf8008", "sf8008m", "sx988", "sx88v2", "sfx6008", "sfx6018"):
				logoname = "octagonlogo"
			elif model and model in ("pulse4k", "pulse4kmini"):
				logoname = "pulselogo"
			elif model and model in ("gbmv200"):
				logoname = "gigabluelogo"

		return logoname

def getDefaultLogo(logoType, width, height):
		if logoType == "model":
			defaultPngName = resolveFilename(SCOPE_GUISKIN, "icons/logos/deflogo.svg")
		else:
			defaultPngName = resolveFilename(SCOPE_GUISKIN, "icons/logos/deflogo-small.svg")

		is_svg = defaultPngName.endswith(".svg")
		return LoadPixmap(defaultPngName, width=width, height=0 if is_svg else height)

def setLogo(px, logoType, width, height):
	pngname = resolveFilename(SCOPE_GUISKIN, "icons/logos/" + getLogoPngName(logoType) + ".svg")
	is_svg = pngname.endswith(".svg")
	png = LoadPixmap(pngname, width=width, height=0 if is_svg else height)
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
	