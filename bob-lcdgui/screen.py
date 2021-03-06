import view as Views
import time
import sys
sys.path.append('.') #this is the path relative to bob_init.sh
from common.sender import sender
import calendar
import os
import json

class Screen(object):
	def __init__(self, display):
		self.display = display
		self.trigger = True
		
	def updateScreen(self, command):
		#print 'button pressed:', command
		if self.trigger: self.view.updateView()
		return self._update(command)
				
	def _update(self, command):
		pass
		
class IdleScreen(Screen):
	def __init__(self, display):
		super(IdleScreen, self).__init__(display)
		self.view = Views.StandardView(self.display)
		
	def _update(self, command):
		self.view.lines[0] = time.strftime("%d/%m/%Y  %H:%M:%S")
		self.view.lines[1] = 'Temperature: %.1f C' % float(sender.sendMessage('get temp'))
		self.view.lines[2] = 'Humidity: %.0f %%' % float(sender.sendMessage('get hum'))
		fan_in = int(float(sender.sendMessage('get fan_in'))*100)/25
		fan_out = int(float(sender.sendMessage('get fan_out'))*100)/25
		self.view.lines[3] = 'Fan IN:'+'='*fan_in+' '*(4-fan_in)+' OUT:'+'='*fan_out
		if command == 'OK':
			return MenuScreen(self.display)
		elif command == 'UP':
			if sender.sendMessage('get lamp') == 'on':
				sender.sendMessage('set lamp off')
			else:
				sender.sendMessage('set lamp on')
			
		return self
	
class MenuScreen(Screen):
	def __init__(self, display):
		super(MenuScreen, self).__init__(display)
		self.view = Views.ListView(self.display, 'Menu', ['Date & Time', 'Sensor bias', 'Set point', 'Logging'])
		
	def _update(self, command):
		self.trigger = True
		if command == 'BACK':
			return IdleScreen(self.display)
		elif command == 'UP':
			self.view.cursorUp()
		elif command == 'DOWN':
			self.view.cursorDown()
		elif command == 'OK':
			sel = self.view.getOptionIndex()
			if sel == 0:
				return DatetimeScreen(self.display)
			elif sel == 2:
				return SetpointScreen(self.display)
		else:
			self.trigger = False
		return self
		
class SetpointScreen(Screen):
	def __init__(self, display):
		super(SetpointScreen, self).__init__(display)
		self.view = Views.SpinnerView(self.display, 'Set Point:')
		#create the spinners
		spinner_values = map(lambda y: str(y/10.0), range(300, 405, 5))
		setpoint_spinner = Views.Spinner(spinner_values)
		self.view.addSpinner(setpoint_spinner)
		
	def _update(self, command):
		self.trigger = True
		if command == 'BACK':
			return MenuScreen(self.display)
		elif command == 'UP':
			self.view.getSelectedSpinner().spinUp()
		elif command == 'DOWN':
			self.view.getSelectedSpinner().spinDown()
		elif command == 'LEFT':
			self.view.prevSpinner()
		elif command == 'RIGHT':
			self.view.nextSpinner()
		elif command == 'OK':
			sender.sendMessage('set setPoint '+self.view.getSelectedSpinner().getValue())
			return MenuScreen(self.display)
		else:
			self.trigger = False
		return self
		
class DatetimeScreen(Screen):
	def __init__(self, display):
		super(DatetimeScreen, self).__init__(display)
		self.view = Views.SpinnerView(self.display, 'Date & Time:')
		currentDT = time.localtime()
		
		days_values = range(1, self.daysOfMonth(currentDT.tm_year, currentDT.tm_mon)+1)
		months_values = range(1,13)
		years_values = range(2016, 2117)
		#sets the days spinner
		days_spinner = Views.Spinner(days_values, '{0:02d}')
		days_spinner.spinIndex = currentDT.tm_mday-1
		#sets the months spinner
		months_spinner = Views.Spinner(months_values, '{0:02d}')
		months_spinner.spinIndex = currentDT.tm_mon-1
		#sets the years spinner
		years_spinner = Views.Spinner(years_values, '{}')
		years_spinner.spinIndex = currentDT.tm_year-2016
		#sets the hours spinner
		hours_spinner = Views.Spinner(range(0, 24), '{:02d}')
		hours_spinner.spinIndex = currentDT.tm_hour
		#sets the minute spinner
		minutes_spinner = Views.Spinner(range(0, 60), '{:02d}')
		minutes_spinner.spinIndex = currentDT.tm_min
		#sets the seconds spinner
		seconds_spinner = Views.Spinner(range(0, 60), '{:02d}')
		minutes_spinner.spinIndex = currentDT.tm_sec
		
		self.view.addSpinner(days_spinner)
		self.view.addSeparator('/')
		self.view.addSpinner(months_spinner)
		self.view.addSeparator('/')
		self.view.addSpinner(years_spinner)
		self.view.addSeparator('  ')
		self.view.addSpinner(hours_spinner)
		self.view.addSeparator(':')
		self.view.addSpinner(minutes_spinner)
		self.view.addSeparator(':')
		self.view.addSpinner(seconds_spinner)
	
	def _setDaySpinnerVals(self):
		months_spinner = self.view.spinners[1]
		if months_spinner.getValue() == 2:
			year = self.view.spinners[2].getValue()
			self.view.spinners[0].setValues(calendar.monthrange(year, 2)[1])
			
	def daysOfMonth(self, year, month):
		days_n = calendar.monthrange(year, month)[1]
		return days_n
		
	def updateDays(self):
		year = self.view.spinners[2].getValue()
		month = self.view.spinners[1].getValue()
		prev_day = self.view.spinners[0].getValue()
		max_days = self.daysOfMonth(year, month)
		self.view.spinners[0].setValues(range(1, max_days+1))
		if prev_day > max_days:
			self.view.spinners[0].spinIndex = max_days-1
		else:
			self.view.spinners[0].spinIndex = prev_day-1
			
	
	def _update(self, command):
		self.trigger = True
		if command == 'BACK':
			return MenuScreen(self.display)
		elif command == 'UP':
			self.view.getSelectedSpinner().spinUp()
		elif command == 'DOWN':
			self.view.getSelectedSpinner().spinDown()
		elif command == 'LEFT':
			self.view.prevSpinner()
		elif command == 'RIGHT':
			self.view.nextSpinner()
		elif command == 'OK':
			day = self.view.spinners[0].getValue()
			month = self.view.spinners[1].getValue()
			year = self.view.spinners[2].getValue()
			date_str = '{0}-{1}-{2}'.format(year, month, day)
			os.system("sudo timedatectl set-time "+date_str)
			return MenuScreen(self.display)
		else:
			self.trigger = False
		if self.trigger:
			self.updateDays()
		return self

class AlarmScreen(Screen):
	def __init__(self, display, alarms):
		super(AlarmScreen, self).__init__(display)
		self.view = Views.StandardView(self.display)
		self.view.lines[0] = 'ALARM ALARM ALARM'
		alarm_dict = json.loads(alarms)
		self.alarm_lines = alarm_dict.values()
		self.view.lines[2] = self.alarm_lines[0]
		self.last_update_time = time.time()
		self.alarm_line_index = 0
	
	def _update(self, command):
		current_time = time.time()
		time_delta = current_time - self.last_update_time
		if time_delta < 1:
			self.trigger = False
		else:
			self.last_update_time = current_time
			self.alarm_line_index = (self.alarm_line_index + 1) % len(self.alarm_lines)
			self.view.lines[2] = self.alarm_lines[self.alarm_line_index]
			self.trigger = True
		
		if command == 'RESET':
			sender.sendMessage('reset-alarms')
			return IdleScreen(self.display)
		return self