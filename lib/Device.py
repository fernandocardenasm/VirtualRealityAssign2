#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

### import python libraries
# ...

class MultiDofInput(avango.script.Script):

  ### output fields
  mf_dof = avango.MFFloat()
  mf_dof.value = [0.0,0.0,0.0,0.0,0.0,0.0,0.0] # init 7 channels

  mf_buttons = avango.MFBool()
  mf_buttons.value = [False, False, False] # init 3 buttons
  
  
  ### functions
  def filter_channel(self, VALUE, OFFSET, MIN, MAX, NEG_THRESHOLD, POS_THRESHOLD):

    VALUE = VALUE - OFFSET
    MIN = MIN - OFFSET
    MAX = MAX - OFFSET

    if VALUE > 0:
      _pos = MAX * POS_THRESHOLD * 0.01

      if VALUE > _pos: # above positive threshold
        VALUE = min( (VALUE - _pos) / (MAX - _pos), 1.0) # normalize interval

      else: # beneath positive threshold
        VALUE = 0

    elif VALUE < 0:
      _neg = MIN * NEG_THRESHOLD * 0.01

      if VALUE < _neg:
        VALUE = max( (VALUE - _neg) / abs(MIN - _neg), -1.0)

      else: # above negative threshold
        VALUE = 0
      
    return VALUE


class SpacemouseInput1(MultiDofInput):
 
  def my_constructor(self, DEVICE_STATION):
  
    ### init sensor
    self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.device_sensor.Station.value = DEVICE_STATION

    ### init callback triggers
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)

    
  ### callbacks
  def frame_callback(self): # evaluated every frame
    
    # button input
    _button1 = self.device_sensor.Button0.value
    _button2 = self.device_sensor.Button1.value
    
    #print(_button1, _button2)
    
    _flag = False
    _buttons = self.mf_buttons.value
    
    if _button1 != _buttons[0]: # trigger changes
      _flag = True

    if _button2 != _buttons[1]: # trigger changes
      _flag = True
     
    if _flag == True: # forward input once per frame (unless there is no input at all)
      self.mf_buttons.value = [_button1,_button2,False]
      
    _x = self.device_sensor.Value0.value
    _y = self.device_sensor.Value1.value * -1.0
    _z = self.device_sensor.Value2.value
    _rx = self.device_sensor.Value3.value
    _ry = self.device_sensor.Value4.value * -1.0
    _rz = self.device_sensor.Value5.value
    
    if _x != 0.0:
      _x = self.filter_channel(_x, 0.0, -0.76, 0.82, 3, 3)
    
    if _y != 0.0:
      _y = self.filter_channel(_y, 0.0, -0.7, 0.6, 3, 3)
      
    if _z != 0.0:
      _z = self.filter_channel(_z, 0.0, -0.95, 0.8, 3, 3)
        
    if _rx != 0.0:
      _rx = self.filter_channel(_rx, 0.0, -0.82, 0.8, 12, 12)
     
    if _ry != 0.0:
      _ry = self.filter_channel(_ry, 0.0, -0.5, 0.6, 12, 12)
    
    if _rz != 0.0:
      _rz = self.filter_channel(_rz, 0.0, -0.86, 0.77, 12, 12)
     
    self.mf_dof.value = [_x,_y,_z,_rx,_ry,_rz,0.0]


class SpacemouseInput2(MultiDofInput):
 
  def my_constructor(self, DEVICE_STATION):
  
    ### init sensor
    self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.device_sensor.Station.value = DEVICE_STATION

    ### init callback triggers
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)

    
  ### callbacks
  def frame_callback(self): # evaluated every frame
    
    # button input
    _button1 = self.device_sensor.Button0.value
    _button2 = self.device_sensor.Button1.value
    
    #print(_button1, _button2)
    
    _flag = False
    _buttons = self.mf_buttons.value
    
    if _button1 != _buttons[0]: # trigger changes
      _flag = True

    if _button2 != _buttons[1]: # trigger changes
      _flag = True
     
    if _flag == True: # forward input once per frame (unless there is no input at all)
      self.mf_buttons.value = [_button1,_button2,False]
      
    _x = self.device_sensor.Value0.value
    _y = self.device_sensor.Value1.value * -1.0
    _z = self.device_sensor.Value2.value
    _rx = self.device_sensor.Value3.value
    _ry = self.device_sensor.Value4.value * -1.0
    _rz = self.device_sensor.Value5.value
    
    if _x != 0.0:
      _x = self.filter_channel(_x, 0.0, -350.0, 350.0, 2, 2)
    
    if _y != 0.0:
      _y = self.filter_channel(_y, 0.0, -350.0, 350.0, 2, 2)
      
    if _z != 0.0:
      _z = self.filter_channel(_z, 0.0, -350.0, 350.0, 2, 2)
        
    if _rx != 0.0:
      _rx = self.filter_channel(_rx, 0.0, -350.0, 350.0, 5, 5)
     
    if _ry != 0.0:
      _ry = self.filter_channel(_ry, 0.0, -350.0, 350.0, 5, 5)
    
    if _rz != 0.0:
      _rz = self.filter_channel(_rz, 0.0, -350.0, 350.0, 5, 5)
     
    self.mf_dof.value = [_x,_y,_z,_rx,_ry,_rz,0.0]



class KeyboardInput(MultiDofInput):
 
  
  def my_constructor(self, DEVICE_STATION):
  
    ### init device sensors
    self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.device_sensor.Station.value = DEVICE_STATION

    ### init callback triggers
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)

        
  ### callbacks
  def frame_callback(self): # evaluated every frame
  
    # button input
    _key1 = self.device_sensor.Button2.value # w
    _key2 = self.device_sensor.Button3.value # a
    _key3 = self.device_sensor.Button4.value # s
    _key4 = self.device_sensor.Button5.value # d
    _key5 = self.device_sensor.Button6.value # page up
    _key6 = self.device_sensor.Button7.value # page down
    _key7 = self.device_sensor.Button8.value # arrow left
    _key8 = self.device_sensor.Button9.value # arrow right
    _key9 = self.device_sensor.Button10.value # arrow up    
    _key10 = self.device_sensor.Button11.value # arrow down

    _x = 0.0
    _y = 0.0
    _z = 0.0
    _rx = 0.0
    _ry = 0.0
    #_rz = 0.0

    if _key2 == True:
      _x = -1.0

    if _key4 == True:
      _x = 1.0

    if _key5 == True:
      _y = 1.0

    if _key6 == True:
      _y = -1.0

    if _key1 == True:
      _z = -1.0

    if _key3 == True:
      _z = 1.0    

    if _key7 == True:
      _ry = 1.0

    if _key8 == True:
      _ry = -1.0

    if _key9 == True:
      _rx = 1.0

    if _key10 == True:
      _rx = -1.0
    
    _x *= 0.2
    _y *= 0.2
    _z *= 0.2        
    _rx *= 0.2
    _ry *= 0.2
    
    self.mf_dof.value = [_x,_y,_z,_rx,_ry,0.0,0.0]
    

class MouseInput(MultiDofInput):
 
  def my_constructor(self, DEVICE_STATION):
  
    ### init device sensors
    self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.device_sensor.Station.value = DEVICE_STATION

    ### init callback triggers
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)
    
        
  ### callbacks
  def frame_callback(self): # evaluated every frame    
    
    # button input
    _button1 = self.device_sensor.Button0.value
    _button2 = self.device_sensor.Button1.value
    
    #print _button1, _button2
    
    _flag = False
    _buttons = self.mf_buttons.value
    
    if _button1 != _buttons[0]: # trigger changes
      _flag = True

    if _button2 != _buttons[1]: # trigger changes
      _flag = True
     
    if _flag == True: # forward input once per frame (unless there is no input at all)
      self.mf_buttons.value = [_button1,_button2,False]
      
    _x = self.device_sensor.Value0.value
    _y = self.device_sensor.Value1.value * -1.0

    #print _x, _y
    
    if _x != 0.0:
      _x = self.filter_channel(_x, 0.0, -100.0, 100.0, 0, 0)
    
    if _y != 0.0:
      _y = self.filter_channel(_y, 0.0, -100.0, 100.0, 0, 0)
          
    self.mf_dof.value = [_x,_y,0.0,0.0,0.0,0.0,0.0]



