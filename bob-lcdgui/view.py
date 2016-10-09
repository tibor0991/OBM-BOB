from display_i2c import i2c_lcd
import button_mapping

class View(object):
	def __init__(self, display):
		self.display = display
		self.display.clear()
		self.lines = ['','','','']
		
	def updateView(self):
		self._update()
		self.showView()
	
	def showView(self):
		self.display.home()
		i = 0
		for line in self.lines:
			self.display.setPosition(0, i)
			self.display.writeString(line)
			i += 1
	
	def _update(self):
		pass

class StandardView(View):
	def __init__(self, display):
		super(StandardView, self).__init__(display)
			
class ListView(View):
	def __init__(self, display, title, options):
		super(ListView, self).__init__(display)
		self.listIndex = 0
		self.options = [option + ' '*(18-len(option)) + 'I' for option in options]
		self.options[0] = self.options[0][:18] + '='
		self.options[len(self.options)-1] = self.options[len(self.options)-1][:18] + '='
		self.lines[0] = title
					
	def cursorUp(self):
		if self.listIndex > 0:
			self.listIndex -= 1
			
	def cursorDown(self):
		if self.listIndex < len(self.options)-1 :
				self.listIndex += 1
			
	def _update(self):
		selected = self.options[self.listIndex]
		if self.listIndex < len(self.options) - 3:
			self.lines[1:] = ['>' + option if option == selected else ' '+option  for option in self.options[self.listIndex:(self.listIndex+3)] ]
		else:
			self.lines[1:] = ['>' + option if option == selected else ' '+option  for option in self.options[len(self.options)-3:len(self.options)] ]
	def getOptionIndex(self):
		return self.listIndex
		
		
class Spinner:
	SPIN_DOWN = 1
	SPIN_UP = -1
	def __init__(self, values, format_str='{}'):
		self.setValues(values)
		self.format_str = format_str
		
	def spinUp(self):
		self._spin(Spinner.SPIN_UP)
		
	def spinDown(self):
		self._spin(Spinner.SPIN_DOWN)
		
	def _spin(self, dir):
		self.spinIndex = (self.spinIndex + dir) % len(self.values)
	
	def getValue(self):
		return self.values[self.spinIndex]
		
	def getFormattedValue(self):
		return self.format_str.format(self.getValue())
		
	def setValues(self, values):
		self.values = values
		self.spinIndex = 0
	
	def getSplitter(self):
		return self.splitter
		
	
		
class SpinnerView(View):
	def __init__(self, display, title):
		super(SpinnerView, self).__init__(display)
		self.lines[0] = title
		self.spinners = []
		self.spinnerIndex = 0
		
	def addSpinner(self, spinner):
		self.spinners.append(spinner)
		
	def nextSpinner(self):
		self.spinnerIndex = (self.spinnerIndex + 1) % len(self.spinners)
		
	def prevSpinner(self):
		self.spinnerIndex = (self.spinnerIndex - 1) % len(self.spinners)
		
	def getSelectedSpinner(self):
		return self.spinners[self.spinnerIndex]
		
	def _update(self):
		spinner_line = ''
		cursor_start = 0
		for spinner in self.spinners:
			if spinner == self.getSelectedSpinner():
				cursor_line_prefix = ' '*cursor_start
				cursor_line_cursor = '^'*len(str(spinner.getValue()))
				cursor_line_suffix = ' '*(20-len(cursor_line_prefix+cursor_line_cursor))
				cursor_line = cursor_line_prefix+cursor_line_cursor+cursor_line_suffix
				self.lines[3] = cursor_line
			spinner_line += spinner.getFormattedValue()
			cursor_start = len(spinner_line)
			
		self.lines[2] = spinner_line
		
		
		