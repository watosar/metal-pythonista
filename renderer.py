from objc_util import *
import os
from ctypes import *
import sys
import time

load_framework('Metal')

MTLCompileOptions, MTLRenderPipelineDescriptor, MTLRenderPipelineReflection = map(ObjCClass,('MTLCompileOptions','MTLRenderPipelineDescriptor', 'MTLRenderPipelineReflection'))

             

device = None
pipeline_state = None
command_queue = None
viewport_size = [300.0,300.0]

triangle_position = [
    [ 250.0,-250.0],
    [-250.0,-250.0],
    [   0.0, 250.0]
]

triangle_color = [
    [1.0,0.0,0.0,1.0],
    [0.0,1.0,0.0,1.0],
    [0.0,0.0,1.0,1.0]
]

flg = False
def get_shader_source():
    with open('shader.metal.js', 'r', encoding='utf-8') as f:
        shader = f.read()
    return shader


def PyRenderer_mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
    global viewport_size
    print('size change')
    size = ObjCInstance(_size)
    viewport_size[:] = size.width, size.height


def PyRenderer_drawInMTKView_(_self, _cmd, _view):
    #time.sleep(1)
    view = ObjCInstance(_view)
    #view.setClearColor_((1.0,0.0,0.0,1.0))
    command_buffer = command_queue.commandBuffer()
    command_buffer.label = 'MyCommand'
    
    renderpass_descriptor = view.currentRenderPassDescriptor()
    
    if renderpass_descriptor != None:
        
        render_encoder = command_buffer.renderCommandEncoderWithDescriptor_(renderpass_descriptor)
        
        render_encoder.label = "MyRenderEncoder"
        
        #view_port = (0.0, 0.0, viewport_size[0], viewport_size[1], 0.0, 1.0)
        #render_encoder.setViewport_(view_port)
        
        render_encoder.setRenderPipelineState_(pipeline_state)
        
        '''
        render_encoder.setVertexBytes_length_atIndex_(
            id(triangle_position),
            2*3, # sizeof(),
            0 # AAPLVertexInputIndexVertices
        )
        
        render_encoder.setVertexBytes_length_atIndex_(
            id(triangle_color),
            4*3, # sizeof(),
            1 # AAPLVertexInputIndexVertices
        )
        
        render_encoder.setVertexBytes_length_atIndex_(
            id(viewport_size),
            2, #sizeof(viewport_size),
            2 # AAPLVertexInputIndexViewportSize
        )
        
        render_encoder.drawPrimitives_vertexStart_vertexCount_(
            3, #MTLPrimitiveTypeTriangle,
            0, 
            3
        )'''
        
        render_encoder.endEncoding()
        command_buffer.presentDrawable_(view.currentDrawable())
        
    command_buffer.commit()
    #print('draw end')

PyRenderer = create_objc_class(
    'PyRenderer',
    superclass = NSObject,
    methods=[
        PyRenderer_mtkView_drawableSizeWillChange_,
        PyRenderer_drawInMTKView_
    ],
    classmethods=[],
    protocols = ['MTKViewDelegate']
)

pipeline_state_descriptor=None
def init(view):
    print('init')
    global device, pipeline_state, command_queue, pipeline_state_descriptor
    device = view.device()
    _error  = c_void_p()
     
    default_library = device.newLibraryWithSource_options_error_(get_shader_source(), MTLCompileOptions.new(), _error)
    
    if _error.value:
        error = ObjCInstance(_error)
        print(error)
        return 
        
    vertex_function = default_library.newFunctionWithName_("vertexShader")
    fragment_function = default_library.newFunctionWithName_("fragmentShader")
    
    pipeline_state_descriptor = MTLRenderPipelineDescriptor.alloc().init()
    #pipeline_state_descriptor.release()
    pipeline_state_descriptor.label = "Simple Pipeline"
    pipeline_state_descriptor.vertexFunction = vertex_function
    pipeline_state_descriptor.fragmentFunction = fragment_function
    
    pipeline_state_descriptor.colorAttachments().objectAtIndexedSubscript(0).pixelFormat = view.colorPixelFormat()
     
    _error = c_void_p()
    pipeline_state = device.newRenderPipelineStateWithDescriptor_error_(pipeline_state_descriptor, _error)
    
    if not pipeline_state:
        print(pipeline_state_descriptor_p)
        print("Failed to created pipeline state,",)
        error = ObjCInstance(_error)
        print(error)
        return 
    print(pipeline_state) 
    command_queue = device.newCommandQueue()
    
    renderer = PyRenderer.new()
    #renderer.release()
    print('init end')
    return renderer

