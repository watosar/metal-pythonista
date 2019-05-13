
import ctypes
from objc_util import *
import renderer as py_renderer


def ViewController_viewDidLoad(_self, _cmd):
    print('did load')
    
def ViewController_viewWillAppear_(_self, _cmd, animated):
    print('will appear')
    view = ObjCInstance(_self).view()
    print(view)
    renderer = py_renderer.init(view)
    print(renderer)
    view.delegate = renderer
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
