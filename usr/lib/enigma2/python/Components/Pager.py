from Components.GUIComponent import GUIComponent
from skin import parseColor, parseFont, parseScale

from enigma import eListbox, gFont, eListboxPythonMultiContent, RT_WRAP, RT_VALIGN_TOP, RT_VALIGN_CENTER, RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, BT_SCALE, BT_ALPHABLEND, BT_KEEP_ASPECT_RATIO, BT_ALIGN_CENTER
from Tools.LoadPixmap import LoadPixmap

from Tools.Directories import resolveFilename, SCOPE_GUISKIN
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from Components.HTMLComponent import HTMLComponent

import NavigationInstance


class Pager(HTMLComponent, GUIComponent):
	def __init__(self):
		GUIComponent.__init__(self)
		self.l = eListboxPythonMultiContent()
		self.l_list = []
		self.l.setBuildFunc(self.buildEntry)
		self.current_index = 0
		self.itemHeight = 25
		self.sourceHeight = 25
		self.pagerForeground = 15774720
		self.pagerBackground = 624318628
		self.l.setItemHeight(self.itemHeight)
		self.l.setFont(1, gFont('Regular', 18))
		self.l.setFont(2, gFont('Regular', 22))
		self.l.setFont(3, gFont('Regular', 22))
		self.l.setFont(4, gFont('Regular', 22))
		self.l.setFont(5, gFont('Regular', 22))
		self.picDotPage = LoadPixmap(resolveFilename(SCOPE_GUISKIN, "icons/dot.png"))
		self.picDotCurPage = LoadPixmap(resolveFilename(SCOPE_GUISKIN, "icons/dotfull.png"))
		self.source = ""
		
	GUI_WIDGET = eListbox

	def buildEntry(self, currentPage, pageCount):
		width = self.l.getItemSize().width()
		xPos = width
		height = self.l.getItemSize().height()

		if self.picDotPage:
			pixd_size = self.picDotPage.size()
			pixd_width = pixd_size.width()
			pixd_height = pixd_size.height()
			width_dots = pixd_width + (pixd_width + 5)*pageCount
			xPos = (width - width_dots)/2 - pixd_width/2
		res = [ None ]
		if pageCount > 0:
			for x in range(pageCount + 1):
				if self.picDotPage and self.picDotCurPage:
					res.append(MultiContentEntryPixmapAlphaBlend(
								pos=(xPos, 0),
								size=(pixd_width, pixd_height),
								png=self.picDotCurPage if x == currentPage else self.picDotPage,
								backcolor=None, backcolor_sel=None, flags=BT_ALIGN_CENTER))
					xPos += pixd_width + 5
		return res

	def selChange(self, currentPage, pagesCount):
		self.l_list = []
		self.l_list.append((currentPage, pagesCount))
		self.l.setList(self.l_list)

	def postWidgetCreate(self, instance):
		instance.setSelectionEnable(False)
		instance.setContent(self.l)
		
	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "pagerForeground":
				self.pagerForeground = parseColor(value).argb()
			elif attrib == "pagerBackground":
				self.pagerBackground = parseColor(value).argb()
			elif attrib == "picPage":
				pic = LoadPixmap(resolveFilename(SCOPE_GUISKIN, value))
				if pic:
					self.picDotPage = pic
			elif attrib == "picPageCurrent":
				pic = LoadPixmap(resolveFilename(SCOPE_GUISKIN, value))
				if pic:
					self.picDotCurPage = pic
			elif attrib == "sourceElement":
				self.source = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return GUIComponent.applySkin(self, desktop, parent)

	