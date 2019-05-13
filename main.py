import ui
from objc_util import *
from viewcontroller import *

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
        sceneview = create_view(0, 0, screen.width, screen.height)
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


my_view = MyView()
my_view.present('full_screen', hide_title_bar=False)
my_view.initialize()
