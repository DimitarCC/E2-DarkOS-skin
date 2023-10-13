from enigma import ePixmap
from Components.Renderer.Renderer import Renderer
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_GUISKIN, resolveFilename

try:
	from SystemInfo import BoxInfo
	model = BoxInfo.getItem("model")
except:
	from Tools.HardwareInfo import HardwareInfo
	model = HardwareInfo().get_device_model()


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
			pngname = resolveFilename(SCOPE_GUISKIN, "icons/logos/" + self.getLogoPngName() + ".svg")
			is_svg = pngname.endswith(".svg")
			png = LoadPixmap(pngname, width=self.instance.size().width(), height=0 if is_svg else self.instance.size().height())
			if png != None:
				self.instance.setPixmap(png)
			else:
				defaultLogo = self.getDefaultLogo()
				if defaultLogo != None:
					self.instance.setPixmap(defaultLogo)

	def getDefaultLogo(self):
		if self.logoType == "model":
			defaultPngName = resolveFilename(SCOPE_GUISKIN, "icons/logos/deflogo.svg")
		else:
			defaultPngName = resolveFilename(SCOPE_GUISKIN, "icons/logos/deflogo-small.svg")

		is_svg = defaultPngName.endswith(".svg")
		return LoadPixmap(defaultPngName, width=self.instance.size().width(), height=0 if is_svg else self.instance.size().height())
	
	def getLogoPngName(self):
		logoname = ""
		if self.logoType == "model":
			return model
		elif self.logoType == "brand":
			if model in ("vuzero4k", "vusolo4k", "vuuno4kse", "vuduo4k", "vuduo4kse", "vuultimo4k"):
				logoname = "vulogo"
		return logoname
	