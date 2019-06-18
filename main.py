import ui
from objc_util import *
from viewcontroller import *
import time
import os
load_framework('Metal')
MTKView = ObjCClass('MTKView')

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.restype = c_void_p
def mtl_create_system_default_device():
    return ObjCInstance(MTLCreateSystemDefaultDevice())

def create_view(x, y, w, h):
    view = MTKView.alloc().initWithFrame_device_((CGRect(CGPoint(x, y), CGSize(w, h))), mtl_create_system_default_device())
    return view
    

sceneview = None
cvc = None

@on_main_thread
class MyView(ui.View):
    def initialize(self):
        global sceneview, cvc
        
        screen = ui.get_screen_size()
        #sceneview = create_view(0, 0, screen.width, screen.height)
        sceneview = create_view(0, 0, 375, 375)
        cvc = ViewController.new().autorelease()
        
        cvc.view = sceneview
        #cvc.view().setShowsStatistics_(True)
    
        print('is loaded?', cvc.isViewLoaded())
        self_objc = ObjCInstance(self)
        self_objc.nextResponder().addChildViewController_(cvc)
        self_objc.addSubview_(sceneview)
        cvc.didMoveToParentViewController_(self_objc)
        
    def will_close(self):
        print('----close----')
        os._exit(0)



my_view = MyView()


my_view.present('full_screen', hide_title_bar=False,)
my_view.initialize()

seek_bar_view = ui.load_view('seek_bar')
my_view.add_subview(seek_bar_view)
seek_bar = seek_bar_view['seek_bar']
current_time = seek_bar_view['current_time']
button = seek_bar_view['button']

play_flg = True
max_time = 3
s_time = py_renderer.s_time

def seek_action(_=None):
    global s_time, play_flg
    play_flg = False
    button.image = ui.Image.named('iob:play_256')
    if seek_bar.value is not None:
        s_time = time.time() - seek_bar.value * max_time
        current_time.text = str(float(seek_bar.value*max_time))[:3]

def time_controlle():
    global s_time, play_flg
    if not play_flg:
        seek_action()
        return seek_bar.value * max_time
    seek = time.time() - s_time
    if seek > max_time:
        play_flg = False
        button.image = ui.Image.named('iob:play_256')
        s_time = time.time() - max_time
    seek_bar.value = seek/max_time
    current_time.text = str(float(seek))[:3]
    return seek
    
def switch_play_flg(_):
    global play_flg
    play_flg = not play_flg
    if play_flg:
        image = ui.Image.named('iob:pause_256')
    else:
        image = ui.Image.named('iob:play_256')
    button.image = image

seek_bar.action = seek_action
py_renderer.get_time = time_controlle
button.action = switch_play_flg

my_view.bg_color = (0,0.3,0,1)
sceneview.setPosition_((187.5,300))

