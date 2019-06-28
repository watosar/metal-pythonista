
import ctypes
from objc_util import *
import renderer


def ViewController_viewDidLoad(_self, _cmd):
    # never be called
    print('did load')
    
    
def ViewController_viewWillAppear_(_self, _cmd, animated):
    print('will appear')
    view = ObjCInstance(_self).view()
    view.delegate = renderer.init(view)
    view.preferredFramesPerSecond = 60


UIViewController = ObjCClass('UIViewController')
ViewController = create_objc_class(
    'ViewController',
    superclass = UIViewController,
    methods=[
        ViewController_viewDidLoad,
        ViewController_viewWillAppear_
    ]
)
